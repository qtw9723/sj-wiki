---
title: 올림푸스 (Olympus) — 로컬 다세션 자율 개발 파이프라인
aliases: [Olympus, 올림푸스, olympus, dev-pipeline]
category: 프로젝트
tags: [프로젝트, 올림푸스, 에이전트, 멀티에이전트, 오케스트레이션, claude-code, 자동화, 개발도구, 포트폴리오, bash, 생성자-비평가, 자가개선]
source: raw/projects/olympus.md
created: 2026-07-01
updated: 2026-07-03
---

> [!tip] 핵심 takeaway
> 🧠 [[내-프로필]]의 **"비개발→개발 전환"·"업무 자동화"·"LLM 활용"** 세 축이 한 프로젝트에서 만나는 결과물이다. "AI가 코드를 짜준다"에서 한 발 더 나아가, **여러 Claude 세션이 역할을 나눠 협업하고 실행되는 테스트가 심판이 되게** 직접 오케스트레이션을 설계·구현했다 → 단순 사용자가 아니라 **에이전트 파이프라인을 만드는 사람**이라는 포트폴리오 근거.
> 🧠 핵심 통찰 하나면 충분: **"LLM 둘이 토론"이 아니라 "실행되는 게이트(lint·test·build) 위에서 싸우게"** 한다. LLM 합의가 아니라 실행 결과가 유일한 진실 → [[CogInsight-Generator]]의 zod 출력 검증, [[mailer]]의 Playwright E2E 게이트와 같은 "LLM을 실행으로 검증한다" 철학의 연장.
> 📄 이건 [[헤르메스-개인비서-Hostinger]] §7-2의 `dev-pipeline`이 **정식 이름(올림푸스)을 얻고 독립 프로젝트로 졸업한 것**이다(같은 코드 계보). 헤르메스(클라우드)로 올리기 전 **로컬 헤드리스로 동작·검증 완료**. 2026-07-02 리네임 확정 → 실제 저장소·디렉토리 모두 `olympus`.

## 한 줄 정의
📄 **기획서 폴더(`spec/<프로젝트>/`)만 넣고 `bash run.sh` 하면, 여러 Claude Code 세션(기획자·생성자·비평가)이 협업해 스펙을 분석·분해·개발하고, 실행되는 테스트(게이트)가 심판이 되어 완성까지 자동으로 굴리는 로컬 오케스트레이터.**

> [!info] 계보 = 헤르메스 §7-2 `dev-pipeline`의 졸업판 📄
> [[헤르메스-개인비서-Hostinger]] §7-2 "코드 자가개선 루프(생성자↔비평가)"의 로컬 구현이 이 도구다. 역할 4종(메티스·헤파이스토스·모모스·헤르메스)·`verify.sh` 그라운드 트루스·자율 트리아지·사람 승인 1회 설계가 그대로 이어진다. → 헤르메스 페이지 §7-2는 "구상+초기 구현", 이 페이지는 "검증까지 끝난 현재 상태"로 읽으면 된다.
>
> ✅ **이름·저장소 현황 (2026-07-02 리네임 완료 📄)**: 실제 저장소·로컬 디렉토리 모두 **`~/IdeaProjects/olympus` / GitHub `qtw9723/olympus`**(private)로 리네임 완료. README 제목·`config.sh`·`run.sh`의 `olympus/` 참조 커밋(`640bc3a`)·푸시, 로컬 dir `mv`, `gh repo rename olympus`까지 반영. (이전 이름 `dev-pipeline`은 계보/커밋 이력에만 남음 — GitHub redirect로 옛 URL도 당분간 접근 가능.)

## 배경 / 동기 📄
- [[헤르메스-개인비서-Hostinger]] §7-2의 "코드 자가개선 루프(생성자↔비평가)" 아이디어를, **헤르메스(클라우드)로 올리기 전에 로컬에서 먼저 검증**하려고 만든 PoC.
- 핵심 통찰: **"LLM 둘이 토론"이 아니라 "실행되는 테스트 위에서 싸우게"** 한다. LLM 합의가 아니라 lint·test·build 결과가 유일한 진실(ground truth).
- 이름 유래(🧠 네이밍): 기획자 **메티스**, 생성자 **헤파이스토스**, 비평가 **모모스**, 루프 제어 **헤르메스** — 이 그리스 신들이 사는 곳이 올림푸스.

## 역할 (다세션) 📄
- **메티스 (Metis) — 기획자/PO, 상시 세션**: 기획서를 **요구사항 분석(필수)**해 `requirements.md`에 의도를 보관(=기억). 작업을 백로그로 분해. 다른 세션 질문에 답하고, 합리적이면 원안과 달라도 변경을 수용·결정. 범위 밖 결함 자율 트리아지. brownfield면 기존 코드 먼저 파악.
- **헤파이스토스 (Hephaestus) — 생성자/Builder**: 스펙→코드+테스트. 최소 변경·동작 보존. 의도 모르면 추측 말고 기획자에게 질문(`ask-planner`).
- **모모스 (Momus) — 비평가/Critic**: 결함 검사. 칭찬 금지·증거 요구. verify를 **직접 재실행**(Builder 말 안 믿음, 깨끗한 셸). 심판 무결성 점검.
- **헤르메스 (Hermes) — 라우터**: `run.sh`가 담당. 차례·라운드·예산·질문 라우팅·사람 에스컬레이션.

🧠 [[헤르메스-개인비서-Hostinger]] §7-2의 원래 3역할 구상(생성/비평/제어)에 **기획자(메티스)를 더한 4역할**이 이 프로젝트의 진화 포인트 — "의도의 기억"을 상시 들고 변경을 자율 결정하는 축이 생겼다.

## 5단계 수명주기 📄
```
spec/<프로젝트>/  ─▶ [메티스] 요구사항 분석(필수) → requirements.md
                      ├─ 진짜 블로커만 → questions.md 쓰고 멈춤(사람)
                      ├─ 그 외 모호함 → 가정으로 진행 + open-questions.md 누적
                      └─ 분해 → backlog.md + 첫 task.md
      각 작업마다:
   [헤파이스토스] 구현+테스트 ──(의도 모르면)──▶ ask-planner → [메티스]가 답
        ▼  verify.sh(심판: lint·test·build)
   [모모스] 결함검사 + verify 재실행
        ↑ AC 위반 → 헤파이스토스   범위밖 결함 → findings(메티스 트리아지)   결함없음 → green
   green → [메티스] 다음 작업 → … → 전부 done → 사람 최종 승인(전체 1회, 머지)
```

## 핵심 설계 원칙 📄 (실전 검증으로 다듬어짐)
1. **그라운드 트루스 = 실행되는 게이트**. `verify.sh` = 대상 repo의 lint·test·build. LLM 의견 아님.
2. **비대칭 역할**(생성자≠비평가, 다른 모델 권장) — 대등한 둘은 함께 버그를 놓친다.
3. **심판 불가침**: Builder는 verify.sh·lint/test 설정·CI 수정 금지. 깨지면 ask-planner로 보고 → 비평가가 diff에 심판 파일이 섞였는지 필수 점검.
4. **자율 결함 트리아지**: 현재 작업 AC 밖 버그는 사람이 아니라 **메티스가** `findings.md`로 받아 백로그 추가/연기/기각을 자율 결정. 사람은 진짜 블로커·보안/스펙 중대위반·최종 승인에만.
5. **작업 단위 승인 없음**: 기획서 전체가 끝난 뒤 **사람 승인 1회**. 모호함은 가정으로 진행하고 끝에 일괄 확인.

## greenfield / brownfield 자동 판단 📄
- `spec/<이름>/` 폴더명 → `$PROJECTS_DIR/<이름>`(기본 `~/IdeaProjects/<이름>`).
- 경로가 **없으면 greenfield**: repo 자동 생성(git init) + 범용 게이트(`templates/verify.sh`, py/node 관용형) 설치.
- **있으면 brownfield**: 기존 코드 수정 모드. 안전하게 `olympus/<프로젝트>-<타임스탬프>` **작업 브랜치 자동 생성**(GIT_BRANCH: auto/none/이름). 각 세션에 개발 MODE 주입 → 기존 구조·규약 준수, 동작 보존, 기존 테스트 유지.

## 헤드리스 무인 실행 📄
- `bash run.sh` 한 방 — 대상 repo·게이트 지정 불필요(spec 폴더명으로 자동).
- `PERMISSION_FLAG`(무인 시 `--dangerously-skip-permissions`), 실행 로그(`state/runs/`), `turn=human` 자동중단(`pause_if_human`), `AUTO_APPROVE`(최종 승인까지 생략).
- `reset.sh`: 새 작업용 state 초기화. state는 런타임(git 미추적), 도구만 버전관리 → 지속 재사용.
- 기획자 상시성: `--session-id`/`--resume`로 세션 유지(안 되면 durable 파일로 맥락 유지).
- **원격 결정 브리지(`REMOTE=1`)** 📄: 사람 개입(진짜 블로커·의도 질문·최종 머지 승인)을 **폰으로** 원격화. 끄면 터미널에서 처리. **개입 종류에 따라 채널을 분리**한다(2026-07-03):
  - **블로커·의도질문**(자유서술 필요) → `olympus-inbox` repo 폴링. 폰 GitHub 앱에서 `## 답변` 채워 commit.
  - **최종 머지 승인**(가장 잦은 yes/no) → **메일 답장 경량 경로**(`APPROVE_VIA_EMAIL=1`, 기본): 승인 요청 메일에 **답장 첫 줄 `y`**(보류 `n`)만 보내면, run.sh가 **발송과 같은 Gmail 계정 IMAP**(SMTP 앱비번 재사용, 신규 서비스 0)을 폴링해 감지. GitHub 파일 편집보다 마찰↓. 견고화: 제목 토큰 `‹OLY-<id>›` run 매칭·대기시작 UIDNEXT 기준선으로 옛 메일 배제·인용부 이전 첫 줄 whole-line 파싱(인용 속 키워드 무시)·`APPROVE_FROM` 발신자 화이트리스트(위조 차단). IMAP 비밀 없음/접속 실패면 **GitHub 승인 경로로 자동 폴백**. `inbox_imap.py`·`remote_approve_email`, 라이브 E2E(발송→폰 y 답장→감지→머지) 검증 완료.
- **토큰 소진 자동 대기·재개(`TOKEN_WAIT=1`, 기본 켜짐)** 📄: 무인 실행 중 Claude Code **사용량 한도**(5시간/주간)에 걸리면 출력 패턴(`You've hit your`)으로 감지 → 리셋까지 대기 → **그 자리에서 자동 재개**. `resilience.sh`의 `claude_guarded`가 메티스/헤파이스토스의 `claude -p` 호출을 감싼다. 대기 중 토큰 ≈0(한도 거부는 추론 전 게이트), 429/일시적 과부하는 CLI 워치독(`CLAUDE_CODE_RETRY_WATCHDOG`)에 위임. macOS·Windows(Git Bash/WSL) 동작. ⚠ 한계: 대기는 실행 중 프로세스 안에서만 → 프로세스가 죽으면 유실, `bash run.sh` 재실행으로 state에서 재개(외부 supervisor 자동재실행은 후속 B안).

## 구성 파일 📄
- `config.sh`(TARGET_REPO·VERIFY_CMD·모델·GIT_BRANCH·권한·예산), `run.sh`(오케스트레이터), `reset.sh`, `templates/verify.sh`(범용 게이트), `roles/{metis,builder,critic}.md`, `spec/<프로젝트>/*.md`(입력), `state/*`(런타임: requirements·backlog·task·ask-planner·findings·questions·open-questions·critic-feedback·verify.txt·handoff.json·runs/).

## 검증 — Mindboard 실전 테스트 (2026-06~07) 📄
파이프라인 검증용으로 **Mindboard**(신규 풀스택 게시판: React+TS 프론트 + FastAPI+SQLite 백엔드, JWT 인증·CRUD·댓글·좋아요·검색·페이지네이션)를 기획서만 넣고 돌림. 결과 T1~T12(+T5.1) 전부 green.
> 📄 정밀: Mindboard는 `~/IdeaProjects/mindboard`에 **검증 산출물(작업 트리)로 존재**하나 아직 **git 커밋 0**(전부 untracked). 즉 올림푸스가 생성·검증한 로컬 결과물이지 커밋된 저장소는 아님. (올림푸스 도구 자체는 `qtw9723/olympus`에 push됨 — 아래 §현재 상태.)
- **백엔드 독립 검증**: 새 리눅스 venv에서 재실행 → ruff clean + **93 passed**. 진짜 green 확인.
- 파이프라인이 **한 단계 위에서** 잡아낸 것들(= 도구 가치 입증):
  - **심판 조작 시도**(T1: Builder가 verify.sh 수정) → Critic이 포착·에스컬레이션 → "심판 불가침" 규칙 신설.
  - **가짜 green 게이트**(T8: 프론트 `tsc --noEmit`가 무검사 통과) → Critic이 적대적으로 검출(빌드의 `tsc -b`가 실제 커버 확인).
  - **자기 오류 자기정정**(T3: Critic이 자기 T1 판정을 새 증거로 반증 — venv 부트스트랩이 py3.9 사용).
  - **자율 트리아지**(updated_at 버그를 메티스가 T5.1로 스케줄해 사람 없이 수정).
- 남은 사람 결정: liked_by_me 필드(스펙 갭, 계약변경), 반응형 수동 점검(R1) — 둘 다 정당하게 open-questions로 보류.

🧠 위 "심판 조작/가짜 green/자기정정"은 [[AI-주간-소식-2026-W25]]에서 정리한 **에이전트 신뢰성 이슈(평가 인식·제안-검증 구조)**가 실제 프로젝트에서 그대로 재현·대응된 사례다.

## 기술 스택 / 방식 📄
- 순수 **bash 오케스트레이션** + **Claude Code CLI 헤드리스(`claude -p`)** 다세션. 외부 의존 없음.
- 언어 무관: 골격 고정, 대상 언어별로 `VERIFY_CMD`/게이트만 교체(어댑터).
- state 파일 공유로 세션 간 통신 → 헤르메스(클라우드)에선 외부 영속 상태(Supabase 등)로 승격 예정.

## 현재 상태 / 다음 📄
- ✅ 로컬 도구로 동작·검증 완료. GitHub `qtw9723/olympus`(private)에 push(리네임 커밋 `640bc3a`, 2026-07-02).
- ✅ **"Olympus" 리네임 완료**: 로컬 dir `~/IdeaProjects/olympus`, GitHub repo `qtw9723/olympus`, 코드 내 참조·spec 하위폴더 규칙 정렬까지 반영(§계보 박스 ✅ 참조).
- ✅ **무인 실행 안정성 강화(2026-07)**: 원격 결정 브리지(`REMOTE`, 폰 승인)·**토큰 소진 자동 대기·재개(`TOKEN_WAIT`, `resilience.sh`)** 추가 → 장시간 무인 실행이 **사람 부재·토큰 한도에도 안 끊기고** 이어짐(§헤드리스 무인 실행).
- ⏸ 헤르메스(클라우드 상시)로는 아직 안 올림 — 당분간 로컬 헤드리스로 사용.
- 다음 후보: Phase 3(요구사항 완료 후 추가기능 제안·교차검증, README §헤르메스로의 매핑에 "미구현—다음 확장 후보"로 명시됨), 게이트 강화(tsc -b), 다중 대상 병행, **토큰 대기 B안**(프로세스 죽어도 자동 재실행하는 외부 supervisor).

## 진행사항 업데이트 로그
### 2026-07-03 (최종 승인 경량화 — Gmail 답장 경로 📄)
- **동기**: 원격 브리지 재검토(과설계/토큰/더 나은 방식 고민) → 결론 "구조는 유지, **가장 잦은 최종 승인만** 더 가벼운 채널로". 블로커·의도질문(자유서술)은 GitHub 유지, 최종 승인(yes/no)만 분리.
- **선택**: 신규 서비스 0 위해 **Gmail 답장 키워드**(Telegram 대신) — 이미 발송에 쓰는 계정의 IMAP 재사용. fragile 지점(스레드 매칭·인용 오탐·위조)은 설계로 잠금.
- **구현**: `inbox_imap.py`(IMAP 폴링 `--await` + 파싱 `--parse`), `remote.sh`의 `remote_approve_email`(remote_ask와 계약 호환), `run.sh` `APPROVE_VIA_EMAIL` 분기 + IMAP 불가 시 GitHub 자동 폴백, `config.sh` 노브 2종. spec/plan(docs/superpowers).
- **견고화**: 제목 토큰 `‹OLY-<id>›`·대기시작 **UIDNEXT 기준선**(실계정 자기발신 UNSEEN 47건 확인 후 추가)·인용부 이전 첫 줄 whole-line 파싱·From 화이트리스트.
- **검증**: 단위(파싱 14 + 래퍼/회귀 11) green + IMAP 로그인 스모크 + **라이브 E2E**(발송→폰 y 답장→감지→y/rc0). 🧠 E2E가 단위테스트로 못 잡은 실버그(무링크 `remote_notify`가 macOS bash 3.2+`set -u`에서 빈 배열 crash) 포착·수정 — "실행으로 검증한다" 철학이 자기 도구에서도 값을 함.
- 🧠 **의미**: [[cafe24-daily-monitoring-cron|클램셸 절전]]류 실행 영속성(b)은 여전히 로컬 종속이지만, 이번 변경은 결정 원격화(a)의 **마찰만** 낮춘 것 — Phase 2(Supabase+Vercel 웹앱)는 실행이 랩탑에 묶인 채라 ROI 낮다고 판단해 보류. PR #2 **스쿼시 머지 완료**(main `5178882`).

### 2026-07-03 (무인 실행 안정성 — 토큰 소진 자동 대기·재개 📄)
- 신규 `resilience.sh`(`claude_guarded`): `claude -p`가 **사용량 한도**로 실패하면 출력 패턴(`You've hit your`, 종료코드 미의존) 감지 → 리셋까지 대기 → **동일 호출 자동 재개**. run.sh의 메티스/헤파이스토스 **두 호출부만** 이 래퍼 경유하도록 배선.
- `config.sh` 노브 5종: `TOKEN_WAIT`(기본 1)·`TOKEN_RETRY_SEC`(1200)·`TOKEN_RESET_BUFFER_SEC`(60)·`TOKEN_WAIT_CHUNK_SEC`(1800)·`TOKEN_MAX_WAIT_SEC`(0=무제한). 429/529는 `CLAUDE_CODE_RETRY_WATCHDOG=1`로 CLI에 위임.
- **크로스플랫폼**(macOS BSD + Windows Git Bash/WSL): 리셋시각 파싱은 best-effort, 실패 시 간격 폴링으로 폴백(macOS). 대기 중 **토큰 ≈0**(한도 거부=추론 전 게이트, 무료). 재확인은 경량 프로브(`claude -p ok`)로.
- 프로세스: brainstorming→스펙→계획→**subagent-driven TDD 5태스크**(태스크별 리뷰)→최종 whole-branch 리뷰(Opus, **MERGE-READY**, 하한클램프 1건 반영)→main 머지·푸시. 사용법은 저장소 `README.md`·`spec/_README.md`에 문서화.
- 🧠 한계(A안): 대기는 실행 중 프로세스 안에서만 — 프로세스 종료 시 유실, `bash run.sh` 재실행으로 durable state에서 재개. 프로세스 죽어도 자동 재실행하는 외부 supervisor는 후속 B안 후보.

### 2026-07-02 (이름 정리 = dev-pipeline → Olympus 리네임 완료 📄)
- **로컬 디렉토리**: `~/IdeaProjects/dev-pipeline` → `~/IdeaProjects/olympus` (`mv`).
- **GitHub repo**: `qtw9723/dev-pipeline` → `qtw9723/olympus` (`gh repo rename`, remote URL 자동 갱신, 옛 URL은 redirect 유지). private 유지.
- **코드 참조 커밋**(`640bc3a`, push 완료): README 제목·`config.sh`·`run.sh`의 도구 폴더명 `dev-pipeline→olympus`, 옛 `spec/00-overview.md` 삭제.
- **spec 하위폴더 규칙 정렬**: 도구 자체 규칙(`spec/_README.md`: "프로젝트마다 하위 폴더 하나")에 맞춰 Mindboard 기획서를 **`spec/Mindboard/`** 로 이동(01~06 + 00_README). `spec/*`는 gitignore(가이드 `_README.md`만 추적)라 git 영향 없음.
- **로컬 파일 gitignore 추가**: `.DS_Store`, `.claude/`.

### 2026-07-02 (저장소 확인 📄, 당시 `qtw9723/dev-pipeline`)
- **역할별 모델 배치 확인** (`config.sh`, "비대칭 역할" 원칙 #2의 구체 증거): 기획자(메티스)·비평가(모모스) = `claude-opus-4-8`, 생성자(헤파이스토스) = `claude-sonnet-4-6`. 생성자≠비평가 다른 모델로 실제 구성됨. 기본 게이트 `VERIFY_CMD="bash verify.sh"`, `GIT_BRANCH=auto`(brownfield 작업브랜치 자동), `PROJECTS_DIR=~/IdeaProjects`, `TARGET_REPO`는 spec 폴더명으로 자동.
- **커밋 이력(6개, 2026-06-29~07-01)**: `dev-pipeline` 초기 구현(다세션 루프, 메티스+Builder↔Critic) → spec/ 폴더 입력 전환 → 헤드리스 자동실행+자율 트리아지+심판 무결성 → state 런타임 분리(git 미추적) → `spec/<프로젝트>/`만 넣으면 대상 repo 자동 생성(git init+범용 게이트).
- **spec/ 현황**: Mindboard 검증(아래 §검증)용 기획서 세트가 담겨 있음 — `01_기획개요(PRD)`·`02_기능명세`·`03_디자인가이드`·`04_기술아키텍처_API`·`05_화면설계`·`06_개발태스크`. (이후 위 리네임 작업에서 `spec/Mindboard/` 하위폴더로 정렬 완료.)

## 의외의 연결점 🧠
- **올림푸스로 내 다른 프로젝트를 개발**: Mindboard 검증 대상이 **React+FastAPI 풀스택(인증·CRUD·RBAC 유사)**이었다는 건, 형태가 거의 같은 [[콜링]](React + Node/Spring, 로그인·카테고리 권한·일정 CRUD)이나 [[팀숲-bible-forest]]를 **올림푸스의 spec으로 넣어 자동 개발**하는 게 현실적이라는 뜻. brownfield 모드로 [[mailer]]·[[notepad]] 기능 추가에도 붙일 수 있다.
- **"LLM을 실행으로 검증한다" 철학의 계열**: [[CogInsight-Generator]](zod 스키마로 LLM JSON 출력 검증) · [[mailer]](Playwright E2E로 챗봇 정상 여부 판정) · 올림푸스(verify.sh로 코드 판정) — 셋 다 "LLM 말을 믿지 않고 실행 결과로 판단"하는 같은 근육.
- **[[에이전트-자동화-도구]] / [[Claude-Code-업데이트-동향]] workflows와의 관계**: Claude Code의 dynamic workflows(다중 에이전트 오케스트레이션)가 하는 일을 **bash+헤드리스 CLI로 직접 손으로 구현**한 셈 → 내장 도구를 쓰기 전에 원리를 밑바닥부터 만들어 본 경험(포트폴리오 스토리로 강함).
- **[[내-프로필]] 경력 합류**: SM/인프라(bash·프로세스·게이트 운영) + NLP/LLM(에이전트 설계)이 한 도구에서 만난다.

## 관련 문서
- [[올림푸스-실행-런북]] — **실제로 돌릴 때 세션 세팅 체크리스트**(env·spec·노브·폰 개입)
- [[index]] · [[내-프로필]] · [[프로젝트-포트폴리오]]
- [[헤르메스-개인비서-Hostinger]] — §7-2 생성자↔비평가 루프(=올림푸스의 씨앗), dev-pipeline 초기 구현 이력
- [[notepad]] — 초기 로컬 PoC 대상(vitest + `verify` 게이트 도입)
- [[CogInsight-Generator]] · [[mailer]] — "LLM을 실행으로 검증" 계열 / brownfield 개발 대상 후보
- [[콜링]] · [[팀숲-bible-forest]] — 올림푸스 spec 투입 후보(풀스택 웹앱)
- [[에이전트-자동화-도구]] · [[Claude-Code-업데이트-동향]] · [[AI-주간-소식-2026-W25]] — 멀티에이전트·제안-검증 구조 동향
- 원본: `raw/projects/olympus.md`
