---
title: Cogi-POC-Generator (Dialog JSON Generator)
category: 프로젝트
tags: [프로젝트, 챗봇, 시나리오, dialog-json, llm, openai, supabase, 핵심]
source: raw/projects/cogi-poc-generator-v1.md
created: 2026-06-09
updated: 2026-07-03
---

> [!tip] 핵심 takeaway
> ⭐ **[[내-프로필]]의 "LLM 활용 챗봇 시나리오 구성 툴"이 이제 실체를 넘어 풀스택 제품으로 컸다.** 단순 JSON 생성기였던 게 → **LLM 다단계 생성 파이프라인 + 데이터구동 규칙엔진 + 학습 레퍼런스 라이브러리 + 테스터 인증/승인**까지 갖춘 사내 POC 제품이 됐다.
> 포트폴리오 관점에서 자랑할 축이 3개: (1) **프롬프트 엔지니어링·LLM 오케스트레이션**(6단계 생성, closed-world 검증, 토큰/비용 집계), (2) **하드코딩 대신 DB-구동 규칙 설계**(solution_rules가 SoT — 운영자가 코드 없이 규칙 조정), (3) **풀스택 운영**(인증/승인 게이트·신뢰기기 로그인·어드민 8탭). 챗봇 도메인 지식 + 풀스택 + LLM이 한 프로젝트에 다 들어왔다.

## 현재 상태 스냅샷 — v0.1.0 프로토타입 배포 (2026-06-30)
> [!note] 마일스톤: "지금 상태 그대로 프로토타입 배포"
> 📄 2026-06-30, **현재 v0.1.0 상태를 그대로 프로토타입으로 배포(릴리스)**하기로 결정. 보고·테스트용 첫 기준선이다. 이 시점의 상황 정리:
> ✅ (2026-07-03 저녁 갱신) **v0.2.0 프로덕션 릴리스 완료** — 이 v0.1.0 스냅샷은 역사 기준선. 현재 프로덕션 = **v0.2.0**(PR #98 머지 `36d0181`, tag `v0.2.0` + GitHub Release, DB 마이그레이션 6개 적용, 프로덕션 함수 5종 배포, Vercel 번들 v0.2.0 확인, dev 리셋 완료) — 아래 [[#✅ v0.2.0 — AI 자유응답(LLM 노드) 블록 (2026-07-03 프로덕션 릴리스)|v0.2.0 블록]] 참고.

**무엇이 어디에 (모두 라이브 확인 200)**
- 📄 **앱 프로토타입**: https://cogi-poc-generator-v1.vercel.app — 실제 생성기 앱(테스터 이메일 OTP 인증 게이트). Vercel 프로젝트 `cogi-poc-generator-v1`.
- 📄 **개요·매뉴얼 공개 문서**: https://cogi-overview.vercel.app — 무계정 공개, 브랜드 파비콘·버전 히스토리 포함. 편집 원본은 claude.ai 아티팩트 `1e30660a…`. (상세 [[#공개 배포 — 개요·매뉴얼 페이지 (운영 SoP)|공개 배포 SoP]])
- 📄 **코드 기준선**: git tag **`v0.1.0`** + GitHub Release, `package.json` 0.1.0, 엣지함수 cogi-generator **v87**, 610커밋 · 마이그레이션 54 · solution_rules 8 카테고리.

**버전 관리**
- 📄 SemVer 0.x로 버전 관리 시작. ⚠ **동결 버전은 임의로 바꾸지 않는다**(테스트·보고는 이 태그 기준). 다음 변경은 새 버전으로.
- 📄 버전 히스토리는 **공개 페이지의 "버전 히스토리" 섹션 + 아래 [[#버전 히스토리 (문서·릴리스 기준선)|위키 버전표]]** 둘을 함께 갱신.

**검증됨 / 미검증**
- ✅ 두 공개 URL 무계정 열람 200, 개요 문서 v0.1.0 내용·파비콘·버전표 반영 확인.
- ⚠ **루프 런타임 탈출 의미는 미검증** — 코드 내장·규칙 튜닝까지 배포됐으나 실제 대화 런타임 탈출 동작은 추가 검증 필요(배포 후 우선 확인 대상).
- ⚠ **변수 처리(특히 JSON 데이터) 미숙 → 개선 필요** (📄 사용자, 2026-06-30): 챗봇 솔루션 런타임이 **JSON 형태 데이터를 자동으로 뿌리지(펼치지) 못함** → 생성된 멘트/노드에서 JSON을 통째로 출력할 수 없고, JSON을 열어 **내부 데이터를 키로 직접 지정**해 써야 함(`${변수.키}`·`${목록[0].키}`, 함수 미지원). 현재는 생성 단계에서 정확한 키 참조로 우회(관련 규칙 PR #88~#90)하나, **사용자가 JSON을 직접 열어보고 맞춰야 하는 수작업이 남아** 변수/구조화 데이터 출력 처리 고도화가 필요. 🧠 개선 방향(후보): 생성 시 JSON 필드를 개별 변수로 자동 펼치기 / 키 참조 자동 생성·검증 / 어떤 키를 쓸지 UI로 안내.

**이번 정리(2026-06-30 세션)에서 한 일** — 🧠 요약
- v0.1.0 동결을 위키([[#진행 현황 (2026-06-30)|진행 현황]])·[[프로젝트-포트폴리오]]·개요 문서에 반영.
- 개요·매뉴얼 문서를 무계정 공개 페이지로 배포 + 운영 SoP·버전 히스토리·브랜드 파비콘 정리.

## 개요
- 📄 설명: Cogi **Dialog JSON Generator** — 챗봇 대화 시나리오(플로우)를 LLM으로 생성하는 POC 제너레이터 + 학습/관리 어드민. (`README.md`)
- 📄 유형: **풀스택**. 프론트(React SPA) + Supabase Edge Functions(Deno) 백엔드 + Postgres. **버전 v0.2.0**(2026-07-03 릴리스 — `package.json` 0.2.0, annotated tag `v0.2.0` + GitHub Release; v0.1.0은 2026-06-30 첫 동결 기준선).
- 📄 생성 흐름: 사용자가 레퍼런스 선택 → 맞춤 질문(설문) 응답 → 학습된 템플릿/규칙 기반으로 Cogi Dialog JSON 생성 → 결과 저장·다운로드. (`README.md`)
- 🧠 2026-06-09 위키 작성 시점엔 "배포 준비된 프론트 POC"였으나, 2주간 ~200커밋으로 **백엔드·LLM 파이프라인·인증이 본격화된 제품**이 됐다.

## 주요 기능
- 📄 **LLM 다단계 생성 파이프라인** (`supabase/functions/cogi-generator`, 엣지함수 **v87** 배포 기준): Stage1 추상 플로우 설계(LLM) → Stage2 결정론적 노드 전개(LLM 0콜) → Stage2.5 값 채우기(LLM) → Stage2.6 ESD 스키마·API 정의 파생(LLM) → **결정론적 안전장치 체인** Stage2.9 루프 탈출변수 정합화 → 2.95 반복수집 루프 래핑 → 3 검증 재시도 루프 래핑 → 3.5 무의미 컨디션 노드 제거 → 3.6 루프 누적 배열 자동 초기화 → output 멘트 패스(placeholder leak 정리·필드 미상 힌트). 🧠 LLM은 설계·값해석만, **구조 정합성·안전장치는 코드(결정론)가 보장**.
- 📄 **반복 루프 생성** (`flow/wrapValidationLoops.ts`, `loopBehavior.ts`): Stage1 LLM이 시나리오 의도에 따라 `loop` 노드(body/exitVar/max)를 *설계* → `expandWithSpecs`가 subdialog JSON으로 결정론 변환(조건식·flag 초기화·안전카운트) → validate/repair가 본문 도달성·exitVar set 존재를 검증. 입력 검증 실패 시 재질문 루프 자동 생성. 루프 노드는 코드 내장, 동작 파라미터(탈출 비교·flag 자동초기화·최대횟수·포맷 정규식)는 `Loop Rule` 카테고리에서 튜닝.
- 📄 **데이터구동 규칙 엔진**: 생성 규칙을 코드에 박지 않고 `solution_rules`(DB, **8 카테고리**: Solution / System Variable / Node Usage / Variable Usage / Value Generation / Output Message / Condition / **Loop Rule**)에 두고 단계별 프롬프트에 주입(`RULE_STAGE_BY_CATEGORY` 매핑). 어드민 또는 레퍼런스 학습으로 규칙 추가. (`CLAUDE.md`)
- 📄 **규칙 학습 + 정합화** (`learn-solution-rules`): 자연어나 예시 봇 JSON에서 생성 규칙을 도출하고, 기존 규칙과 충돌 시 교체/유지/수정으로 정합화. 솔루션 규칙 탭 상단 패널로 통합.
- 📄 **레퍼런스 학습**: `derive-node-specs`(결정론적 노드 추출 → LLM 일반화 → closed-world 검증), `learn-rules`(레퍼런스 JSON 구조 학습). (`supabase/functions/`)
- 📄 **시나리오 레퍼런스 라이브러리** (`/scenarios`, `cogi_scenario_references`): 산업군별(금융/물류/소매/도매/의료/기타) 미니봇 학습자료. Stage1 few-shot 예시로 주입 + 사용자 단일선택/조립.
- 📄 **API 레퍼런스 라이브러리** (`cogi_api_references`): import용 API 정의 관리(엔드포인트당 1행) + 어드민에서 실제 호출 test(프록시). 쿼리 파라미터·JSON 통째 바디·필수/선택 구분 지원, 이름 비우면 LLM 생성, 이름 검증(한글·특수문자·공백 불가), 테스트 통과 후 수동 등록(자동등록 폐기), 미통과 시 위치 안내·자동 이동.
- 📄 **테스터 인증·승인** (`testers`, `trusted-device`): 이메일 OTP 로그인 → 승인 게이트(pending→approved) → 계정별 결과(RLS) → 신뢰기기 등록 후 이메일만으로 재로그인(30일).
- 📄 **LLM 토큰 사용량·예상비용 집계·표시** (`flow/usage.ts`).
- 📄 **사용자 피드백**: 플로팅 버튼 → 우측하단 팝오버, 어드민 피드백 관리 탭(미완료 배지).
- 📄 어드민 **8탭**: 질문 / 참고자료 / 템플릿 / 솔루션 규칙(규칙 학습·정합화 패널 내장) / 피드백(미완료 배지) / 시나리오 레퍼런스 / API 레퍼런스 / 테스터. (레거시 `rules`=필드정의 학습은 라우트로만 잔존, 메인 네비에서 제외)

## 기술 스택
[[공통-기술스택]] 기반 + 풀스택 확장:
- 📄 **프론트**: React 19.2, Vite 8, React Router 7, Tailwind CSS 4, Radix UI + shadcn, lucide-react. 폼/검증 = react-hook-form + **zod**(Dialog JSON 구조 검증의 핵심).
- 📄 **백엔드**: Supabase Edge Functions(Deno/TypeScript) **21개**, Postgres(**54 마이그레이션**, RLS). 순수 함수(flow/*)는 `deno test`로 단위 테스트. ([[parking]])
- 📄 **LLM**: **OpenAI `gpt-4o`** (temperature 0.1). ⚠ GEMINI는 mailer/grafana용이고 Cogi와 무관(혼동 금지).
- 📄 **배포**: 프론트 Vercel(main 푸시 자동), 엣지함수 `supabase functions deploy`, DB `supabase db push`.

## 아키텍처
- 🧠 **3계층**: React SPA(설문·결과·라이브러리·어드민) ↔ Supabase Edge Functions(생성·학습·CRUD·인증) ↔ Postgres(규칙·레퍼런스·결과·테스터). LLM 호출은 전부 엣지함수 안에서만(키 노출 차단).
- 📄 **Flow 1급화**: Stage1 LLM이 플로우를 *설계*(FlowSpec)하고 reachability 검증·repair, Stage2가 노드에디터 JSON으로 *결정론적 전개*. 과거의 "통째 JSON을 LLM이 뱉는" 경로는 제거 — 🧠 LLM은 설계만, 구조 정합성은 코드가 보장하는 **하이브리드(LLM+결정론)** 패턴. 2026-06-29 **반복 루프**(LLM이 loop 설계 → 코드가 subdialog로 결정론 전개·탈출 검증)도 같은 골격의 최신 사례.
- 📄 **규칙 = 데이터, 로직 = 코드**: 7개 규칙 카테고리가 생성 단계(flow/config/output/condition)에 매핑돼 주입. 단 결정론적 안전장치(루트 stack 제거, 변수 use-before-declare 차단 등)는 코드에 잔존. (`CLAUDE.md`)
- 📄 **레퍼런스 일원화**: 2026-06-16 `features` 레이어 제거 → 레퍼런스 중심으로 통합. 2026-06-17 레거시 값-할당 3탭(필드스키마/조건패턴/값할당) 제거.

## 진행 현황 (2026-07-03 저녁 — v0.2.0 릴리스)
- 📄 **v0.2.0 프로덕션 릴리스 (2026-07-03)**: 4축 규약 전체 수행 — ① 코드: PR #98 머지(`36d0181`, PR #97 롤백을 릴리스로 의도적 무효화), annotated tag `v0.2.0` + GitHub Release, CHANGELOG [0.2.0] 정리 ② DB: 미적용 llm 마이그레이션 6개 push + 프로덕션 재조회 검증(AI 질문 3행·llmloop 규칙 2행 dev와 완전 일치, 템플릿 멱등 확인) ③ 엣지함수: 프로덕션 슬러그 5종(cogi-generator·admin-questions·admin-results·admin-solution-rules·results) 배포 + **프로덕션 스모크 생성 1회 전수 통과**(chained 2·guarded 1, 결과는 검증 후 삭제) ④ 프론트: Vercel 자동 배포, 번들 v0.2.0 확인.
- 📄 **머지 후 dev 리셋 완료(규약)**: dev_questions·dev_solution_rules를 프로덕션 미러로 재시드(diff 0 검증), dev_cogi_results 비움. ⚠ 질문 id가 재발급됨 — 이후 dev 테스트 요청은 새 id 기준.
- 📄 **규모**: 총 **662 커밋**, 마이그레이션 63(전부 적용), 엣지함수 26(프로덕션 21 + dev 5), solution_rules 8 카테고리(prod 30행 = dev).
- 🧠 남은 결: **런타임 검증**(Cogi 솔루션에 올려 llmloop 대화 동작 — apiKey·model·docsearch storeId는 사용자가 직접 입력), 규칙·학습자료 운영형 보강, 변수/JSON 출력 처리 고도화(v0.1.0부터의 과제), 수집형 체인의 분기·이탈 tool(v0.3 후보).

## 공개 배포 — 개요·매뉴얼 페이지 (운영 SoP)
> 📄 이 프로젝트의 **"개요 및 매뉴얼" 한 장짜리 문서**를 공개 웹페이지로 배포해 둠. **이 문서 내용을 수정·반영하라고 하면 → 아래 공개 페이지에 재배포**한다(사용자 지시, 2026-06-30).

- 🌐 **공개 URL (무계정 열람·공유용)**: **https://cogi-overview.vercel.app** — Claude 무관 정적 호스팅. 자기완결 HTML(이미지·CSS·JS 전부 내장).
  - ⚠ 긴 배포-전용 URL(`cogi-overview-xxxx-...vercel.app`)은 Vercel 보호(302)로 막힘 → **반드시 짧은 `cogi-overview.vercel.app`만 공유**.
- 🧩 **원본(편집용)**: claude.ai 아티팩트 `https://claude.ai/code/artifact/1e30660a-4c19-4a59-9f19-198bed774f7d` (단일 HTML, 개요/사용매뉴얼/관리자 3탭).
- 🎨 **파비콘**: 배포 디렉토리에 `favicon.svg`(워드마크 브랜드 마크 = 검정 라운드 사각형 `#11162A` + 앰버 가로바 `#B5701B` + 흰 세로바)를 두고, head에 `<link rel="icon" type="image/svg+xml" href="/favicon.svg">`. **재배포 디렉토리엔 `index.html`과 `favicon.svg` 둘 다** 있어야 한다(스크래치패드는 세션 임시 → 새 세션은 아래 원본으로 favicon.svg 재생성).
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-label="Cogi">
    <rect width="32" height="32" rx="10" fill="#11162A"/>
    <rect x="7" y="10" width="13.5" height="4.2" rx="2" fill="#B5701B"/>
    <rect x="13" y="10" width="4.2" height="13.5" rx="2" fill="#FFFFFF"/>
  </svg>
  ```
- 🛠 **재배포 절차** (📄 확인된 동작):
  1. HTML 수정(스크래치패드 작업본 또는 아티팩트 갱신).
  2. `index.html`로 복사한 배포 디렉토리에서 `vercel deploy --prod` (Vercel 계정 `qtw9723`, 프로젝트 **`cogi-overview`**).
  3. `curl -s -o /dev/null -w "%{http_code}" https://cogi-overview.vercel.app` 가 **200**인지 확인(인증 벽 없음).
  4. 같은 변경을 claude.ai 아티팩트에도 반영(`url=` 동일 아티팩트로 재배포)하면 원본·공개본 동기화.
- 🧠 수정 시 **아래 버전 히스토리 표 + 공개 페이지의 "버전 히스토리" 섹션**을 함께 갱신한다(둘이 mirror).

### 버전 히스토리 (문서·릴리스 기준선)
새 버전을 동결/배포할 때마다 **이 표**와 **공개 페이지의 버전 히스토리 섹션**에 한 줄씩 추가한다.

| 버전 | 날짜 | 기준선 | 핵심 내용 |
|---|---|---|---|
| **v0.2.0** | 2026-07-03 | main `36d0181` · 662커밋 · 마이그레이션 63 | **AI 자유응답(LLM 노드) 블록** — 지식소스 3종(문서/일반/혼합) 전역·시나리오별 선택, 시나리오별 LLM(Q&A형 + 수집형 **LLM-구동 플로우 체인**), llmloop 레퍼런스 골격(ask_docs+docsearch 2패스), STAGE 3.65(anythingelse 1회성)·3.75(api 결과 예외 처리) 안전장치, DEV 테이블 모드, apiKey·model·storeId 사용자 입력 불변식. |
| **v0.1.0** | 2026-06-30 | 엣지함수 cogi-generator **v87** · 610커밋 · 마이그레이션 54 | 프로토타입 동결(SemVer 0.x 시작, tag·GitHub Release). 결정론 생성 안전장치 체인(Stage 2.9~3.6) 완비, API 결과 멘트 노출·placeholder 정리. **첫 보고·테스트 기준선.** |

## 다음 버전 확인·개선 항목 (v0.1.0 이후 백로그)
> 🧠 내부 개발 백로그 — **공개 페이지엔 싣지 않음**(LLM 의존성·무한반복 위험 등은 회사 솔루션 내부·약점이라 공개 부적합). 다음 버전 작업/검증 시 이 목록을 기준선으로 본다.

### ✅ v0.2.0 — AI 자유응답(LLM 노드) 블록 (2026-07-03 프로덕션 릴리스)
> 📄 2026-07-02 하루에 설계→구현→main 머지·릴리스(PR #94~#96)까지 갔다가 **같은 날 PR #97로 전량 롤백**. 프로덕션은 v0.1.0 유지, v0.2.0은 CHANGELOG상 **"미릴리스(dev 테스트 중)"** — v0.2.0 태그 없음. 이후 작업은 `feat/llm-v0.2.0-testing` 브랜치 + dev 환경에 누적.
> 📄 **2026-07-03 릴리스**: 아래 7/3 확장 전부(생성 결함 3건 수정 + 지식소스 + 시나리오별 LLM + LLM-구동 체인 + model 빈 값 + api 예외 처리)를 담아 **프로덕션 릴리스 완료**(tag `v0.2.0`). llm 마이그레이션 6개도 프로덕션 적용·검증 완료.
> 📄 **머지 전 최종 검증 통과 (7/3, dev API 전 기능 매트릭스)**: 시나리오 **6종**(docs/general/mixed+수집·검증루프/LLM 미사용/**API 연동**/**ESD 연동+LLM 결합**) + 전역 "둘 다"(docs)를 한 봇으로 생성해 전수 점검 — 이 과정에서 **메뉴 llmloop 주입이 시나리오 llmloop에 가려지는 결합 버그를 발견·수정**(`9a5e96a`, 시나리오 패스 선행 + 비시나리오 판정). 최종 결과 `8598c9c5`(최종검증봇_v020, llmloop 6개: 시나리오 4+메뉴+폴백, api·esd 노드 각 1) **전 항목 통과** — API 정의(`api_defs`: getMember, URL·${memberId} 바인딩)와 ESD 스키마(`esd_schemas`: 상담기록/memo)는 봇 JSON이 아니라 **generation_tiers의 별도 산출물**(Cogi import용)로 나가는 설계임을 확인. 이후 **LLM-구동 플로우 체인 규격**(아래 확장 2)과 **STAGE 3.75 api 결과 예외 처리 보장**(`c4b97bf` — 레퍼런스 관용구 [성공 자식(저장 변수 조건)→catch-all 실패 output]을 모든 api 노드에 보장, 재검증 `d7083216` 전수 통과)까지 반영하고, 결과 JSON 다운로드 파일명을 봇 이름 기반(`cogi-{봇이름}.json`)으로 개선(`87d2a23`)해 최종 홀드 지점 = **`87d2a23`**.

#### 7/3 확장 — 생성 결함 수정 + 지식소스 + 시나리오별 LLM (📄 git log `04ff579`~`3ca4282`, dev 검증 완료)
- 📄 **생성 결함 3건 수정** (`04ff579`, 검증봇_V3 생성물 피드백): ① **anythingelse 1회성 보장** — welcome처럼 다이얼로그당 1개(루트)만 유효. Stage 1 카탈로그에서 제외 + 신규 **STAGE 3.65**(normalizeAnythingElse: 중간 잔존분은 자식 있으면 컨디션 노드로 전환, 없으면 제거). ② **제작 챗봇 정보 prompt 주입** — 설문의 시나리오 상세(진입 발화·수집 항목·완료 결과)를 '챗봇 정보'에 나열 + "기능 요청은 진입 발화로 안내" 지침. ③ **llmloop 레퍼런스 풀 body** — tool `[ask_docs, no_answer]` + body `[ask_docs 핸들러→답변 reset→정보찾기 subdialog(docsearch 2패스)] + [LLM reset(_llm.terminate)→no_answer output]` (한화라이프 봇·LLM 노드 샘플 구조 그대로).
- 📄 **LLM 지식소스 3종 + 시나리오별 LLM** (`ca13dc4`, 설계 spec `docs/superpowers/specs/2026-07-03-llm-knowledge-source-and-scenario-llm-design.md`):
  - **지식소스**: `문서 검색(docs)`=ask_docs 골격+"문서 내용만 근거"(내부 정보 한정) / `일반 LLM(general)`=tool·body 없이 일반 지식 / `혼합(mixed)`=골격+"문서 우선, 없으면 일반 지식 보완". 기본값 general(도구 모르는 잔존 llmloop 포함 — storeId 없는 docsearch 런타임 실패 방지). ⚠ "웹 검색" 논의는 **LLM 일반 답변**을 의미(별도 웹 검색 기능 아님 — 사용자 확인).
  - **시나리오별 LLM (한화 봇 패턴)**: 시나리오 필드 "AI 자유응답 사용=예"면 그 시나리오 흐름 **마지막 잎 output 뒤에** 주제 전담 Q&A llmloop. **하이브리드**: Stage 1 규칙 지시 + STAGE 3.7 결정론 보장(있으면 소스별 정규화, 없으면 주입). 시나리오 식별은 진입 발화 조건 매칭.
  - **설문**: 전역 "AI 지식소스" 질문 + 시나리오 템플릿 필드 2개("AI 자유응답 사용"/"AI 지식소스"). ⚠ 템플릿은 **공유 templates 테이블에 라이브 반영됨**(사용자 승인) — 프로덕션 설문 UI에도 필드 노출(구 프론트는 showWhen 미지원이라 항상 표시, v0.1.0 생성기는 무시하므로 생성 영향 없음).
- 📄 **model도 빈 값 불변식** (`3ca4282`): 키에 따라 쓸 수 있는 모델이 달라 **apiKey·model·(docsearch) storeId 전부 사용자가 Cogi에서 직접 입력** — 정규화가 model="" 강제(기본값 gpt-4o 주입 제거).
- 📄 **검증**: deno 테스트 183개(신규 ~30개 TDD) + 실데이터(문제났던 cogi-49420202.json 재통과) + **dev 생성기 API 실호출 2회** — 최종 샘플 `dev_cogi_results` **09bde7a9**(지식검증봇_V5: FAQ 시나리오=docs 골격+주제 한정 prompt, 폴백=general 도구 없음, model·apiKey 전부 빈 값). Stage 1이 갱신된 규칙만으로 시나리오 끝 llmloop을 스스로 배치한 것도 확인(하이브리드 양 경로 모두 동작).
- 🧠 **머지 후 확인거리(minor)**: Stage 1이 분기·자식에 같은 조건을 중복 부여해 잉여 else 노드가 생기는 사례(도달 불가·무해) / llmloop stream 값이 파생 스펙(false)과 주입(true)에서 불일치.
- 📄 **구현 내용 (PR #94·#95)**: 질문지 "AI 자유응답(LLM) 사용" 선택 시 생성 시나리오에 `llmloop` 노드 보장 — 메뉴형(메뉴 분기 "AI 상담" 주입)·폴백형(anythingelse 안내를 llmloop으로 치환)·둘 다 지원. 신규 결정론 단계 **STAGE 3.7** `flow/applyLlmBlocks.ts`(주입·치환·정규화), Stage 2.5 `FILLABLE_TYPES`에 `llmloop` 허용. DB: AI 자유응답 질문 2행 + llmloop 규칙 2행(Node Usage·Value Generation).
- 📄 **핵심 안전 불변식 (구현됨)**: 모든 llmloop에 `config.apiKey = ""` 강제(레퍼런스 실키 유출 차단) + model/type 기본값·대소문자 교정 + 빈 prompt 템플릿 보충.
- 📄 **DEV 테이블 모드 (7/2 도입)**: `-dev` 슬러그 함수 5개(cogi-generator·admin-questions·admin-solution-rules·results·admin-results) + `dev_questions`/`dev_solution_rules`/`dev_cogi_results` + 로컬 프론트 `VITE_DEV_TABLES=true`(버전 배지 DEV 표시). "실행-후-머지" 워크플로우 — 프로덕션 슬러그·테이블 무접촉. 상세 규약은 저장소 `CLAUDE.md` "DEV 워크플로우 규약" 섹션(7/3, SoT).
- 📄 **dev에서 이어진 튜닝 (7/2 오후)**: 폴백 치환 시 output 자식 가진 anythingelse 선택(Stage 1산 빈 anythingelse에 막히던 문제), llmloop prompt 백틱 템플릿 리터럴 정규화, **프롬프트 샘플 섹션 구조**(챗봇 성향/챗봇 정보/응답 지침 — 챗봇 정보 나열 + 시나리오 비답습 지침, dev 규칙에 반영).
- 📄 **범위 밖(v0.3 후보)**: 툴 정의·docsearch·`_llm.tool.name` 분기·`_llm.terminate` 루프 제어.
- ✅ **(해결) 프로덕션 마이그레이션**: llm 마이그레이션 6개 릴리스 때 전부 적용·재조회 검증 완료(UPDATE 체인 no-op 아님 확인, 템플릿 멱등 가드 정상).
- ⚠ **레퍼런스 상태 (📄 DB 조회, 7/3)**: 한화라이프 LLM 봇·노드 샘플은 nodeSpecs 파생 완료(`llmloop` 포함). 단 **"LLM 노드 샘플 (7/2 발췌)"은 `pending`(nodeSpecs 미파생)** — 마스터 레퍼런스로 선택하면 Stage 1 게이트에 막힘. prompt 컨벤션 근거로는 이미 규칙에 반영돼 있어 마스터로 안 쓰면 지장 없음(파생 실행 여부는 추후 결정).

#### 7/3 확장 2 — LLM-구동 플로우 체인(수집형 LLM 시나리오 새 규격) (📄 `886f55f`, dev 검증 완료)
- 📄 **배경 (사용자 재정의)**: 시나리오 LLM은 "흐름 끝 Q&A 부착"이 아니라 **llmloop이 플로우 자체를 구성** — tool 분기 + body의 set/output으로 기존 결정론 플로우를 구현. 순서 수집은 **항목마다 전담 llmloop**(이름 받는 LLM → 연락처 받는 LLM), 각 단계에 기본 응답(고정 질문)이 있고 답변에 따라 다르게 진행. ⚠ **이 규격은 LLM 노드 내부 진행 시나리오(수집형)에만 적용**(사용자 확정) — Q&A형·미사용·전역은 기존 유지.
- 📄 **체인 규격** (`llmFlowChain.ts`, 설계 spec `2026-07-03-llm-driven-flow-scenarios-design.md`): 항목별 `[기본 응답 output("되묻는 말" 우선) → 수집 판정 llmloop]` 쌍을 then으로 연결. llmloop은 올바른 값이면 `save_{변수명}` tool 호출 → body `[핸들러 node → set(local.{변수명}=_llm.tool.args.{변수명} + _llm.terminate=true)]` → 다음 단계, 아니면 terminate 없음 = 자연 반복(재요청). **형식 검증은 LLM 판정으로 이동**(전화번호 등 prompt+tool 인자 힌트), 필수=반복/선택=빈 값 허용. 원본 api/esd 노드는 보존해 체인 끝 재배선(local 바인딩 호환), 완료 output은 "완료 시 결과"로 생성. 수집형은 지식소스 도구 미부착.
- 📄 **결정론 전담(이 규격 한정 접근 A)**: STAGE 3.7이 수집형 서브트리를 통째 교체(진입만 유지). **루트 부재 보장** 추가: Stage 1이 시나리오를 누락해도 진입 컨디션 노드를 결정론 생성(수집형·Q&A형 공통). Stage 1 카탈로그에서 **docsearch 제외**(llmloop body 전용 — anythingelse 전례).
- 📄 **검증**: deno **197 tests**(체인 빌더 6 + 통합 6 신규) + dev API 매트릭스 `bc678750` — 2단계 체인(이름 필수→연락처 선택·전화번호·되묻는 말) + 상담기록(체인→esd→완료 재배선) + Q&A/미사용/API/ESD/전역 회귀 **전수 통과**. 규칙 2행 갱신(dev 반영 + 마이그레이션 `20260703130000`).

1. 📄 **탈출 set 누락 (LLM 의존, 미해결 — 우선)**: flag 루프의 **구조는 결정론적으로 보장**되지만, **LLM이 본문에 탈출 flag set 자체를 안 만들면 무한 반복**. `normalizeLoopExit`는 *틀린* flag만 고칠 뿐 **없는 set은 만들지 못함**. → 다음 버전 확인: **앱에서 flag 루프 생성 시 본문에 탈출 set이 있는지 여전히 눈으로 확인 필요**. (검증루프·API·ESD는 결정론적이라 항상 안전 — 이 위험은 LLM이 설계하는 flag 루프에 한정.) ↔ 기존 메모 "런타임 탈출 의미 미검증"과 같은 결.
2. 📄 **자동 회귀 검증 부재 (🧠 옵션 2 — 급하지 않음)**: 코드가 바뀔 때마다 polarity·flag 흐름을 **다시 수동 라이브로 확인**해야 함. 지금은 "동작하는 거 확인했다"는 **1회 관측**이라 회귀에 약함. **런타임 평가를 모사하는 시뮬 하네스**가 있으면 자동화됨. → 우선순위 낮음: **루프 로직이 또 크게 흔들릴 때 도입**해도 됨.

🧠 (참고) 위 둘 외 이미 기록된 한계: **변수/JSON 출력 처리 미숙**(JSON 자동 출력 불가→키 직접 지정), 둘 다 위 [[#현재 상태 스냅샷 — v0.1.0 프로토타입 배포 (2026-06-30)|현재 상태 스냅샷]] 한계 참고.

## 진행사항 업데이트 로그
### 2026-07-03 (오후) — v0.2.0 확장(지식소스·시나리오 LLM) 후 ⏸ 홀드 (📄 git log·dev API 실검증)
- **생성 결함 3건 수정**(`04ff579`): anythingelse 1회성(STAGE 3.65 신설+카탈로그 제외) · 제작 챗봇 정보 prompt 주입(시나리오 상세) · llmloop 레퍼런스 풀 body(ask_docs/no_answer+docsearch 2패스).
- **지식소스 3종 + 시나리오별 LLM**(`ca13dc4`): 문서 검색/일반 LLM/혼합을 전역·시나리오별로 설문 선택, "사용=예" 시나리오 끝에 주제 전담 Q&A llmloop(하이브리드: Stage 1 규칙+3.7 결정론 보장). 설계 spec 커밋, 공유 templates에 필드 2개 라이브 반영(사용자 승인).
- **model 빈 값 불변식**(`3ca4282`): apiKey·model·storeId 전부 사용자 입력(키 종속).
- **검증**: deno 183 tests + dev 생성기 API 실호출(최종 샘플 `09bde7a9` — 시나리오 docs 골격/폴백 general/빈 키·모델 모두 확인).
- **⏸ 홀드**: 이 지점(`3ca4282`, 650커밋·마이그레이션 62)에서 v0.2.0 개발 동결(사용자 지시). 프로덕션 머지는 별도 승인 대기 — llm 마이그레이션 5개 미적용 주의.

### 2026-07-03 — v0.2.0 구현→main 롤백→dev 테스트 체제 + 보안 정리 (📄 git log·DB 직접 조회)
- **v0.2.0 하루 만에 구현→릴리스→롤백 (7/2)**: 설계 문서(`d6e57d5`) 당일에 applyLlmBlocks(STAGE 3.7)·DB 질문/규칙까지 구현해 PR #94(기능)·#95(model 대소문자 픽스)·#96(릴리스)로 main 머지 → **같은 날 PR #97로 전량 revert**. 프로덕션 v0.1.0 유지, v0.2.0은 "미릴리스(dev 테스트 중)"로 CHANGELOG 정정.
- **DEV 테이블 모드 도입 (`ac9ea93`)**: 같은 Supabase 안에 `dev_questions`/`dev_solution_rules`/`dev_cogi_results` + `-dev` 슬러그 함수 5개 + 프론트 `VITE_DEV_TABLES=true`. 프로덕션 무접촉 "실행-후-머지" 워크플로우 확립.
- **dev 튜닝 3건 (7/2 오후)**: 폴백 anythingelse 선택 픽스(`00715c1`) · prompt 백틱 정규화(`e1588cd`) · 프롬프트 샘플 섹션 구조 — 챗봇 정보 나열+비답습 지침(`dde7e15`, dev 규칙에도 반영 확인).
- **DEV 워크플로우 규약 명문화 (7/3, `5c4bb3d`)**: 저장소 CLAUDE.md에 "모든 작업은 dev / 프로덕션 머지 시 4축(코드·DB·엣지함수·프론트) 전체 마이그레이션+push 후 재검증 / 머지 후 dev_ 테이블을 프로덕션 미러로 리셋" 규약 추가(사용자 지시). 이 기기 Claude 메모리에도 동일 규약 저장.
- **보안 정리 — 레퍼런스 JSON apiKey 전수 마스킹 (7/3, DB 직접)**: JSON 보유 7개 테이블 전수 스캔 → 비어있지 않은 apiKey **8건**(한화라이프 LLM 봇 5 · 노드 샘플 2 · 옛 생성 결과 1)을 전부 `""`로 마스킹, 재스캔 0건 확인. 설계 문서의 "평문 키 제거 권장" 항목 해소.
- **구조 수치**: 마이그레이션 54→60, 엣지함수 21→26(dev 슬러그 +5), 커밋 610→646(테스트 브랜치).
- 🧠 의미: 6/30 "생성 결과의 결정론 강제"에 이어, 7/2~3은 **작업 환경 자체의 결정론화**(dev 격리·머지 절차·리셋 규약) — 프로덕션 안정성을 프로세스 수준으로 끌어올린 구간.

### 2026-07-02 — v0.2.0 설계 착수(문서만) + 낡은 초안 폐기 (📄 git log)
- 🚧 **AI 자유응답(LLM 노드) 블록 v0.2.0 설계 착수** (`d6e57d5`, 브랜치 `feat/llm-response-block`): 설계 문서 1개만 추가(`docs/superpowers/specs/2026-07-02-llm-response-block-design.md`, +131줄). **코드 0줄·main 미머지·버전 v0.1.0 그대로.** 상세는 위 [[#🚧 v0.2.0 설계 착수 — AI 자유응답(LLM 노드) 블록 (⚠ 설계 문서만, 미구현·미머지)|v0.2.0 설계 블록]].
- 📄 **낡은 개요·매뉴얼 초안 `.md` 폐기** (PR #93, 2026-07-01 머지): `docs/프로젝트-개요-및-매뉴얼-초안.md` 삭제(−168줄). 초안의 잘못된 버전("1.0.1")·구식 커밋수가 실제 v0.1.0 상태와 혼동될 위험 → SoT를 공개 페이지(cogi-overview.vercel.app)+claude.ai 아티팩트로 일원화.
- 🧠 이 기간 main 반영 실코드 변경은 **없음**(문서 정리 + 미머지 설계뿐). 버전·기능 기준선은 v0.1.0 유지.

### 2026-06-30 — v0.1.0 프로토타입 동결 + 결정론적 생성 안전장치 (📄 git log, PR #76~#85)
- **v0.1.0 프로토타입 동결 (PR #84, 가장 큰 신규)**: 버전 관리 시작 — `package.json` 0.1.0 + annotated tag `v0.1.0` + GitHub Release. 보고·테스트용 기준선(엣지함수 cogi-generator **v87** 배포 기준). ⚠ 동결 버전은 변경 금지, 테스트는 태그 기준.
- **앱 버전 배지 (PR #85)**: 전 화면 좌하단에 현재 앱 버전 상시 표시.
- **반복 수집 결정론화 (PR #80·81)**: '여러 개 입력' 플래그로 반복 수집을 결정론 래핑(Stage 2.95). LLM이 직접 만든 count 루프도 제자리 정규화.
- **루프 누적 배열 변수 자동 초기화 (PR #79, Stage 3.6)**: 루프 누적 배열을 결정론적으로 사전 초기화.
- **무의미 컨디션 노드 결정론 제거 (PR #77·78, Stage 3.5)**: 컨디션 노드 사용 요건 강화 + 무의미한 노드 생성·잔존 차단.
- **반복 수집 루프 규칙 (PR #76)**: 배열 누적 + 본문 탈출 분기 규칙.
- **출력 멘트 정리 (PR #82·83)**: API 조회 결과를 멘트에서 *값*으로 노출, 멘트 placeholder leak 정리 + 필드 미상 힌트 개선.
- **구조 수치**: 마이그레이션 49→54. 엣지함수 21개·solution_rules 8 카테고리는 유지.
- 🧠 6/29의 "LLM 설계 + 코드 검증" 하이브리드를, 6/30엔 **생성 후처리 안전장치 체인(Stage 2.9~3.6)**으로 더 두껍게 — 생성 결과의 결정론·정합성을 코드가 강제하는 방향이 한층 굳어짐.

### 2026-06-29 — 루프 생성·규칙 학습 정합화·API 고도화 (📄 git log, PR #42~#67)
- **반복 루프 생성 (가장 큰 신규, PR #57·60·63~67)**: LLM이 시나리오 의도대로 `loop` 노드를 *설계*하고, flag 변수 탈출 규약 + 결정론적 subdialog 변환·검증으로 정확성 보장. 입력 검증 실패 시 재질문 루프 자동 생성. 동작 파라미터는 `Loop Rule` 카테고리(루프 동작 설정)에서 튜닝. → 🧠 "LLM 설계 + 코드 검증" 하이브리드 패턴을 반복 제어까지 확장.
- **규칙 학습 + 정합화 (PR #52·53)**: `learn-solution-rules` 엣지함수 신설 — 자연어/예시 JSON에서 규칙 도출 → 기존 규칙과 충돌 시 교체/유지/수정. 별도 화면 → 솔루션 규칙 탭 상단 패널로 통합.
- **API 레퍼런스 고도화 (PR #46~#49·54·55)**: 쿼리 파라미터·JSON 통째 바디·필수/선택 구분, 이름 비우면 LLM 생성, 이름 검증(한글·특수문자·공백 불가), 테스트 통과 후 수동 등록(자동등록 폐기), 테스트 게이트 위치 안내·자동 이동, '보낼 정보'에서 자기 결과 제외.
- **변수명 규칙 고도화 (PR #56·58·59)**: 수집 정보 **항목명↔변수명 분리**, 변수명 규칙을 condition 단계에도 주입(분기에서 항목명 새던 버그·날조 차단).
- **생성 신뢰성 픽스**: 메인 welcome 보장(#57), `_result` 노드내부 전용·스코프 시나리오내부=local(#51).
- **UX**: 시나리오 폼 전체 필드 도움말(#44·45), 결과 응답 긴 텍스트 박스 넘침 해결(#50), 어드민 로그인 진입·탭 배지 줄바꿈 방지(#42·43).
- **구조 수치**: 엣지함수 20→21(`learn-solution-rules`), 마이그레이션 40→49, solution_rules 7→8 카테고리(`Loop Rule`), 어드민 9→8탭(규칙 학습 통합).

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
