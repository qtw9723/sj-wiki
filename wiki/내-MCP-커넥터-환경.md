---
title: 내 MCP 커넥터 & 도구 환경
category: 도구/스킬
tags: [mcp, 커넥터, cowork, 도구, 자동화, 본인정보, 스킬공격면, 권한최소화, 프롬프트인젝션, 되돌림추적]
source: raw/my-connectors-and-techstack.md (회사 섹션 포함 원본은 sj-wiki-work vault로 이동), raw/ai-digest/2026-09-01.md (§4 스킬 공격면)
created: 2026-06-09
updated: 2026-09-01
---

> [!tip] 핵심 takeaway
> **네([[내-프로필]])가 지금 실제로 손에 쥔 자동화·에이전트 무기고.** macOS + Claude Cowork 데스크탑 환경에서 쓰는 MCP 커넥터·내장 도구·스킬의 단일 목록이다.
> 가장 큰 레버리지: ① **scheduled-tasks(cron)** = 크론탭 자동화의 GUI 후계자 ② **computer-use / Claude in Chrome** = 화면 제어 자동화(시연 리허설·반복 업무) ③ **카카오 Play MCP** = 일정·알림·검색을 카카오 생태계로 묶기.
> 의외의 포인트: 개인 [[카카오-Play-MCP]]·[[schedule-reporter-kakao]]의 알림/발송 자동화는 본업의 알림 업무 감각과도 통한다 — 같은 "결과를 사람에게 푸시" 전략.

## 환경
- **이중 기기 구성** 🧠: ① **Mac** — Claude Cowork 데스크탑 앱·이 sj-wiki 운영·MCP 커넥터 사용(이 페이지 내용). ② **Windows PC** — ai-crawler(`D:\Projects\ai-crawler`)를 Windows Task Scheduler로 자동 실행([[웹-크롤링-기초]]). 즉 위키/대화 작업은 Mac, 크롤링 자동화는 Windows에서 돈다.
- **OS/앱(주 작업)**: macOS + Claude Cowork 데스크탑 앱.
- 정리일 2026-06-09 (이중 기기 명시 2026-06-15).

## 1. MCP 커넥터
### 1-1. 카카오 Play MCP (카카오 공식)
KakaoMap(장소·길찾기) / KakaotalkCal(캘린더·할일) / KakaotalkChat(나에게 메모) / TodoMate(할일·목표) / NaverSearch(뉴스·블로그·쇼핑·데이터랩) / AptInfo(실거래가) / UsStockInfo(미국주식·재무제표) / YouTubeData(영상·자막).
→ **도구 단위 상세는 [[카카오-Play-MCP]]**.

### 1-2. Claude 내장 MCP (Cowork)
| 커넥터 | 역할 |
|---|---|
| `computer-use` | macOS 데스크탑 제어(스크린샷·마우스·키보드) |
| `Claude in Chrome` / `Control Chrome` | 크롬 자동화(DOM·JS)·탭 제어 |
| `workspace (bash)` | Linux 샌드박스 쉘 + web_fetch |
| `cowork` | 파일 관리·Artifact 생성·폴더 접근 |
| `scheduled-tasks` | 예약 작업(cron) 생성·관리 |
| `session-info` | 세션·대화 이력 조회 |
| `mcp-registry` / `plugins` | 커넥터·플러그인 검색·설치 제안 |
| `visualize` | 위젯(SVG/HTML) 인라인 렌더 |

### 1-3. Skills (Cowork)
`docx`·`pdf`·`pptx`·`xlsx`(오피스 문서) / `schedule`(예약 작업) / `skill-creator`·`setup-cowork`.

## 2. 개발/업무 도구 (요약)
- **IDE**: IntelliJ IDEA(주), VS Code(보조). **DB/API**: DBeaver, Postman.
- **브라우저**: Chrome(주, Claude in Chrome 연동), NAVER Whale.
- **협업**: MS Teams·Outlook·Office·OneNote, KakaoTalk(사내 메신저), Zoom.
- 개인 프로젝트 기술 스택 상세는 [[공통-기술스택]] (React19·Vite8·Tailwind4·Supabase).

## 3. 회사 업무 환경
- 회사(사내 AI 챗봇) 업무 환경·플랫폼·프로젝트 기밀 상세는 **PC 전용 `sj-wiki-work` vault**에 분리 보관.

## 🆕 4. 스킬·커넥터 = 공격면 (2026-09-01 추가)

> 🧠 이 절은 [[AI-주간-소식-2026-W36]] (W36-EN4) **SkillSafetyBench**(`arXiv:2605.12015v3`)를 계기로 신설한다. 위 1·2절이 *"무엇을 쓸 수 있나"* 라면, 이 절은 *"그것이 무엇에 손댈 수 있나"* 다.

📄 **논문 인용**: *"**Reusable skills are becoming a common interface for extending LLM agents**, packaging **procedural guidance with access to files, tools, memory, and execution environments**. However, this **modularity introduces attack surfaces**…"* (`raw/ai-digest/2026-09-01.md`, arXiv 섹션 · 8/31 공고)

- 🚨 🧠 **인용된 정의가 위 §1-2·§1-3 목록 그 자체다.** 스킬은 *"절차적 지침 + 파일·도구·메모리·실행환경 접근"* 을 한 덩어리로 묶은 것이고, 모듈성이 곧 공격면이 된다.
- 🚨 📄 **선행 사건이 이미 위키에 있다**: (KR-W35-108) **Claude Code Opus 5 Auto Mode 프롬프트 인젝션 60~80%**([[AI-주간-소식-2026-W35]]) — 🧠 그건 *사건*이었고 SkillSafetyBench는 *그 사건을 재는 자*다.

### ⏳ 접근권 4칸 표 (작성 예정 · 🧠 처방)

🧠 커넥터·스킬마다 아래 4칸을 채우면 **어디가 위험한지**가 목록에서 바로 보인다. ⚠ 아직 실제 권한 범위를 실측하지 않았으므로 **아래는 예시 2행뿐**이고 나머지는 미작성이다(단정 금지).

| 커넥터/스킬 | 파일 | 도구 | 메모리 | 실행 |
|---|---|---|---|---|
| `workspace (bash)` | ○ | ○ | — | **○ (임의 코드)** |
| `Claude in Chrome` | — | ○ | — | ○ (DOM·JS) |
| *(나머지 미작성)* | | | | |

- ✅ **운영 규칙 🧠**: ① **외부 콘텐츠(웹·메일·RSS)를 읽는 경로에서는 Auto Mode를 끈다** — 📄 (KR-W35-108) 근거. ② **커넥터를 늘릴 때마다 공격면이 는다** — 안 쓰는 커넥터는 켜 두지 않는다. ③ 📄 (W36-EN7) **Logos**의 *"capability = tracked inverse를 지닌 컴포넌트"* — 🧠 **되돌릴 수 없는 동작(발송·삭제·결제)** 을 가진 커넥터를 따로 표시한다.
- 🔥 ✅ **[[CLAUDE]] §1과의 층 구분**: 📄 (KR-W36-22) 엑스큐어넷 X-GEN은 *"프롬프트에 **들어가는** 것"* 을 막는다 → §1(기밀 분리)이 그 층이다. 📄 (W36-EN4)는 *"스킬이 **만질 수 있는** 것"* 을 잰다 → 🧠 **스킬 권한 최소화**가 그 층이며, 이 vault엔 아직 없다. ✅ 두 층은 서로를 대체하지 않는다.
- 🧠 **MCP의 학술 명명이 붙었다**: 📄 (W36-EN7) *"cross-process bus"* · (W35-EN37) *"조직 경계를 넘는 에이전트"* · (W36-EN6) *"오프라인 검증 가능한 증거 번들"* — **런타임 조립 → 프로세스 간 버스 → 되돌림 추적 → 증거 번들**이 한 스택의 네 층이다. ⚠ 세 편 모두 초록 잘림본으로 구현 상세는 raw에 **없음**.

## 의외의 연결점
- 🆕 🔥 🚨 **「무기고」 페이지가 곧 「공격면」 페이지다** — 🧠 이 문서는 2026-06-09에 *"내가 손에 쥔 자동화 무기고"* 로 시작했는데, 📄 2026-08~09의 (KR-W35-108)·(W36-EN4)를 지나며 **같은 목록이 위험 목록으로도 읽히게 됐다.** 🧠 늘리는 것과 줄이는 것이 같은 표에서 관리돼야 한다는 뜻이고, ✅ 그래서 §4의 4칸 표를 **§1 목록과 분리하지 않고 붙여 둔다**.
- **scheduled-tasks(cron) ↔ 자동화 정체성**: [[내-프로필]]의 파이썬+크론탭 → [[schedule-reporter-kakao]] → 이 커넥터들로 진화. 같은 본능, 더 강한 도구 → 흐름은 [[에이전트-자동화-도구]].
- **computer-use / Claude in Chrome ↔ 데모 운영**: 화면 전환·반복 작업 리허설을 화면 제어 도구로 자동화/검증할 여지.
- **카카오 채널**: 개인 [[카카오-Play-MCP]](KakaotalkChat·Cal)로 "결과를 카카오로 푸시" — 알림 자동화 직관.
- **NaverSearch datalab(연령·성별 트렌드)**: 타게팅·캠페인 설계 시 트렌드 데이터 활용 발상.

## 관련 문서
- [[카카오-Play-MCP]] · [[공통-기술스택]] · [[에이전트-자동화-도구]] · [[schedule-reporter-kakao]] · [[내-프로필]]
- 🆕 🔥 🚨 [[AI-주간-소식-2026-W36]] — (W36-EN4) SkillSafetyBench(스킬 = 파일·도구·메모리·실행 접근 = 공격면) · (W36-EN7) Logos(cross-process bus · tracked inverse) · (W36-EN6) 오프라인 검증 가능한 증거 번들
- 🆕 🚨 [[AI-주간-소식-2026-W35]] — (KR-W35-108) Claude Code Opus 5 Auto Mode 프롬프트 인젝션 60~80% · (W35-EN37) 조직 경계를 넘는 에이전트 위험 프레임워크
- 🆕 [[CLAUDE]] — §1(입력 차단)과 스킬 권한 최소화(실행 제한)는 **다른 층**이며 서로를 대체하지 않는다
