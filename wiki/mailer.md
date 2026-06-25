---
title: CS SmartHub (mailer)
category: 프로젝트
tags: [프로젝트, 풀스택, 포트폴리오, cs자동화, express, nodemailer, supabase, grafana]
source: "사내 git 저장소 (live), 사용자 확인 2026-06-10 / 저장소 재확인 2026-06-25"
status: 진행중
flagship: true
created: 2026-06-09
updated: 2026-06-25
---

> [!tip] 핵심 takeaway (포트폴리오 관점)
> ⭐ **[[내-프로필]]의 "비개발→개발 전환"을 증명하는 1순위 포트폴리오 프로젝트.** 단순 사이드가 아니라 **본인이 직접 기획하고, 실제 사용자(사내 CS팀)의 요구사항을 받아 개발·운영 중인** 풀스택 사내 도구다.
> 포트폴리오에서 팔 포인트: ① **기획+개발 1인 풀스택** ② **실사용자 기반**(요구사항 수집→반영 사이클) ③ **지속 개발**(179 커밋·약 3개월·현재진행) ④ "메일 발송"을 넘어 **CS 업무 자동화 허브**(Mailer+Grafana 리포트+Chatbot)로 확장 ⑤ **LLM(Gemini) 로그 분석·Playwright 챗봇 모니터링** 등 최신 자동화 스택 적용.
> ⚠️ 개발 시 주의: `supabase db push` 금지 (아래 '마이그레이션 규칙').

## 한 줄 소개
사내 **CS팀의 반복 업무를 자동화하는 통합 허브** (CS SmartHub). 메일 발송 자동화 + 모니터링 리포트 자동 발송 + 챗봇 관리를 한 곳에서.

## 문제 / 배경 📄(사용자)
- **CS팀 ≠ 단순 고객응대.** 실제 업무 범위: 솔루션 가이드 제작 · 솔루션 신버전 테스트 · 버그 리포팅 · **서버·서비스 모니터링** · 신제품 요구사항 정리 및 버그 테스트 · **해외사업 전반**.
- 그런데 **팀원이 4명뿐** → 만성 인력 부족. 박상준은 이 **CS팀을 돕는 포지션**으로 배치됨([[내-프로필]]).
- 그래서 업무 효율화용 웹 프로그램을 하나씩 만들어 제공하다, 이를 **하나로 통합한 솔루션**으로 키운 것이 CS SmartHub다(= 이 프로젝트의 기원·목적).
- 뿌리: [[내-프로필]]의 과거 "파이썬+크론탭+메일 보고서" 자동화 경험을 팀이 직접 쓰는 웹 도구로 발전.

## 내 역할 📄(사용자)
- **기획**: 본인이 직접 기획.
- **사용자 리서치**: 실제 사용자(사내 CS팀)에게 요구사항을 수집해 반영.
- **개발/운영**: 프론트+백엔드+배포까지 1인 풀스택. 지속 개발 중.

## 주요 기능 📄(저장소 구조 기준)
화면(Page) = 기능 단위. 통합 진입점은 **Hub**.
- **Hub** (`HubPage`): 기능 통합 대시보드.
- **Mailer** (`MailerPage`): 메일 발송 **작업(Job)** 관리 + **발신자(Sender)** 관리 + 태그(`JobCard`·`JobModal`·`SenderModal`·`TagInput`). Nodemailer/SMTP 발송.
  - 📄 **임팩트**: 기존엔 수 분마다 반복적으로 메일을 보내고 확인하느라 **CS팀 4명 전원이 30분~1시간씩 메일 발송에만 매달림** → 자동 발송으로 전환해 **투입 인력 0**.
- **Grafana 리포트** (`GrafanaPage`): **Elasticsearch/Prometheus 쿼리 → 리포트 생성 → 이메일 자동 발송**. 스케줄링(`schedule`)·설정(`settings`, 로그 ingestion-lag 보정·KST)·이메일 템플릿(`email`).
  - 📄 **임팩트**: 기존엔 매일 아침 ES 쿼리를 메모장에 모아두고 하나씩 날려 **4명이 각자 10~20분씩** 모니터링 → 주요 정보를 **매일 아침 메일로 자동 수신**, 아침 루틴이 '메일 확인'으로 축소.
  - 📄 **쿼리 UI 관리** (2026-06-17~, `server/grafana/config.js`→DB): 하드코딩됐던 메트릭/로그쿼리를 Supabase JSONB로 옮겨 **설정 탭에서 추가/수정/삭제 + enabled 토글**(`QueryListEditor`). **테스트(실호출) 통과해야 등록**(`POST /test-query`). 코드 배포 없이 모니터링 대상 변경. → 🧠 운영자(CS팀)가 직접 모니터링 항목을 늘릴 수 있게 됨.
  - 📄 **LLM(Gemini) 로그 분석** (2026-06-24~, `server/grafana/analyze.js`): 앱별 ERROR 로그를 Gemini가 분석해 중복 정리 + "솔루션에서 확인할 포인트" 요약 → 메일·웹 표시(`AiSummary`). best-effort(실패해도 리포트 정상).
  - 📄 **영속 로그 유형** (`LogTypesTab`): LLM이 정리한 유형을 DB에 누적 저장(유형별 노트·회차별 로그·발생 타임라인). 2026-06-25에 **개별 로그(occurrence) 정규화 저장**으로 전환 — LLM은 분류만, 시각·메시지는 ES 원본 그대로 보존(`grafana_log_entries`)해 모든 발생 시각을 손실 없이 기록.
- **Chatbot 모니터링** (`ChatbotPage` + `routes/chatbot`): 📄 로컬 `monitor_link.sh`(단일 봇 curl) 대체. **여러 챗봇 등록 → 하루 1회 GitHub Actions에서 Playwright로 실제 사용자처럼 접속·발화·응답 확인 → 실패 시 메일**(`scripts/chatbot-check.mjs`). 시나리오 스텝 타입(발화/버튼 클릭), iframe 포함 전체 프레임 탐색, 카테고리 필터(봇당 단일 카테고리)로 그룹 단위 부분 실행, 허브에서 수동 실행 버튼.
  - 📄 **정시 트리거**: Supabase **pg_cron(08:30 KST)** 이 `/api/chatbot/dispatch`를 호출해 워크플로우를 일으킨다. (GH `on:schedule`은 ~2h 지연 실측되어 제거.)
- **인증** (`LoginPage`): 로그인(세션 쿠키, 현재 100일 유지).
  - 📄 **이중 인증 체계**: 사람 요청은 `auth`(`x-app-password` 헤더, 앱 비밀번호 게이트), 머신 요청(pg_cron·grafana tick·chatbot dispatch)은 `cronAuth`(`Bearer CRON_SECRET`). → 🧠 사용자용·자동화용 인증을 분리해 정시 트리거·외부 dispatch를 비밀로 보호.

## 기술 스택 📄
[[공통-기술스택]](React19/Vite8/Tailwind4) +
- **백엔드**: Express.js (`server/`), Nodemailer/SMTP, Supabase([[parking]], pg_cron 포함)
- **Grafana 연동**: Elasticsearch/Prometheus 클라이언트(`server/grafana/client.js`), 리포트/스케줄/이메일/분석 모듈
- **LLM**: Google [[Gemini]] (`@google/generative-ai`, 기본 `gemini-2.5-flash`) — 로그 분석 요약(best-effort). 키는 `<redacted>`(.env+Vercel).
- **브라우저 자동화**: [[Playwright]] (챗봇 시나리오 체크, GitHub Actions에서 실행)
- **UI**: @dnd-kit(드래그), cmdk(Cmd+K 팔레트), sonner(토스트), lucide-react, Pretendard + 디자인 토큰(@theme)
- **테스트**: vitest, @testing-library/react, supertest, jsdom (`*.test.js`)
- **배포**: Vercel (`vercel.json`, `api/index.js`), [[GitHub Actions]](챗봇 체크 워크플로우)
- 실행: `npm run dev` = vite + Express 동시(concurrently)

## 진행 현황 📄(git, 2026-06-25 기준)
- **규모**: 총 **179 커밋**. 기간 **2026-03-27 ~ 2026-06-25** (약 3개월, 현재진행). 2026-06-09 이후 **+80커밋**.
- **상태**: 🔄 활발히 개발 중. 패키지 `cs-smarthub` v0.1.0.
- **개발 방식** 🧠: spec→plan→TDD(superpowers) + 브랜치-퍼-태스크 + PR 단위 머지(현재 PR #20대). 설계/계획 문서가 `docs/superpowers/specs·plans`에 누적됨.
- **2026-06-09 이후 큰 흐름**(저장소 📄):
  - **NOC(관제 콘솔) 리디자인**: 디자인 토큰(@theme)+Pretendard, 아이콘 레일, Cmd+K 팔레트, 컴팩트 행 리스트, 하트비트 바, send_log 발송 이력, 토스트/확인 다이얼로그, 모바일 반응형.
  - **Chatbot 모니터링 신설**: Playwright 시나리오 체크 + GitHub Actions + pg_cron 정시 트리거 + 스텝 타입(발화/버튼) + 카테고리 그룹 실행.
  - **Grafana 쿼리 UI 관리**: 하드코딩 쿼리 → DB(JSONB) + 설정 UI + 테스트 게이트.
  - **Grafana LLM 로그 분석**: Gemini 요약 + 영속 로그 유형 + 개별 발생 시각 보존(occurrence 정규화).
- **DB 스키마 진화** 📄(Supabase 마이그레이션 이력): `add_send_log`(06-10) → `add_chatbot_monitoring`(chatbots/check_log/settings) → `add_grafana_queries`(metrics·log_queries JSONB, 06-17) → `add_chatbot_category`(+list, 06-22) → `add_grafana_log_types`(+runs·last_analysis 캐시, 06-24) → `add_grafana_log_entries`(occurrence 보존, 06-25) → `add_grafana_log_type_run_note`(회차 메모, 06-25). → 🧠 기능 추가가 곧 스키마 마이그레이션으로 기록돼 반복적 스키마 진화를 추적 가능(`db push` 금지·멱등 SQL 적용은 아래 규칙).

## 화면 (스크린샷)
> 이미지는 `raw/assets/`에 두고 `![[파일명]]`으로 임베드한다. 파일명 규칙: `cs-smarthub_<무엇>[_YYYYMMDD].png` (공백 X, 소문자·하이픈).
> 각 이미지 아래 *이탤릭 캡션*으로 무슨 화면인지 1줄. 포트폴리오에 그대로 쓸 수 있게 기능별로 묶는다.

_(아직 없음 — 스크린샷을 `raw/assets/`에 넣고 알려주면 캡션과 함께 기능별로 배치합니다.)_

<!-- 배치 예시:
### Mailer — 발송 작업 목록
![[cs-smarthub_mailer-jobs.png]]
*메일 발송 작업(Job)을 카드로 관리하는 화면.*

### Grafana 리포트 — 자동 발송 이메일
![[cs-smarthub_grafana-report-email.png]]
*매일 아침 자동 수신되는 모니터링 리포트 메일.*
-->

## 진행사항 업데이트 로그 (누적)
> "프로젝트 업데이트" 요청 시 라이브 저장소를 확인해 여기에 최신순으로 추가한다.
- **2026-06-10**: 포트폴리오용 정리 + 라이브 저장소 기준 초기 진행현황 기록(99커밋, Hub/Mailer/Grafana/Chatbot/Auth 기능 파악).
- **2026-06-10**: 📄(사용자) CS팀 배경·프로젝트 기원·**정량 임팩트**(메일 인력 0화, 아침 모니터링 축소) 보강. 문제/배경·기능 임팩트·포트폴리오 STAR 갱신.
- **2026-06-25** (후속 보강): 📄 raw 재점검 중 위키에 빠진 구체 사실 2건 보강 — ① **이중 인증 체계**(`auth` x-app-password / `cronAuth` Bearer CRON_SECRET) ② **Supabase 마이그레이션 이력**(send_log→chatbot_monitoring→grafana_queries→chatbot_category→grafana_log_types→grafana_log_entries→run_note)로 스키마 진화 추적성 추가.
- **2026-06-25**: 📄 라이브 저장소 재확인(99→**179커밋**, +80). 2026-06-10 이후 4개 큰 작업 반영 — ① **NOC 관제 콘솔 리디자인**(디자인 토큰·아이콘 레일·Cmd+K·하트비트 바·send_log) ② **Chatbot 모니터링 신설**(Playwright+GitHub Actions+pg_cron 정시 트리거, 스텝 타입, 카테고리 그룹 실행) ③ **Grafana 쿼리 UI 관리**(하드코딩→DB JSONB + 테스트 게이트) ④ **Grafana LLM(Gemini) 로그 분석 + 영속 로그 유형**(개별 발생 시각 보존). 기술 스택에 Gemini·Playwright·GitHub Actions·cmdk/sonner 추가.

## ⚠️ 마이그레이션 규칙 (중요)
- **`supabase db push` 금지.** 마이그레이션은 **Supabase SQL Editor에서 멱등(idempotent) SQL로 직접 적용**.
- 이유: 로컬 마이그레이션 이력과 원격 DB 상태 divergence → `db push`가 충돌·덮어쓰기 유발.
- [[parking]] 일반 절차(`supabase db push`)와 상충하므로 mailer엔 이 예외가 우선.

## 포트폴리오 활용 포인트 🧠
- **STAR 소재 (정량 임팩트 확보됨)**:
  - 상황(S): 4명뿐인 CS팀이 광범위한 업무 + 반복 수작업(메일 발송·아침 모니터링)에 매몰.
  - 과제(T): 반복 업무를 자동화해 인력을 본질 업무로 돌리기.
  - 행동(A): 직접 기획 + 사용자(CS팀) 요구사항 수집·반영 + 풀스택 개발/운영 + 개별 도구를 통합 솔루션화.
  - 결과(R): 📄 메일 발송 **투입 인력 0화**, 아침 모니터링 **4명×10~20분 → 메일 확인**으로 축소.
- **차별점**: 토이가 아니라 **실사용자·실운영·지속개발**(179커밋, 약 3개월+).
- 🧠 **최신 기술 어필 포인트**(2026-06 신규): **LLM(Gemini)로 운영 로그 자동 분석·요약**, **Playwright로 챗봇을 실사용자처럼 시나리오 점검**, **pg_cron으로 정시 트리거 신뢰성 확보**(GH on:schedule 지연 문제를 진단해 우회) — "단순 자동화"를 넘어 LLMOps/E2E 모니터링까지 다룬 사례로 어필 가능.
- 🧠 더 채우면 좋을 것: 절감 시간의 **월/연 환산 수치**, 대표 기능 스크린샷·아키텍처 다이어그램, 회고(가장 어려웠던 기술 난제→해결: 예) on:schedule 지연 진단→pg_cron 전환, LLM 시각 누락→ES 원본 보존 설계).

## 관련 문서
- [[프로젝트-포트폴리오]] · [[schedule-reporter-kakao]](형제 프로젝트, CORS로 연동) · [[parking]] · [[공통-기술스택]] · [[에이전트-자동화-도구]] · [[내-프로필]]
- 기술: [[Gemini]] · [[Playwright]] · [[GitHub Actions]]
