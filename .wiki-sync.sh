#!/bin/zsh
# sj-wiki 자동 위키화 — launchd에서 매일 09:00, 18:00 실행
# 동작: 마지막 동기화 이후 raw/ 에 새로 추가·변경된 파일만 찾아 헤드리스 claude로 위키화.
#       새 파일이 없으면 claude를 호출하지 않고 즉시 종료(토큰 절약).
#
# 충돌 내성(2026-06-15 개선): 한 번의 git 충돌이 자동화를 영구히 망가뜨리던 문제를 해결.
#   - 시작 시 이전 회차가 남긴 미완료 rebase/merge/unmerged 상태를 자가 치유한다.
#   - pull --rebase 충돌 시 즉시 abort하여 깨진 상태를 절대 남기지 않는다.
#   - push는 경합(race) 대비 재시도하고, 진짜 콘텐츠 충돌은 백업 브랜치로 보존 후 원격 기준 복구한다.
#   - 중복 실행 잠금. log.md는 union 머지로 충돌을 원천 차단(.gitattributes).

export PATH="/Users/sangjun/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# 헤드리스 인증: cron/launchd는 macOS 로그인 키체인에 접근할 수 없으므로,
# `claude setup-token`으로 만든 장기 토큰을 파일에서 읽어 사용한다.
[ -f "$HOME/.sj-wiki-token" ] && export ANTHROPIC_AUTH_TOKEN="$(cat "$HOME/.sj-wiki-token")"

WIKI="/Users/sangjun/sj-wiki"
MARKER="$WIKI/.last_wiki_sync"   # 마지막으로 "원격까지 성공 동기화"된 시각 기준 파일
LOG="$WIKI/.wiki-sync.log"
LOCK="$WIKI/.wiki-sync.lock"
CLAUDE="/Users/sangjun/.local/bin/claude"

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

cd "$WIKI" || { log "ERROR: cd 실패"; exit 1; }

# ──────────────────────────────────────────────────────────────────────────
# 잠금: 중복 실행 방지(긴 claude 실행이 다음 스케줄과 겹쳐 충돌하는 것 차단).
#       3시간 이상 된 잠금은 죽은 프로세스 잔존으로 간주해 제거한다.
# ──────────────────────────────────────────────────────────────────────────
[ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +180 2>/dev/null)" ] && rmdir "$LOCK" 2>/dev/null
if ! mkdir "$LOCK" 2>/dev/null; then
  log "다른 인스턴스 실행 중 — 종료"
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT INT TERM

# ──────────────────────────────────────────────────────────────────────────
# 자가 치유: 이전 회차가 충돌로 중단되어 남긴 흔적을 정리한다.
#   이 한 단계가 "한 번의 충돌 → 자동화 영구 wedge"를 막는 핵심.
# ──────────────────────────────────────────────────────────────────────────
if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
  log "⚠ 이전 회차 rebase 미완료 감지 — abort로 복구"
  git rebase --abort >> "$LOG" 2>&1 || git rebase --quit >> "$LOG" 2>&1
fi
if [ -f .git/MERGE_HEAD ]; then
  log "⚠ 이전 회차 merge 미완료 감지 — abort로 복구"
  git merge --abort >> "$LOG" 2>&1
fi
if [ -n "$(git ls-files -u 2>/dev/null)" ]; then
  log "⚠ unmerged 파일 잔존 — origin/main 기준으로 강제 복구"
  git fetch -q origin main >> "$LOG" 2>&1
  git reset --hard origin/main >> "$LOG" 2>&1
fi

# ──────────────────────────────────────────────────────────────────────────
# 안전한 pull --rebase: 충돌이 나면 즉시 abort하여 깨진 상태를 남기지 않는다.
#   반환: 0=성공, 1=콘텐츠 충돌(abort 완료), 2=기타 실패
# ──────────────────────────────────────────────────────────────────────────
git_pull_rebase() {
  if git pull --rebase --autostash -q origin main >> "$LOG" 2>&1; then
    return 0
  fi
  if [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    git rebase --abort >> "$LOG" 2>&1   # --autostash는 abort 시 자동 복원
    log "⚠ rebase 충돌 — abort로 깨끗한 상태 복구"
    return 1
  fi
  log "⚠ git pull 실패(충돌 외 사유, 예: 네트워크) — 로컬 상태로 진행"
  return 2
}

# 0) 작업 전 원격 최신 반영. 충돌이면 abort하고 로컬로 진행(이후 push 단계에서 재시도).
git_pull_rebase

# 1) 마지막 동기화 이후 새로/변경된 raw 파일 탐지 (마커 없으면 전체)
# 이미지/바이너리(스크린샷 등)는 자동 위키화 대상에서 제외 — 요청 시 수동 임베드한다.
EXCL=( ! \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.svg' -o -iname '*.pdf' \) )
if [ -f "$MARKER" ]; then
  NEW_FILES=$(find raw -type f -newer "$MARKER" "${EXCL[@]}" 2>/dev/null)
else
  NEW_FILES=$(find raw -type f "${EXCL[@]}" 2>/dev/null)
fi

# 2) 새 파일이 없으면 종료
if [ -z "$NEW_FILES" ]; then
  log "변경 없음 — 건너뜀"
  exit 0
fi

log "신규/변경 파일 감지:"
echo "$NEW_FILES" | sed 's/^/    /' >> "$LOG"

# 3) 헤드리스 claude로 위키화 (자신의 폴더 안에서만 작업)
PROMPT="raw 폴더에 새로 추가/변경된 아래 파일들을 wiki/CLAUDE.md 운영 규칙에 따라 위키화해줘.

대상 파일:
$NEW_FILES

규칙:
- 기존에 있던 주제면 새 페이지를 만들지 말고 해당 wiki 페이지를 보강/수정한다.
- 서로 다른 특성의 자료 간 연관성과 의외의 연결점을 [[위키링크]]로 적극 교차참조한다.
- 모든 위키 페이지 맨 앞에 wiki/내-프로필.md 관점의 핵심 takeaway를 > [!tip] callout으로 넣는다.
- 작업 후 wiki/index.md(카테고리 분류)와 wiki/log.md(이력, 최신을 위로)를 갱신한다.
- raw/ 폴더는 읽기만 하고 절대 수정하지 않는다."

if ! "$CLAUDE" -p "$PROMPT" \
     --permission-mode acceptEdits \
     --allowedTools "Read,Edit,Write,Glob,Grep,Bash(find:*),Bash(ls:*)" \
     >> "$LOG" 2>&1; then
  log "ERROR: claude 실행 실패 (마커 미갱신, 다음 회차 재시도)"
  exit 1
fi
log "위키화 완료"

# 4) 변경분을 커밋. 변경이 없으면 이미 원격과 일치한다고 보고 마커만 갱신.
git add -A
if git diff --cached --quiet; then
  log "git: 변경 없음 — 이미 반영됨, 마커 갱신 후 종료"
  touch "$MARKER"
  exit 0
fi
git commit -q -m "auto(wiki): $(date '+%F %H:%M') 자동 위키화" \
  -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" >> "$LOG" 2>&1

# 5) push: 원격을 먼저 rebase로 반영하고 push. 경합(race)은 재시도로 흡수.
#    진짜 콘텐츠 충돌이면 자동 커밋을 백업 브랜치에 보존하고 원격 기준으로 복구한다.
SYNCED=false
for attempt in 1 2 3; do
  git_pull_rebase
  rc=$?
  if [ "$rc" -eq 1 ]; then
    # 콘텐츠 충돌: 손실 없이 보존 후 저장소를 깨끗한 원격 상태로 되돌린다.
    BK="conflict-backup-$(date '+%Y%m%d-%H%M%S')"
    git branch "$BK" >> "$LOG" 2>&1
    git fetch -q origin main >> "$LOG" 2>&1
    git reset --hard origin/main >> "$LOG" 2>&1
    log "⚠ 자동 위키화 결과가 원격과 충돌 — '$BK' 브랜치에 보존하고 저장소는 원격 기준으로 복구."
    log "   → 마커 미갱신: 다음 회차에 최신 원격 기준으로 재위키화하여 수렴(보통 충돌 해소). 필요 시 '$BK' 검토."
    break
  fi
  if git push -q origin main >> "$LOG" 2>&1; then
    SYNCED=true
    log "✅ git push 완료"
    break
  fi
  log "⚠ push 거부(원격이 그 사이 변경됨) — 재시도 $attempt/3"
done

# 6) 원격까지 성공적으로 동기화된 경우에만 마커 갱신.
#    (push 실패/충돌 시 마커를 두면 다음 회차가 동일 파일을 재처리해 자가 수렴)
if $SYNCED; then
  touch "$MARKER"
else
  log "⚠ 이번 회차 원격 동기화 미완료 — 마커 미갱신(다음 회차 재시도). 저장소는 깨끗한 상태."
fi
