---
title: Cogi-POC-Generator (Dialog JSON Generator)
category: 프로젝트
tags: [프로젝트, 챗봇, 시나리오, dialog-json, llm, openai, supabase, 핵심]
source: raw/projects/cogi-poc-generator-v1.md
created: 2026-06-09
updated: 2026-06-25
---

> [!tip] 핵심 takeaway
> ⭐ **[[내-프로필]]의 "LLM 활용 챗봇 시나리오 구성 툴"이 이제 실체를 넘어 풀스택 제품으로 컸다.** 단순 JSON 생성기였던 게 → **LLM 다단계 생성 파이프라인 + 데이터구동 규칙엔진 + 학습 레퍼런스 라이브러리 + 테스터 인증/승인**까지 갖춘 사내 POC 제품이 됐다.
> 포트폴리오 관점에서 자랑할 축이 3개: (1) **프롬프트 엔지니어링·LLM 오케스트레이션**(6단계 생성, closed-world 검증, 토큰/비용 집계), (2) **하드코딩 대신 DB-구동 규칙 설계**(solution_rules가 SoT — 운영자가 코드 없이 규칙 조정), (3) **풀스택 운영**(인증/승인 게이트·신뢰기기 로그인·어드민 8탭). 챗봇 도메인 지식 + 풀스택 + LLM이 한 프로젝트에 다 들어왔다.

## 개요
- 📄 설명: Cogi **Dialog JSON Generator** — 챗봇 대화 시나리오(플로우)를 LLM으로 생성하는 POC 제너레이터 + 학습/관리 어드민. (`README.md`)
- 📄 유형: **풀스택**. 프론트(React SPA) + Supabase Edge Functions(Deno) 백엔드 + Postgres. 버전 1.0.1.
- 📄 생성 흐름: 사용자가 레퍼런스 선택 → 맞춤 질문(설문) 응답 → 학습된 템플릿/규칙 기반으로 Cogi Dialog JSON 생성 → 결과 저장·다운로드. (`README.md`)
- 🧠 2026-06-09 위키 작성 시점엔 "배포 준비된 프론트 POC"였으나, 2주간 ~200커밋으로 **백엔드·LLM 파이프라인·인증이 본격화된 제품**이 됐다.

## 주요 기능
- 📄 **LLM 다단계 생성 파이프라인** (`supabase/functions/cogi-generator`): designFlow → expandWithSpecs → fillNodeValues(2.5) → deriveEsdSchemas → deriveApiDefs(2.6) → output 멘트 패스. 단계마다 검증·재시도.
- 📄 **데이터구동 규칙 엔진**: 생성 규칙을 코드에 박지 않고 `solution_rules`(DB, 7 카테고리)에 두고 단계별 프롬프트에 주입. 어드민 또는 레퍼런스 학습으로 규칙 추가. (`CLAUDE.md`)
- 📄 **레퍼런스 학습**: `derive-node-specs`(결정론적 노드 추출 → LLM 일반화 → closed-world 검증), `learn-rules`(레퍼런스 JSON 구조 학습). (`supabase/functions/`)
- 📄 **시나리오 레퍼런스 라이브러리** (`/scenarios`, `cogi_scenario_references`): 산업군별(금융/물류/소매/도매/의료/기타) 미니봇 학습자료. Stage1 few-shot 예시로 주입 + 사용자 단일선택/조립.
- 📄 **API 레퍼런스 라이브러리** (`cogi_api_references`): import용 API 정의 관리(엔드포인트당 1행) + 어드민에서 실제 호출 test(프록시).
- 📄 **테스터 인증·승인** (`testers`, `trusted-device`): 이메일 OTP 로그인 → 승인 게이트(pending→approved) → 계정별 결과(RLS) → 신뢰기기 등록 후 이메일만으로 재로그인(30일).
- 📄 **LLM 토큰 사용량·예상비용 집계·표시** (`flow/usage.ts`).
- 📄 **사용자 피드백**: 플로팅 버튼 → 우측하단 팝오버, 어드민 피드백 관리 탭(미완료 배지).
- 📄 어드민 8탭: questions / references / templates / solution-rules / rules / scenario-references / api-references / feedback / testers.

## 기술 스택
[[공통-기술스택]] 기반 + 풀스택 확장:
- 📄 **프론트**: React 19.2, Vite 8, React Router 7, Tailwind CSS 4, Radix UI + shadcn, lucide-react. 폼/검증 = react-hook-form + **zod**(Dialog JSON 구조 검증의 핵심).
- 📄 **백엔드**: Supabase Edge Functions(Deno/TypeScript) 20개, Postgres(40 마이그레이션, RLS). ([[parking]])
- 📄 **LLM**: **OpenAI `gpt-4o`** (temperature 0.1). ⚠ GEMINI는 mailer/grafana용이고 Cogi와 무관(혼동 금지).
- 📄 **배포**: 프론트 Vercel(main 푸시 자동), 엣지함수 `supabase functions deploy`, DB `supabase db push`.

## 아키텍처
- 🧠 **3계층**: React SPA(설문·결과·라이브러리·어드민) ↔ Supabase Edge Functions(생성·학습·CRUD·인증) ↔ Postgres(규칙·레퍼런스·결과·테스터). LLM 호출은 전부 엣지함수 안에서만(키 노출 차단).
- 📄 **Flow 1급화**: Stage1 LLM이 플로우를 *설계*(FlowSpec)하고 reachability 검증·repair, Stage2가 노드에디터 JSON으로 *결정론적 전개*. 과거의 "통째 JSON을 LLM이 뱉는" 경로는 제거 — 🧠 LLM은 설계만, 구조 정합성은 코드가 보장하는 **하이브리드(LLM+결정론)** 패턴.
- 📄 **규칙 = 데이터, 로직 = 코드**: 7개 규칙 카테고리가 생성 단계(flow/config/output/condition)에 매핑돼 주입. 단 결정론적 안전장치(루트 stack 제거, 변수 use-before-declare 차단 등)는 코드에 잔존. (`CLAUDE.md`)
- 📄 **레퍼런스 일원화**: 2026-06-16 `features` 레이어 제거 → 레퍼런스 중심으로 통합. 2026-06-17 레거시 값-할당 3탭(필드스키마/조건패턴/값할당) 제거.

## 진행 현황 (2026-06-25)
- 🧠 **상태: 사내 테스터 대상 POC 운영 단계.** 생성 파이프라인·규칙엔진·레퍼런스 학습·인증/승인이 모두 갖춰져, 코드 없이 어드민에서 규칙·시나리오·API를 학습/관리하는 형태로 성숙.
- 🧠 남은 결: 규칙·학습자료를 카테고리별로 하나씩 채워가는 운영형 작업(시나리오 레퍼런스 → API 레퍼런스 순으로 진행 중), 폼 도움말 등 UX 다듬기.

## 진행사항 업데이트 로그
### 2026-06-25 — 2주간(2026-06-09~) ~200커밋, POC가 풀스택 제품으로 (📄 git log)
- **Flow 단계 1급화**: Stage1 LLM 플로우 설계 → Stage2 결정론적 JSON 전개. legacy 전체-JSON 경로 제거, reachability 검증·repair·다중 루트 지원.
- **레퍼런스→노드스펙 파생**(derive-node-specs, closed-world 검증) + 판별 유니온 variant 다중 선택.
- **질문 유형 시스템**: group_list/select/multi_select 중첩 입력 UI, 봇 정체성 질문(intent) seed.
- **레거시 정리**: features 레이어 + 값-할당 3탭 제거(레퍼런스로 일원화).
- **생성 신뢰성**: STAGE 2.5 값 채우기·재시도, ESD 스키마 동시생성, output 멘트 전담패스(말투·재시도), 변수 `${}` 보간, use-before-declare 차단, 시스템 식별자 난수생성, Pre/Post Dialog 항상 포함.
- **토큰/비용 집계** 표시 추가.
- **data-driven 규칙**: solution_rules가 source-of-truth로 전환, "규칙은 어드민/학습으로 관리" 원칙 확립.
- **시나리오 레퍼런스 라이브러리**(few-shot 주입 + 단일/조립 + `/scenarios`).
- **API 레퍼런스 라이브러리**(CRUD + 실호출 test + 시나리오에서 직접 입력/매핑).
- **테스터 인증 전면 도입**: 이메일 OTP + 승인 게이트 + 계정별 결과(RLS) + 신뢰기기 이메일-only 로그인 + 어드민 테스터 관리(승인/차단/삭제).
- **사용자 피드백**(팝오버 + 미완료 배지), 폼 도움말/툴팁 보강.
- 🧠 메모리 노트와 일치: 시나리오 값 생성(PR#3·4), 시나리오 레퍼런스(PR#30), API 레퍼런스(PR#34), 테스터 인증(PR#38), 커스텀 SMTP 모두 반영됨.

### 2026-06-09 — 최초 위키화
- 프론트 POC(Dialog JSON 생성 + Supabase + zod 검증) 상태로 정리.

## 왜 중요한가 (챗봇 도메인 ↔ 개발)
- 🧠 "Dialog JSON" = 챗봇 대화 흐름 정의 포맷. 이걸 LLM으로 생성·검증하는 도구라는 점에서, 회사 **챗봇 시나리오 구성**을 자동화/도구화한 결과물.
- 🧠 LLM이 *설계*하고 zod/closed-world 검증이 *구조를 강제*하는 구조 → **LLM 환각 방지의 정석 파이프라인**을 실전에서 구현한 사례(포트폴리오로 강력).

## 의외의 연결점 (🧠 판단 영역)
- ⭐ **회사 업무와 직결**: 이 도구가 만드는 Dialog JSON = 회사에서 손으로 짜던 챗봇 시나리오와 같은 산출물. 개인 도구로 본업을 가속하는 지점. (회사 내부 상세는 PC 전용 `sj-wiki-work` vault)
- **규칙=데이터 설계**는 다른 프로젝트에도 이식 가능한 패턴 — [[mailer]]의 운영 규칙류도 같은 식으로 DB-구동화하면 비개발자(CS팀)가 직접 조정 가능.
- [[mailer]]·[[schedule-reporter-kakao]]가 "업무 자동화 축"이라면, 이 프로젝트는 "챗봇 도메인 + LLM 오케스트레이션 축". 셋 다 [[공통-기술스택]]+[[parking]] 공유.
- 다음 레버리지: [[Claude-Code-업데이트-동향]]의 에이전트/`/goal` 흐름과 합류 — 생성·검증·재시도 루프를 에이전트화. ([[claude-api]] 참고: 단 현재 provider는 OpenAI gpt-4o)

## 관련 문서
- [[프로젝트-포트폴리오]] · [[내-프로필]] · [[공통-기술스택]] · [[parking]] · [[claude-api]] · [[Claude-Code-업데이트-동향]] · [[mailer]] · [[schedule-reporter-kakao]]
