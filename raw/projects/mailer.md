# mailer (cs-smarthub)

## 프로젝트 개요
- **설명**: CS SmartHub - 사내 CS팀 업무 자동화 통합 허브 (메일 발송 + 모니터링 리포트 + 챗봇 모니터링)
- **유형**: 풀스택 애플리케이션 (React SPA + Express)
- **버전**: 0.1.0 (package name: cs-smarthub)
- **마지막 확인**: 2026-06-25
- **경로**: `/Users/sangjun/IdeaProjects/mailer`
- **규모**: 총 179 커밋. 기간 2026-03-27 ~ 2026-06-25 (현재진행). 2026-06-09 이후 +80커밋(이번 업데이트 구간).

## 기술 스택
- **프론트엔드**: React 19 + Vite 8 + Tailwind CSS 4 (디자인 토큰 @theme + Pretendard)
- **백엔드**: Express.js (Node.js, `server/`)
- **데이터베이스**: Supabase (Postgres). pg_cron 사용.
- **이메일**: Nodemailer / SMTP
- **LLM**: Google Gemini (`@google/generative-ai`, 기본 `gemini-2.5-flash`, `GEMINI_API_KEY`) — 로그 분석용 (best-effort)
- **브라우저 자동화**: Playwright (챗봇 시나리오 체크, GitHub Actions에서 실행)
- **UI**: @dnd-kit(드래그), cmdk(Cmd+K 팔레트), sonner(토스트), lucide-react
- **테스트**: vitest, @testing-library/react, supertest, jsdom
- **배포**: Vercel (`vercel.json`, `api/index.js` 진입)

## 개발 명령어
```bash
npm run dev           # vite + express 동시 (concurrently)
npm run dev:client    # vite만
npm run dev:server    # express만
npm run build         # 프로덕션 빌드
npm run test          # vitest run
npm run test:watch    # vitest watch
npm run lint          # eslint
```

## 화면 / 기능 (src/pages)
- **HubPage**: 통합 대시보드. 상태 배너(메일+챗봇 합산), 아이콘 레일, Cmd+K 팔레트.
- **MailerPage**: 메일 발송 작업(Job) + 발신자(Sender) 관리. 컴팩트 행 리스트, 하트비트 바, send_log 발송 이력, 이메일 검증·일괄 붙여넣기, 확인 다이얼로그·토스트·낙관적 토글.
- **GrafanaPage**: Elasticsearch/Prometheus 모니터링 리포트 자동 발송. LLM 로그 분석 요약, 영속 로그 유형(LogTypesTab), 쿼리 UI 관리, 설정.
- **ChatbotPage**: 챗봇 모니터링. 봇 CRUD, 시나리오 스텝(발화/버튼 클릭), 카테고리 필터, 수동 실행.
- **LoginPage**: 로그인(세션 쿠키, 100일 유지).

## 서버 구조 (server/)
- `index.js`, `db.js`, `smtp.js`
- `routes/`: `mailer.js`, `grafana.js`, `chatbot.js` (+ 각 .test.js)
- `grafana/`: `client.js`(ES 클라이언트), `report.js`, `schedule.js`, `settings.js`, `config.js`(시드/폴백), `email.js`, `analyze.js`(Gemini LLM 분석), `logTypes.js` (+ 테스트)
- 인증: `auth`(x-app-password 헤더) / `cronAuth`(Bearer CRON_SECRET — pg_cron·grafana tick·chatbot dispatch용)

## 챗봇 모니터링 (2026-06-10~ 신규)
- 로컬 `monitor_link.sh`(단일 봇 curl 가용성)를 대체. 여러 봇 등록 → 하루 1회 Playwright로 실제 사용자처럼 접속·발화·응답 확인 → 실패 시 메일.
- 러너: `scripts/chatbot-check.mjs` (Playwright chromium), 판정 순수함수 `scripts/lib/judge.mjs`.
- 워크플로우: `.github/workflows/chatbot-check.yml` — workflow_dispatch만 사용(on:schedule 제거).
- **정시 트리거**: Supabase pg_cron(chatbot-check-dispatch, 23:30 UTC=08:30 KST) → `/api/chatbot/dispatch` 호출 → GitHub Actions workflow_dispatch. (GH on:schedule은 ~2h 지연 실측되어 제거.)
- 시나리오 스텝 타입: 발화(입력창) / 버튼 클릭. 스텝별 셀렉터 오버라이드(⚙). iframe 포함 전체 프레임 탐색, 렌더링 지연 재시도.
- 카테고리(2026-06-22): 봇당 단일 카테고리(TEXT). 필터 칩 + 그룹 단위 부분 실행. 관리 목록(이름변경·삭제).
- 허브에서 전체/개별/카테고리별 수동 실행 버튼(GitHub dispatch).
- 외부(인터넷) 공개 봇 대상. 입력창 1순위 셀렉터는 사내 챗봇 솔루션 위젯 id, 이후 일반 휴리스틱.

## Grafana 리포트 신규 (2026-06-17~)
- **쿼리 UI 관리**: `config.js`에 하드코딩됐던 메트릭(Prometheus)·로그쿼리(ES)를 Supabase JSONB 컬럼(metrics/log_queries)로 이전, 설정 탭에서 추가/수정/삭제 + enabled 토글. 코드 배포 없이 모니터링 대상 변경. **테스트(실호출) 통과해야 등록**(POST /test-query). config.js는 시드/폴백.
- 설정 페이지 데스크톱 재구성, 쿼리 에디터 리디자인, 테스트=리포트 건수 일치(log_lag_hours 적용).

## Grafana LLM 로그 분석 + 영속 로그 유형 (2026-06-24~)
- 앱별 ERROR 로그를 Gemini가 분석 → 중복 정리 + "솔루션에서 확인할 포인트" 요약. 메일 + 웹 리포트 표시.
- 영속 로그 유형: LLM이 정리한 유형을 DB에 누적 저장. 웹에서 유형별 열람·노트·회차별 로그. 저장은 tick(발송 시각) 1회. 웹 수동 "재분석"은 미리보기(저장 안 함). LLM은 best-effort(실패해도 리포트 정상).
- AI 요약 불릿 한 줄 응답 분해 처리.
- **개별 로그 정규화(2026-06-25, PR #16)**: 타임라인이 중복 시각을 누락하던 문제 → LLM은 분류(rows 인덱스)만, 시각·메시지는 ES 원본 그대로 `grafana_log_entries`에 저장 → 모든 발생 시각 보존. 오늘 수집 하이라이트(run_at 기준), 회차별 메모.

## Supabase 마이그레이션 (최근)
- 20260610000000_add_send_log
- 20260610100000_add_chatbot_monitoring (chatbots / chatbot_check_log / chatbot_monitor_settings)
- 20260617000000_add_grafana_queries (metrics/log_queries JSONB)
- 20260622000000_add_chatbot_category, 20260622010000_add_chatbot_category_list
- 20260624000000_add_grafana_log_types (grafana_log_types / grafana_log_type_runs / last_analysis 캐시)
- 20260625000000_add_grafana_log_entries (개별 occurrence 보존)
- 20260625100000_add_grafana_log_type_run_note (회차 메모)

## 운영 규칙 (중요)
- **`supabase db push` 금지.** 로컬 마이그레이션 이력 ↔ 원격 DB divergence 때문. Management API(SUPABASE_ACCESS_TOKEN)로 멱등 SQL 적용. 마이그레이션 파일은 기록용.
- **배포는 PR 머지로.** main 직접 푸시 차단 → PR + `gh pr merge` → Vercel 자동 배포. 프로덕션 401은 정상(앱 비밀번호 게이트).
- 개발 워크플로우: superpowers(spec→plan→TDD), 브랜치-퍼-태스크, PR 단위.

## 시크릿 (이름만, 값 비공개)
- APP_PASSWORD, CRON_SECRET, GITHUB_TOKEN, GITHUB_REPO, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ACCESS_TOKEN, GEMINI_API_KEY, HUB_URL, SMTP 자격증명 등 (.env / Vercel Env / GitHub Secrets)

## 문서
- README.md: Vite 템플릿 기본값(프로젝트 설명 아님)
- CLAUDE.md / AGENTS.md: Vercel best practices 보일러플레이트
- docs/superpowers/specs·plans: 기능별 설계·구현 계획 (실질 문서)

## 상태
활발히 개발 중 (최근 커밋 2026-06-25). flagship 포트폴리오 프로젝트.
