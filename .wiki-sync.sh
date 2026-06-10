#!/bin/zsh
# sj-wiki 자동 위키화 — crontab에서 매일 09:00, 18:00 실행
# 동작: 마지막 동기화 이후 raw/ 에 새로 추가·변경된 파일만 찾아 헤드리스 claude로 위키화.
#       새 파일이 없으면 claude를 호출하지 않고 즉시 종료(토큰 절약).

export PATH="/Users/sangjun/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# 헤드리스 인증: cron은 macOS 로그인 키체인에 접근할 수 없으므로,
# `claude setup-token`으로 만든 장기 토큰을 파일에서 읽어 사용한다.
[ -f "$HOME/.sj-wiki-token" ] && export ANTHROPIC_AUTH_TOKEN="$(cat "$HOME/.sj-wiki-token")"

WIKI="/Users/sangjun/sj-wiki"
MARKER="$WIKI/.last_wiki_sync"   # 마지막 동기화 시각 기준 파일
LOG="$WIKI/.wiki-sync.log"
CLAUDE="/Users/sangjun/.local/bin/claude"

cd "$WIKI" || { echo "$(date '+%F %T') ERROR: cd 실패" >> "$LOG"; exit 1; }

# 1) 마지막 동기화 이후 새로/변경된 raw 파일 탐지 (마커 없으면 전체)
# 이미지/바이너리(스크린샷 등)는 자동 위키화 대상에서 제외 — 요청 시 수동 임베드한다.
if [ -f "$MARKER" ]; then
  NEW_FILES=$(find raw -type f -newer "$MARKER" ! \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.svg' -o -iname '*.pdf' \) 2>/dev/null)
else
  NEW_FILES=$(find raw -type f ! \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.svg' -o -iname '*.pdf' \) 2>/dev/null)
fi

# 2) 새 파일이 없으면 종료
if [ -z "$NEW_FILES" ]; then
  echo "$(date '+%F %T') 변경 없음 — 건너뜀" >> "$LOG"
  exit 0
fi

echo "$(date '+%F %T') 신규/변경 파일 감지:" >> "$LOG"
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

if "$CLAUDE" -p "$PROMPT" \
     --permission-mode acceptEdits \
     --allowedTools "Read,Edit,Write,Glob,Grep,Bash(find:*),Bash(ls:*)" \
     >> "$LOG" 2>&1; then
  # 4) 성공 시에만 마커 갱신 (실패 시 다음 실행에서 재시도)
  touch "$MARKER"
  echo "$(date '+%F %T') 위키화 완료" >> "$LOG"
else
  echo "$(date '+%F %T') ERROR: claude 실행 실패 (마커 미갱신, 다음 회차 재시도)" >> "$LOG"
  exit 1
fi
