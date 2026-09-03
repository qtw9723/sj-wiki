---
title: Delivery SmartHub (delivery-smarthub)
category: 프로젝트
tags: [프로젝트, 풀스택, 포트폴리오, 자동화, 멀티허브, express, supabase, playwright]
source: "라이브 저장소 github.com/qtw9723/delivery-smarthub (private), 신규 구축 세션 2026-07-21"
status: 진행중
created: 2026-07-21
updated: 2026-07-21
---

> [!tip] 핵심 takeaway (포트폴리오 관점)
> ⭐ **[[mailer|CS SmartHub]]의 "팀 자동화 허브" 패턴을 재사용해 delivery팀용으로 확장한 형제 프로젝트.** 단순 복제가 아니라 **멀티허브 플랫폼 + 중앙 백오피스**로 한 단계 추상화를 올린 게 팔 포인트다.
> 어필 포인트: ① **검증된 모듈(챗봇 모니터링)을 재사용**하되 `hub_id` 구분 컬럼으로 **멀티테넌트화** ② **라이브 서비스(cs)를 전혀 건드리지 않고** 같은 Supabase에 신규 테이블을 병렬로 세워 안전하게 확장(무중단·무위험 마이그레이션 설계) ③ **여러 팀 허브를 한 곳에서 관리하는 중앙 백오피스** 신설 ④ 브레인스토밍→스펙→계획→TDD 프로세스로 하루 만에 Phase1 완주(테스트 82개·E2E 통과).
> ⚠️ 개발 시 불변 원칙: **cs 라이브 테이블/배포/크론 무접근**, DB는 Management API 멱등 SQL만(`db push` 금지 — [[mailer]]와 동일).

## 한 줄 소개
**Delivery팀 전용 자동화 통합 플랫폼.** [[mailer|CS SmartHub]]의 형제 격으로, 챗봇 모니터링을 첫 공유 모듈로 시작해 delivery 고유 기능을 점차 추가하며, 여러 팀 허브(CS·Delivery·…)를 한 곳에서 보는 **중앙 백오피스**를 둔다.

## 문제 / 배경 📄(사용자·2026-07-21 세션)
- [[mailer|CS SmartHub]]가 CS팀 자동화 허브로 자리잡자, **delivery팀도 같은 방식의 통합 도구**가 필요해졌다.
- delivery팀이 쓸 기능을 앞으로 하나씩 붙일 예정이고, **중간에서 전체를 관리할 백오피스**가 필요하다.
- 즉 "cs와 비슷하지만 다른 프로젝트" — 같은 모듈(챗봇 모니터링)은 재사용하되, DB는 분리하거나 조회 조건 컬럼으로 구분되면 좋겠다는 요구.

## 핵심 설계 결정 📄(사용자 확정, 2026-07-21)
- **멀티허브 플랫폼 지향**: 백오피스가 관리하는 "전체" = 여러 팀 허브 중앙 관리(cs·delivery·향후 팀).
- **cs는 나중 온보딩**: delivery 허브 + 백오피스를 먼저 만들고, 라이브 cs는 지금 건드리지 않는다.
- **코드 (A1)**: 새 단독 레포. [[mailer]] 스택([[공통-기술스택]]+Express)을 복사·프루닝(grafana/mailer 모듈 제거)하고 챗봇 모듈만 허브화해 이식.
- **DB (B2 변형)**: [[mailer]]와 **동일한 Supabase 프로젝트**를 재사용하되 **cs 라이브 테이블 무접근**. 허브 인식 신규 테이블을 **병렬로 파서** 그 위에서만 동작·테스트하고, 검증 후 cs 데이터를 이관(온보딩)한다.

## 주요 기능 📄(저장소 구조 기준)
- **챗봇 모니터링** (`ChatbotPage` + `routes/chatbot`): [[mailer]]의 Playwright 시나리오 체크 모듈을 **허브 인식으로 이식**. 모든 쿼리에 `hub_id` 스코프, 러너는 `HUB_KEY`(기본 delivery)로 대상 허브만 체크. 실패 시 허브별 수신자에게 메일.
- **중앙 백오피스** (`AdminPage` + `routes/admin`, `/admin`): 🆕 delivery-smarthub의 핵심 신규 기능.
  - **허브 관리**: 허브 목록/추가/활성화 토글(`hubs` 레지스트리).
  - **크로스 허브 현황**(`GET /api/admin/overview`): 모든 허브의 챗봇·최근 체크 상태를 한 화면에서 집계.
  - **허브별 설정**: 수신자·카테고리 편집.
- **인증** (`LoginPage`): [[mailer]]와 동일한 앱 비밀번호 게이트(`x-app-password`), 머신 트리거는 `Bearer CRON_SECRET`.

## 데이터 모델 📄(허브 인식 신규 테이블)
같은 Supabase 프로젝트(ref `enawzdqroidrhtjqhpka`, [[parking]])에 cs 테이블과 **이름 충돌 없이** 병렬 생성:
- `hubs` — 허브 레지스트리(`key`: delivery/cs/…, name, enabled). delivery 시드.
- `hub_chatbots` — 챗봇 + **`hub_id` (조회 조건 컬럼)**. scenario/input_selector/category/enabled 계승.
- `hub_chatbot_check_log` — 체크 이력(hub_id 비정규화 포함).
- `hub_chatbot_settings` — **허브당 1행**(cs의 싱글톤 `id=1` 방식을 hub_id PK로 진화).
- 전 테이블 RLS ENABLE(서버 service_role 전용, anon 정책 없음). → [[Supabase-RLS-정책]] 규약 준수.

## 기술 스택 📄
[[공통-기술스택]](React19/Vite8/Tailwind4) +
- **백엔드**: Express.js (`server/`), Nodemailer/SMTP, Supabase([[parking]])
- **브라우저 자동화**: [[Playwright]] (챗봇 시나리오 체크, [[GitHub Actions]]에서 실행)
- **UI**: cmdk(Cmd+K), sonner(토스트), lucide-react
- **테스트**: vitest + supertest (82개 통과)
- **배포**: Vercel(`vercel.json`, `api/index.js`) — **Phase1은 미배포**(private 레포만)
- 실행: `npm run dev` = vite + Express 동시(concurrently)

> ⚠️ **이 페이지 본문은 2026-07-21(Phase1) 시점에서 멈춰 있다.** 이후 SmartHub 통합
> 플랫폼으로 재설계·배포되고 CS 컷오버까지 끝나(모듈 5종·허브 2개·크론 4잡) 아래 "진행 현황"
> 절의 상태·스택 서술은 낡았다. **현재 상태의 출처는 저장소의 `README.md`·`ROADMAP.md`·
> `docs/deploy-notes.md`다.** 본문 전면 갱신은 별도 "프로젝트 업데이트" 작업으로 남는다
> (아래 업데이트 로그는 최신).

## 진행 현황 📄(2026-07-21 기준 — 낡음)
- **상태**: 🔄 Phase1 구축 완료. 패키지 `delivery-smarthub` v0.1.0. private 레포 푸시(commit `1ecc864`).
- **개발 방식** 🧠: 브레인스토밍(superpowers)→스펙→계획→인라인 구현→검증. 문서가 `docs/superpowers/specs·plans`에 누적, `docs/deploy-notes.md`에 배포 절차 문서화(미실행).
- **검증**: 테스트 82개 통과, `npm run build` 통과, **실 API E2E 스모크**(봇 생성→admin overview 노출→삭제→401) 통과. **cs 데이터 무변경 확인**(chatbots 10행·로그 259행 그대로).

## 진행사항 업데이트 로그 (누적)
> "프로젝트 업데이트" 요청 시 라이브 저장소를 확인해 여기에 최신순으로 추가한다.
- **2026-09-03**: **허브 기본 잠금 + CI 신설·상류 감시**(PR #11·#12·#13). 허브가 공개가 되는 세 갈래(생성 / 공개 허브에 비용 모듈 켜기 / 비밀번호 해제)에 각각 확인을 걸어 v0.3.0 완료. 이어서 백로그의 "패리티 가드 CI화"를 하려다 두 가지를 더 발견 — 🔴 **이 저장소엔 자동 검증이 아예 없었고**(push·PR에서 테스트·lint·빌드 무실행), 🔴 **패리티 가드 자체가 Cogi 작업 트리를 읽어 흔들렸다**(한 세션에 상류 HEAD가 세 번 움직여 우리 코드 그대로인데 빨강↔초록). CI 신설 + 가드를 고정 커밋 기준으로 + 드리프트 알람 분리(매일) + "조용한 스킵을 실패로". 그리고 **신설한 CI가 첫 실행에서 실제 버그를 잡았다** — 첨부 스토리지 클라이언트가 모듈 로드 시점에 초기화돼 설정값이 없으면 메일 잡 편집 화면 전체가 죽는 구조였고(로컬에선 .env 때문에 안 보였다), 지연 초기화로 고쳤다. main CI 초록.
  - 후속: Cogi가 private이라 상류 감시에는 저장소 시크릿 `COGI_TOKEN`(repo 읽기 PAT)이 필요하다.
- **2026-09-02**: **doc-to-api 비용 노출 차단 + 백오피스 위험 경고**(PR #7·#9). 외부 비용(Cogi 청구 gpt-4o)이 걸린 유일한 경로가 허브 비밀번호만 검사해, 공개 허브에서는 기능을 켠 적 없어도 무인증 호출이 통과했다(전날 실측 `?hub=cs` 200). 관문을 둘 더 세움 — 기능 활성 확인(`hub_features`, 마스터키도 불통과) + 허브별 시간당 호출 상한(`hub_module_calls` 신규 테이블, 서버리스라 카운터를 DB에·DB 무응답이면 fail-closed). 백오피스는 "공개 허브 + 비용 모듈" 조합을 빨간 배너·카드 경고·칩으로 표시(위험 모듈은 레지스트리의 `externalCost` 플래그에서). 프로덕션 검증: cs 404·마스터키 404·delivery 200·기록 1행. 테스트 +35.
  - 부수 발견 🔴: **doc-to-esd가 상류(Cogi) QA 수정 12건을 못 받은 채 3주 방치**됐다(`cogiParity` 가드 2건 실패가 그 증거). **중복·빈 헤더 열에서 데이터 소실**이 포함돼 있어 로드맵 v0.2.0 항목5로 등재(PR #8). 가드가 로컬에서만 돌아 아무도 몰랐던 것이 근본 문제 → CI화가 후속.
- **2026-07-21**: 신규 구축. 요구(delivery팀 자동화 플랫폼·챗봇 모듈 재사용·중앙 백오피스) → 3개 결정질문으로 아키텍처 확정(멀티허브·cs 나중 온보딩·A1+B2변형) → Phase1 완주(챗봇 모듈 허브화 + 중앙 백오피스 + hub_* 신규 테이블). private 레포 생성·푸시.

## ⚠️ 불변 원칙 (cs 무접근)
- cs 라이브 테이블 `chatbots`/`chatbot_check_log`/`chatbot_monitor_settings` **읽기·쓰기 전면 금지.** 오직 `hub_*`만.
- cs의 Vercel·pg_cron 잡(jobid 8)·GitHub Actions **변경 금지.**
- DB는 Management API 멱등 SQL만(`supabase db push` 금지 — [[mailer]] 규칙과 동일, [[parking]] 일반 절차의 예외).

## 후속 (Phase1 아님) 🧠
1. **cs 온보딩**: `hub_*` 검증 후 cs 데이터를 `hub_chatbots`(hub=cs)로 이관하는 멱등 마이그레이션 → 백오피스에 cs 허브 자동 등장 → (옵션) cs 앱도 신규 테이블 소비.
2. **배포·pg_cron 실등록**: 신규 Vercel 프로젝트 + cs와 별개의 새 pg_cron 잡(`docs/deploy-notes.md`, 사용자 확인 후).
3. **delivery 고유 기능** 추가.

## 포트폴리오 활용 포인트 🧠
- **STAR 소재**: (S) cs 허브 성공 → delivery팀도 필요 (T) 검증된 모듈 재사용하되 라이브 무중단 (A) 멀티허브 스키마 설계 + 신규 테이블 병렬 + 중앙 백오피스 (R) 하루 만에 Phase1·테스트 82개·cs 무영향 검증.
- **차별점**: [[mailer]]가 "단일 팀 도구"라면 delivery-smarthub는 **플랫폼화(멀티테넌트 + 중앙 관리)** 로의 진화 → 아키텍처 사고를 보여주는 소재.
- 🧠 더 채우면 좋을 것: 배포 후 스크린샷(백오피스 크로스 허브 뷰), cs 온보딩 마이그레이션 회고, "왜 별도 레포 + 같은 DB"였는지 트레이드오프 설명.

## 관련 문서
- [[delivery-smarthub-링크]] — 저장소·문서 링크 모음
- [[mailer|CS SmartHub]](모듈·스택을 물려준 형제·기원) · [[프로젝트-포트폴리오]] · [[공통-기술스택]] · [[parking]](공유 Supabase) · [[내-프로필]]
- 기술: [[Playwright]] · [[GitHub Actions]]
