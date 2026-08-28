---
title: CogInsight-Generator (Dialog JSON Generator)
category: 프로젝트
tags: [프로젝트, 챗봇, 시나리오, dialog-json, llm, openai, supabase, 핵심]
source: raw/projects/coginsight-generator.md, raw/ai-digest/2026-08-12.md, raw/ai-digest/2026-08-13.md, raw/ai-digest/naver-2026-08-20.md, raw/ai-digest/naver-2026-08-21.md, raw/ai-digest/2026-08-21.md, raw/ai-digest/2026-08-22.md
created: 2026-06-09
updated: 2026-08-27
---

> [!tip] 핵심 takeaway
> ⭐ **[[내-프로필]]의 "LLM 활용 챗봇 시나리오 구성 툴"이 이제 실체를 넘어 풀스택 제품으로 컸다.** 단순 JSON 생성기였던 게 → **LLM 다단계 생성 파이프라인 + 데이터구동 규칙엔진 + 학습 레퍼런스 라이브러리 + 테스터 인증/승인**까지 갖춘 사내 POC 제품이 됐다.
> 포트폴리오 관점에서 자랑할 축이 3개: (1) **프롬프트 엔지니어링·LLM 오케스트레이션**(6단계 생성, closed-world 검증, 토큰/비용 집계), (2) **하드코딩 대신 DB-구동 규칙 설계**(solution_rules가 SoT — 운영자가 코드 없이 규칙 조정), (3) **풀스택 운영**(인증/승인 게이트·신뢰기기 로그인·어드민 8탭). 챗봇 도메인 지식 + 풀스택 + LLM이 한 프로젝트에 다 들어왔다.

## 현재 상태 스냅샷 — v0.1.0 프로토타입 배포 (2026-06-30)
> [!note] 마일스톤: "지금 상태 그대로 프로토타입 배포"
> 📄 2026-06-30, **현재 v0.1.0 상태를 그대로 프로토타입으로 배포(릴리스)**하기로 결정. 보고·테스트용 첫 기준선이다. 이 시점의 상황 정리:
> ✅ (2026-07-03 저녁 갱신) **v0.2.0 프로덕션 릴리스 완료** — 이 v0.1.0 스냅샷은 역사 기준선. 현재 프로덕션 = **v0.2.0**(PR #98 머지 `36d0181`, tag `v0.2.0` + GitHub Release, DB 마이그레이션 6개 적용, 프로덕션 함수 5종 배포, Vercel 번들 v0.2.0 확인, dev 리셋 완료) — 아래 [[#✅ v0.2.0 — AI 자유응답(LLM 노드) 블록 (2026-07-03 프로덕션 릴리스)|v0.2.0 블록]] 참고.
> ✅ (2026-07-08) v0.2.1 — ESD 스키마 파생 핫픽스(PR #100, tag v0.2.1). 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-08 v0.2.1]].
> ✅ (2026-07-09) v0.2.2 — **프로젝트명 전면 변경: CogInsight Generator**. 📄 **확정 사항(2026-07-09, 사용자 확인)**: 구명(코드네임 4글자, 이 vault에서 표기 금지)은 **사용 불가 판정** → 코드·DB·함수 슬러그·Vercel·GitHub·위키·메모리 전체 리네임. **구 URL 전부 폐기**(공유했던 링크는 재안내 필요). 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-09]]. ⚠ 이 페이지의 과거 로그·버전표 속 명칭·URL·테이블명도 새 이름으로 소급 치환됨(사실 관계는 동일, 이름만 현행화).
> ✅ (2026-07-09 오후) v0.3.0 — 시나리오 레퍼런스 라이브러리 릴리스(레퍼런스 5종 승격, dev 리셋 완료). 상세는 [[#진행 현황|진행 현황]].
> ✅ (2026-07-09) v0.3.1 — **생성기 백엔드 LLM 모델 `gpt-4o` → `gpt-5.2` 전환**(PR #105, tag v0.3.1). OpenAI 키 로테이션 포함. ⚠ 비용 단가표(`flow/usage.ts`) 미갱신 이슈. 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-09 v0.3.1]].
> ✅ (2026-07-15) **v0.4.0 — 플로우 시각화 프로덕션 릴리스** (PR #106 머지 main `52a0f59`, tag v0.4.0 + GitHub Release). react-flow 캔버스 뷰어(구조 다이어그램 + 사용자 흐름도) + PNG·풀스크린, **진입점 4곳**(레퍼런스 2 + 생성 결과 2). 프론트 전용(Vercel 자동 배포, DB·엣지함수 무변경). 검증 green(deno 260/0, build 2065). 공유 개요 페이지·링크 노트 갱신. 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-15 릴리스]].
> ✅ (2026-07-15) **v0.4.1 — 결과 탭 사용자별 보기** (PR #107 머지 main `3b68501`, tag v0.4.1). 결과 탭(`/results`)에 사용자 필터 드롭다운 + "사용자별로 묶어 보기" 그룹 토글. 프론트 전용(`created_by`), main 직접 릴리스(사용자 요청). 공개 개요 페이지도 v0.4.1 반영(히어로·버전표 갱신·재배포). ⚠ **정정(2026-07-21)**: 이 "공개 개요 페이지 v0.4.1 반영"은 **실제 라이브에 도달하지 않았음**(2026-07-20까지 라이브·아티팩트 모두 v0.3.0) — 2026-07-21에야 실제 복구·배포됨. 아래 [[#진행사항 업데이트 로그|2026-07-21 로그]] 참고.
> ✅ (2026-07-28) **v0.5.0 — 입력 소스 다양화** (PR #111 머지 main `1e3237d`, tag v0.5.0 + GitHub Release). **현재 프로덕션 = v0.5.0**. 설문 폼 외 4갈래 입구(①엑셀→ESD CSV/스키마 `/convert` ②API문서(OpenAPI)→api_def ③자연어→시나리오 `/nl` ④POC문서(엑셀·PDF·MD·txt)→생성) + 신규 엣지함수 2종(`poc-doc-parse`·`nl-scenario-parse`) 배포, Vercel v0.5.0 라이브 확인 + 사내 온프렘 배포 완료 + 공개 개요 페이지 v0.5.0 반영. DB·`solution_rules` 무변경. 릴리스 규약 5단계화(⑤ 공개 개요 페이지 필수). ⚠ dev 리셋만 다음 버전 착수 시로 이월.
> ✅ (2026-07-29) **v0.5.1 — UI/UX 앱 셸 개편 + 문서→API 생성 도구** (PR #113 머지 main `345fa96`, tag v0.5.1 + GitHub Release). **현재 프로덕션 = v0.5.1**. 헤더 nav → **그룹형 사이드바 앱 셸**(접기/펼치기·툴팁·버전 배지 우상단), 라우팅 개편(`/`=자연어 기본·`/survey`=설문·`/doc` 승격·`/api` 신규), 전역 로딩 오버레이, 신규 엣지함수 `api-doc-parse`. DB·`solution_rules` 무변경. 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-29 v0.5.1]].
> ✅ (2026-08-04) **v0.6.0 — ESD·API 선행 정의·매핑 + 멀티파일 지능형 수집** (PR #114 머지 main `1e5d53d`, tag v0.6.0 + GitHub Release). **현재 프로덕션 = v0.6.0**. 생성 앞단 ESD·API 선행 정의(`EsdFrontStage`, 옵트인·회귀 없음)를 매핑에 실사용(`proposeMapping` + 옵션 2-pass `MappingStep`), ESD는 결과 `generation_tiers.esd` 번들. 멀티파일 지능형 수집(`MultiFileUpload`, 자동 분류·라우팅 + 신규 `ingest-classify`), API 문서 하이브리드 인입(OpenAPI 결정론 + `api-doc-parse` LLM 폴백). 용어 통일(ESD·API 편집·스키마). 아키텍처: ESD 별도 테이블 없이 결과 번들(`generation_tiers.esd`, `results` PATCH). DB 규칙 마이그레이션 `20260731130000_mapping_rules`(버전 무관), 프로덕션 함수 4종 배포, 사내 온프렘 배포 완료. **기능 검증에서 `.json/.yaml` 추출·한글 CSV mojibake 버그 2건 발견·수정.** ⚠ 공개 개요 페이지(`coginsight-overview`)·claude.ai 아티팩트 반영은 별도 진행. 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-08-04 v0.6.0 릴리스]].
> ✅ (2026-07-21) **v0.4.2 — 결과 확인 창 UI 개선** (PR #108 머지 main `2986e1f`, tag v0.4.2 + GitHub Release). 결과 상세(`/results/:id`)의 입력 시나리오 카드화·접기(기본 접힘) + 요약 헤더(봇 이름·메타 칩)·섹션 네비 + 버튼 색 통일. 프론트 전용. 공개 개요 페이지·아티팩트·위키 동기화 완료. 상세는 [[#진행사항 업데이트 로그|2026-07-21 v0.4.2 로그]].

**무엇이 어디에 (모두 라이브 확인 200)** — 공유용 정리는 [[CogInsight-Generator-링크]]
- 📄 **앱 프로토타입**: https://coginsight-generator.vercel.app — 실제 생성기 앱(테스터 이메일 OTP 인증 게이트). Vercel 프로젝트 `coginsight-generator`.
- 📄 **개요·매뉴얼 공개 문서**: https://coginsight-overview.vercel.app — 무계정 공개, 브랜드 파비콘·버전 히스토리 포함. 편집 원본은 claude.ai 아티팩트 `1e30660a…`. (상세 [[#공개 배포 — 개요·매뉴얼 페이지 (운영 SoP)|공개 배포 SoP]])
- 📄 **사내 온프렘 배포**(2026-07-28 추가): 회사 로컬 서버에도 앱을 함께 서빙(포트 3006, pm2+serve). **정적 프론트만 온프렘**이고 백엔드(Supabase·엣지함수·LLM)는 Vercel 프로덕션과 **동일 클라우드 공유** — 브라우저가 직접 Supabase로 나간다. 릴리스마다 `scripts/deploy-internal.sh`로 함께 배포(빌드→전송→재기동). ⚠ 사내 서버 주소·계정·방화벽 등 인프라 상세는 기밀 분리 원칙상 **레포 `DEPLOYMENT.md`에만** 둔다(이 동기화 vault에는 미기재).
- 📄 **코드 기준선**: git tag **`v0.1.0`** + GitHub Release, `package.json` 0.1.0, 엣지함수 coginsight-generator **v87**, 610커밋 · 마이그레이션 54 · solution_rules 8 카테고리.
- 📄 **소스 저장소**(2026-07-29 추가): 기존 GitHub(개인, Vercel 배포용 `origin`)에 더해 **사내 GitLab에도 전체 미러**(할당받은 회사 프로젝트, 회사 계정). 전 브랜치 31 + 태그 11 push, 기본 브랜치 `main` 정리 완료. ⚠ 사내 GitLab **호스트·프로젝트 경로·계정·인증(PAT) 상세는 기밀 분리 원칙상 레포 `DEPLOYMENT.md`에만** 둔다(이 동기화 vault엔 미기재). 🧠 이후 양쪽 유지 시 remote별 개별 push.

**버전 관리**
- 📄 SemVer 0.x로 버전 관리 시작. ⚠ **동결 버전은 임의로 바꾸지 않는다**(테스트·보고는 이 태그 기준). 다음 변경은 새 버전으로.
- 📄 버전 히스토리는 **공개 페이지의 "버전 히스토리" 섹션 + 아래 [[#버전 히스토리 (문서·릴리스 기준선)|위키 버전표]]** 둘을 함께 갱신.

**검증됨 / 미검증**
- ✅ 두 공개 URL 무계정 열람 200, 개요 문서 v0.1.0 내용·파비콘·버전표 반영 확인.
- ⚠ **루프 런타임 탈출 의미는 미검증** — 코드 내장·규칙 튜닝까지 배포됐으나 실제 대화 런타임 탈출 동작은 추가 검증 필요(배포 후 우선 확인 대상).
- ⚠ **변수 처리(특히 JSON 데이터) 미숙 → 개선 필요** (📄 사용자, 2026-06-30): 챗봇 솔루션 런타임이 **JSON 형태 데이터를 자동으로 뿌리지(펼치지) 못함** → 생성된 멘트/노드에서 JSON을 통째로 출력할 수 없고, JSON을 열어 **내부 데이터를 키로 직접 지정**해 써야 함(`${변수.키}`·`${목록[0].키}`, 함수 미지원). 현재는 생성 단계에서 정확한 키 참조로 우회(관련 규칙 PR #88~#90)하나, **사용자가 JSON을 직접 열어보고 맞춰야 하는 수작업이 남아** 변수/구조화 데이터 출력 처리 고도화가 필요. 🧠 개선 방향(후보): 생성 시 JSON 필드를 개별 변수로 자동 펼치기 / 키 참조 자동 생성·검증 / 어떤 키를 쓸지 UI로 안내.

**이번 정리(2026-06-30 세션)에서 한 일** — 🧠 요약
- v0.1.0 동결을 위키([[#진행 현황|진행 현황]])·[[프로젝트-포트폴리오]]·개요 문서에 반영.
- 개요·매뉴얼 문서를 무계정 공개 페이지로 배포 + 운영 SoP·버전 히스토리·브랜드 파비콘 정리.

## 개요
- 📄 설명: CogInsight **Dialog JSON Generator** — 챗봇 대화 시나리오(플로우)를 LLM으로 생성하는 POC 제너레이터 + 학습/관리 어드민. (`README.md`)
- 📄 유형: **풀스택**. 프론트(React SPA) + Supabase Edge Functions(Deno) 백엔드 + Postgres. **버전 v0.2.0**(2026-07-03 릴리스 — `package.json` 0.2.0, annotated tag `v0.2.0` + GitHub Release; v0.1.0은 2026-06-30 첫 동결 기준선).
- 📄 생성 흐름: 사용자가 레퍼런스 선택 → 맞춤 질문(설문) 응답 → 학습된 템플릿/규칙 기반으로 CogInsight Dialog JSON 생성 → 결과 저장·다운로드. (`README.md`)
- 🧠 2026-06-09 위키 작성 시점엔 "배포 준비된 프론트 POC"였으나, 2주간 ~200커밋으로 **백엔드·LLM 파이프라인·인증이 본격화된 제품**이 됐다.

## 주요 기능
- 📄 **LLM 다단계 생성 파이프라인** (`supabase/functions/coginsight-generator`, 엣지함수 **v87** 배포 기준): Stage1 추상 플로우 설계(LLM) → Stage2 결정론적 노드 전개(LLM 0콜) → Stage2.5 값 채우기(LLM) → Stage2.6 ESD 스키마·API 정의 파생(LLM) → **결정론적 안전장치 체인** Stage2.9 루프 탈출변수 정합화 → 2.95 반복수집 루프 래핑 → 3 검증 재시도 루프 래핑 → 3.5 무의미 컨디션 노드 제거 → 3.6 루프 누적 배열 자동 초기화 → output 멘트 패스(placeholder leak 정리·필드 미상 힌트). 🧠 LLM은 설계·값해석만, **구조 정합성·안전장치는 코드(결정론)가 보장**.
- 📄 **반복 루프 생성** (`flow/wrapValidationLoops.ts`, `loopBehavior.ts`): Stage1 LLM이 시나리오 의도에 따라 `loop` 노드(body/exitVar/max)를 *설계* → `expandWithSpecs`가 subdialog JSON으로 결정론 변환(조건식·flag 초기화·안전카운트) → validate/repair가 본문 도달성·exitVar set 존재를 검증. 입력 검증 실패 시 재질문 루프 자동 생성. 루프 노드는 코드 내장, 동작 파라미터(탈출 비교·flag 자동초기화·최대횟수·포맷 정규식)는 `Loop Rule` 카테고리에서 튜닝.
- 📄 **데이터구동 규칙 엔진**: 생성 규칙을 코드에 박지 않고 `solution_rules`(DB, **8 카테고리**: Solution / System Variable / Node Usage / Variable Usage / Value Generation / Output Message / Condition / **Loop Rule**)에 두고 단계별 프롬프트에 주입(`RULE_STAGE_BY_CATEGORY` 매핑). 어드민 또는 레퍼런스 학습으로 규칙 추가. (`CLAUDE.md`)
- 📄 **규칙 학습 + 정합화** (`learn-solution-rules`): 자연어나 예시 봇 JSON에서 생성 규칙을 도출하고, 기존 규칙과 충돌 시 교체/유지/수정으로 정합화. 솔루션 규칙 탭 상단 패널로 통합.
- 📄 **레퍼런스 학습**: `derive-node-specs`(결정론적 노드 추출 → LLM 일반화 → closed-world 검증), `learn-rules`(레퍼런스 JSON 구조 학습). (`supabase/functions/`)
- 📄 **시나리오 레퍼런스 라이브러리** (`/scenarios`, `coginsight_scenario_references`): 산업군별(금융/물류/소매/도매/의료/기타) 미니봇 학습자료. Stage1 few-shot 예시로 주입 + 사용자 단일선택/조립.
- 📄 **API 레퍼런스 라이브러리** (`coginsight_api_references`): import용 API 정의 관리(엔드포인트당 1행) + 어드민에서 실제 호출 test(프록시). 쿼리 파라미터·JSON 통째 바디·필수/선택 구분 지원, 이름 비우면 LLM 생성, 이름 검증(한글·특수문자·공백 불가), 테스트 통과 후 수동 등록(자동등록 폐기), 미통과 시 위치 안내·자동 이동.
- 📄 **입력 소스 4갈래** (v0.5.0, 2026-07-28): 설문 폼 외에 ① 엑셀→ESD 업로드 CSV·스키마 JSON(`/convert`, 프론트 결정론) ② API 인터페이스 문서(OpenAPI)→`api_def`(어드민 "문서에서 가져오기") ③ 자연어→시나리오(`/nl`, `nl-scenario-parse`) ④ POC 문서(엑셀·PDF·MD·txt)→챗봇 생성(`poc-doc-parse`). ③④는 LLM 추출 → 기존 시나리오 편집 UI로 보정 → 기존 `responses`·`createResult` 경로 재사용. ⚠ 흐름도 **이미지 시각 해석은 미지원**(PDF는 텍스트 레이어만).
- 📄 **앱 셸 · 문서→API 생성 도구** (v0.5.1, 2026-07-29): 그룹형 사이드바 앱 셸(접기/펼치기·레일 툴팁·버전 배지 우상단) + 전역 로딩 오버레이 + `/api` 문서→API 생성(한 문서에서 여러 `api_def`를 OpenAPI 결정론 파서 → LLM 폴백 `api-doc-parse` 하이브리드로 추출·검토·저장).
- 📄 **테스터 인증·승인** (`testers`, `trusted-device`): 이메일 OTP 로그인 → 승인 게이트(pending→approved) → 계정별 결과(RLS) → 신뢰기기 등록 후 이메일만으로 재로그인(30일).
- 📄 **LLM 토큰 사용량·예상비용 집계·표시** (`flow/usage.ts`).
- 📄 **사용자 피드백**: 플로팅 버튼 → 우측하단 팝오버, 어드민 피드백 관리 탭(미완료 배지). (v0.3.0 dev, 미머지: "지금 보는 화면 첨부" 체크 시 뷰포트 캡처 첨부 + 어드민 썸네일·클릭 확대 — [[#진행사항 업데이트 로그|7/7 저녁 로그]])
- 📄 어드민 **8탭**: 질문 / 참고자료 / 템플릿 / 솔루션 규칙(규칙 학습·정합화 패널 내장) / 피드백(미완료 배지) / 시나리오 레퍼런스 / API 레퍼런스 / 테스터. (레거시 `rules`=필드정의 학습은 라우트로만 잔존, 메인 네비에서 제외)

## 기술 스택
[[공통-기술스택]] 기반 + 풀스택 확장:
- 📄 **프론트**: React 19.2, Vite 8, React Router 7, Tailwind CSS 4, Radix UI + shadcn, lucide-react. 폼/검증 = react-hook-form + **zod**(Dialog JSON 구조 검증의 핵심).
- 📄 **백엔드**: Supabase Edge Functions(Deno/TypeScript) **34개**(프로덕션 슬러그 23 + `-dev` 사본, v0.6.0 브랜치 기준), Postgres(**65 마이그레이션**, RLS). 순수 함수(flow/*)는 `deno test`로 단위 테스트. ([[parking]])
- 📄 **LLM**: **OpenAI `gpt-5.2`** (v0.3.1, 2026-07-09부터 — 이전 `gpt-4o`에서 전환. 생성기가 OpenAI를 호출하는 5개 엣지함수 전부: coginsight-generator·learn-rules·learn-solution-rules·derive-node-specs·admin-solution-rules). ⚠ 생성 결과물(챗봇 llmloop 노드)의 출력 모델은 사용자가 CogInsight 솔루션에서 직접 입력하므로 무변경. ⚠ GEMINI는 mailer/grafana용이고 CogInsight와 무관(혼동 금지).
- 📄 **배포**: 프론트 Vercel(main 푸시 자동) + **사내 온프렘**(로컬 서버 3006, pm2+serve, `scripts/deploy-internal.sh`), 엣지함수 `supabase functions deploy`, DB `supabase db push`.

## 아키텍처
- 🧠 **3계층**: React SPA(설문·결과·라이브러리·어드민) ↔ Supabase Edge Functions(생성·학습·CRUD·인증) ↔ Postgres(규칙·레퍼런스·결과·테스터). LLM 호출은 전부 엣지함수 안에서만(키 노출 차단).
- 📄 **Flow 1급화**: Stage1 LLM이 플로우를 *설계*(FlowSpec)하고 reachability 검증·repair, Stage2가 노드에디터 JSON으로 *결정론적 전개*. 과거의 "통째 JSON을 LLM이 뱉는" 경로는 제거 — 🧠 LLM은 설계만, 구조 정합성은 코드가 보장하는 **하이브리드(LLM+결정론)** 패턴. 2026-06-29 **반복 루프**(LLM이 loop 설계 → 코드가 subdialog로 결정론 전개·탈출 검증)도 같은 골격의 최신 사례.
- 📄 **규칙 = 데이터, 로직 = 코드**: 7개 규칙 카테고리가 생성 단계(flow/config/output/condition)에 매핑돼 주입. 단 결정론적 안전장치(루트 stack 제거, 변수 use-before-declare 차단 등)는 코드에 잔존. (`CLAUDE.md`)
- 📄 **레퍼런스 일원화**: 2026-06-16 `features` 레이어 제거 → 레퍼런스 중심으로 통합. 2026-06-17 레거시 값-할당 3탭(필드스키마/조건패턴/값할당) 제거.

## 진행 현황
> 📄 **현재 프로덕션 = v0.9.0**(기존 챗봇 업로드 후 수정 + 자산 역파생, 2026-08-28 — PR #120 main `99e8705`, tag v0.9.0). Cogi가 만들지 않은 **솔루션 챗봇 JSON을 올려** 다이어그램으로 보고 편집하고 다시 내려받는다(`/upload`). 올린 봇에서 **NLU·ESD를 역파생**한다(신규 함수 `derive-assets`). 핵심 불변식은 **왕복 무손실** — `generated_json`이 곧 원본이고 편집은 델타 패치로만. 회귀 3종 × 실제 봇 4 fixture로 고정. 노드 타입 레지스트리(화이트리스트) — 편집 8종/잠김 13종, 잠금 사유를 코드에 분류. 잠긴 노드도 내용은 읽기 좋게 표시되고 이름은 편집된다. 직전 v0.8.1(NLU 기준 조건 설정, PR #119 `91628fb`).
> 🔶 **현재 개발 = 없음**(v0.7.0 릴리스 완료). 다음 = **v0.8.0 NLP 생성 & NLP 기준 조건 설정** 착수 예정 — dev 리셋·재세팅(`package.json` 버전 올리기 포함)이 다음 사이클 첫 단계다. 그 이전 릴리스: v0.6.0(ESD·API 선행 정의·매핑, PR #114)·v0.5.1(UI/UX 앱 셸, PR #113)·v0.5.0(입력 소스 다양화, PR #111).

- 📄 **v0.4.0 dev 구현 완료 (2026-07-14~15) — [[올림푸스-Olympus]] 자율 개발**: 레퍼런스 플로우 시각화(react-flow 캔버스 뷰어). 백로그 T1~T7 전부 완료, verify green(deno 250/0·build 2065 modules), **프로덕션 무배포**(dev 전용, `AUTO_MERGE=0 DEPLOY_ON_DONE=0`). 사용자 "프로덕션에 머지" 시 4축 릴리스. 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-14~15]].
- 📄 **v0.3.1 프로덕션 릴리스 (2026-07-09)**: 생성기 백엔드 LLM `gpt-4o` → `gpt-5.2` 전환(5개 엣지함수) + OpenAI 키 로테이션. v0.4.0 dev 사이클과 무관한 독립 패치(격리 브랜치 `fix/llm-gpt-5.2`, PR #105, tag v0.3.1). ⚠ `flow/usage.ts` 단가표 미갱신(비용 추정 부정확 — TODO).
- 📄 **v0.3.0 프로덕션 릴리스 (2026-07-09)**: 4축 규약 전체 수행 — ① 코드: PR #103 머지(main `ae99f4d`), tag `v0.3.0` + GitHub Release, CHANGELOG [0.3.0] 확정(741커밋) ② DB: dev↔본 테이블 diff 0 확인, 마이그레이션 20260707120000(피드백 screenshot_path) push·재조회 검증, **시나리오 레퍼런스 5종 승격**(도매 제외 — 사용자 선별, id 유지, 재조회 검증) ③ 엣지함수: 전 슬러그(27종) 재배포 + **프로덕션 스모크 생성 1회 통과**(collect-loop, `injected=true`·계좌 잔액 조회봇 few-shot 실주입 확인, 결과 삭제) ④ 프론트: Vercel 자동 배포·번들 0.3.0 확인.
- 📄 **머지 후 dev 리셋 완료(규약)**: dev_questions·dev_solution_rules·dev_coginsight_feedback 프로덕션 미러 재시드(내용 diff 0 검증), dev_coginsight_results 비움, 스토리지 `dev/` 스크린샷 정리, dev 슬러그 7종 main 기준 재배포. ⚠ 질문 id 재발급 — 이후 dev 테스트는 새 id 기준(하네스는 text 매칭이라 무영향). ⚠ **의도된 diff 1건**: 도매(대량주문 견적봇) 레퍼런스는 dev가 유일 소스라 dev에 보존(품질 교정 후 승격 예정 — dev 6건 = prod 5건 + 도매).
- 📄 **v0.3.0 dev 진행 (2026-07-06~07)**: 브랜치 `feat/v0.3.0-observability-regression`(main 미머지·프로덕션 무배포, 배지 `v0.3.0 DEV` 선반영). 관측성·회귀 하네스·dev 레퍼런스 6종·few-shot 전/후 검증(로드맵 항목 1·2 ✅, 항목 4 부분)에 이어 7/7 **레퍼런스 구조 시드 생성(STAGE 3.68) + 시드 UX 5건 + 피드백 스크린샷 첨부**까지 누적 — 상세는 [[#진행사항 업데이트 로그|업데이트 로그]]·[[#로드맵 — v0.3.0 (계획): 시나리오 레퍼런스 라이브러리 테스트·고도화|로드맵]].
- 📄 **v0.2.0 프로덕션 릴리스 (2026-07-03)**: 4축 규약 전체 수행 — ① 코드: PR #98 머지(`36d0181`, PR #97 롤백을 릴리스로 의도적 무효화), annotated tag `v0.2.0` + GitHub Release, CHANGELOG [0.2.0] 정리 ② DB: 미적용 llm 마이그레이션 6개 push + 프로덕션 재조회 검증(AI 질문 3행·llmloop 규칙 2행 dev와 완전 일치, 템플릿 멱등 확인) ③ 엣지함수: 프로덕션 슬러그 5종(coginsight-generator·admin-questions·admin-results·admin-solution-rules·results) 배포 + **프로덕션 스모크 생성 1회 전수 통과**(chained 2·guarded 1, 결과는 검증 후 삭제) ④ 프론트: Vercel 자동 배포, 번들 v0.2.0 확인.
- 📄 **머지 후 dev 리셋 완료(규약)**: dev_questions·dev_solution_rules를 프로덕션 미러로 재시드(diff 0 검증), dev_coginsight_results 비움. ⚠ 질문 id가 재발급됨 — 이후 dev 테스트 요청은 새 id 기준.
- 📄 **규모**: 총 **662 커밋**, 마이그레이션 63(전부 적용), 엣지함수 26(프로덕션 21 + dev 5), solution_rules 8 카테고리(prod 30행 = dev).
- 🧠 남은 결: **런타임 검증**(CogInsight 솔루션에 올려 llmloop 대화 동작 — apiKey·model·docsearch storeId는 사용자가 직접 입력), 규칙·학습자료 운영형 보강, 변수/JSON 출력 처리 고도화(v0.1.0부터의 과제), 수집형 체인의 분기·이탈 tool(~~v0.3 후보~~ → 백로그. 📄 2026-07-06 사용자 확정으로 **v0.3.0 = 시나리오 라이브러리** — 아래 [[#로드맵 — v0.3.0 (계획): 시나리오 레퍼런스 라이브러리 테스트·고도화|로드맵]]).

> [!note] 다음 버전 계획 (2026-07-20 브레인스토밍 → 2026-07-21 v0.5.0·v0.6.0 확정 → 2026-07-29 v0.6.0/v0.7.0 재편 + v0.8.0 NLP 추가 — SoT는 저장소 `ROADMAP.md`)
> 📄 **v0.5.0 (계획) = 입력 소스 다양화** — 설문 폼 한 입구에만 의존하던 생성을, 사용자가 이미 가진 산출물·자연어로도 솔루션 업로드 결과를 만들 수 있게 확장. 4개 항목:
> 1. **엑셀 → 업로드용 CSV 변환** (형식 맞춰 정제·다운로드). 🔶 진행 중 — 변환 화면 구현 + **ESD 스키마 JSON 동시 산출**까지 dev 브랜치 완료(2026-07-23, 미릴리스). 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-07-23]].
> 2. **API 인터페이스 문서 → 업로드용 JSON** (명세 해석·필드 추출).
> 3. **POC 문서(시나리오 정의서·흐름도) → 챗봇 생성** (문서 파싱·플로우 매핑).
> 4. **자연어 시나리오 생성** (설문 값 대체 경로, 생성 규칙 `solution_rules` 준수).
> 🔶 **v0.6.0 (개발 중, 2026-07-31 착수) = ESD 선행 생성 & 매핑 기반 설정** — 생성 파이프라인을 "ESD(데이터/서비스 정의) 선행 → 그 ESD 기반 매핑 설정 → 생성"으로 재편. **⚠ 2026-07-31 아키텍처 전환**: 2026-07-29 원설계의 "새 `esd` 테이블 저장소"를 **폐기**하고 ESD를 **생성 결과 번들**(`coginsight_results.generation_tiers.esd`, 신규 컬럼 없음)로 저장 — "선행"은 저장 라이브러리가 아니라 **생성 마법사의 세션 단계**. ESD 미연결 시 기존 경로 완전 무변경(**회귀 없음 = 핵심 불변식**). 블록 A(선행 저작·검증)/D(입력 강화)/B+C(매핑) 3블록. SoT는 저장소 `docs/superpowers/specs/2026-07-31-v0.6.0-esd-frontstage-mapping-design.md`.
> 📄 **v0.7.0 (계획) = 생성 결과 수정 + 문서→ESD 파싱 견고화** (2026-07-29 확정, 기존 v0.6.0 자연어 수정 흡수·확장) — 생성된 flow/`generated_json`을 세 방식으로 수정: ①자연어 지시 ②설문 기반(원설문 항목 편집→반영) ③다이얼로그 기반(대화형 부분 편집). 전체 재생성 vs 부분 패치·불변식(`checkBot`) 재검증·수정 이력(diff)은 착수 시 결정. v0.4.0 다이어그램 편집(백로그)과 상보적. **+ 블록 E(2026-07-31 추가 → ✅ 2026-08-05 dev 구현 완료)**: v0.6.0 코드리뷰·QA에서 드러난 **문서(엑셀)→ESD 자동생성의 조용한 오판·데이터 유실** 개선(시트 선택 부재·헤더 행 1행 고정·중복/빈 헤더 덮어쓰기·예약열 무안내 제외 등) — QA 세트 11파일 실측으로 12건 수정, 브랜치 `fix/convert-esd-qa-hardening` `7bfe07b`(프로덕션 무배포). 상세는 [[#진행사항 업데이트 로그|진행 로그 2026-08-05]].
> 📄 **v0.8.0 (계획) = NLP 생성 & NLP 기준 조건 설정** (2026-07-29 확정) — 인텐트·엔티티·어터런스로 된 **NLP(NLU 학습) 산출물을 CSV로 생성**해 솔루션 시스템에 업로드하고, 생성 시 플로우 조건을 **발화(utterance) 매칭이 아니라 그 인텐트/엔티티에 바인딩**한다. ESD가 데이터 계약이면 NLP는 발화 이해 계약 — v0.6.0 엔티티와 상보적. CSV 스키마·어터런스 생성 기준·런타임 조건 계약 정합은 착수 시 결정.
> 🧠 **장기 방향(버전 미정)**: 2026-07-20 브레인스토밍의 **"순차 플로우 → LLM 주도 상황 적응형 생성"** 3항목(① LLM 노드 상황 적응형 진행 = `llmFlowChain`을 단일 agentic 노드로 일반화 ② 컨디션 노드를 진입 라우팅 전용으로 ③ 라이브러리 기반 생성 UX)은 v0.6.0/v0.7.0 확정에 따라 버전 미배정 백로그로 유지(저장소 ROADMAP "장기 방향" 절).
> 📄 **운영 방침(2026-07-29, v0.8.0 추가로 갱신)**: 확정 버전은 v0.6.0/v0.7.0/v0.8.0 셋만 유지. 단 개발 중 **볼륨 여유가 있으면 백로그 항목을 하나씩 해당 버전 스코프에 포함**(상보적인 것 우선 — 예: 다이얼로그 수정 ↔ 다이어그램 편집).

## 공개 배포 — 개요·매뉴얼 페이지 (운영 SoP)
> 📄 이 프로젝트의 **"개요 및 매뉴얼" 한 장짜리 문서**를 공개 웹페이지로 배포해 둠. **이 문서 내용을 수정·반영하라고 하면 → 아래 공개 페이지에 재배포**한다(사용자 지시, 2026-06-30).

- 🌐 **공개 URL (무계정 열람·공유용)**: **https://coginsight-overview.vercel.app** — Claude 무관 정적 호스팅. 자기완결 HTML(이미지·CSS·JS 전부 내장).
  - ⚠ 긴 배포-전용 URL(`coginsight-overview-xxxx-...vercel.app`)은 Vercel 보호(302)로 막힘 → **반드시 짧은 `coginsight-overview.vercel.app`만 공유**.
- 🧩 **원본(편집용)**: claude.ai 아티팩트 `https://claude.ai/code/artifact/1e30660a-4c19-4a59-9f19-198bed774f7d` (단일 HTML, 개요/사용매뉴얼/관리자 3탭).
- 🎨 **파비콘**: 배포 디렉토리에 `favicon.svg`(워드마크 브랜드 마크 = 검정 라운드 사각형 `#11162A` + 앰버 가로바 `#B5701B` + 흰 세로바)를 두고, head에 `<link rel="icon" type="image/svg+xml" href="/favicon.svg">`. **재배포 디렉토리엔 `index.html`과 `favicon.svg` 둘 다** 있어야 한다(스크래치패드는 세션 임시 → 새 세션은 아래 원본으로 favicon.svg 재생성).
  ```svg
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-label="CogInsight">
    <rect width="32" height="32" rx="10" fill="#11162A"/>
    <rect x="7" y="10" width="13.5" height="4.2" rx="2" fill="#B5701B"/>
    <rect x="13" y="10" width="4.2" height="13.5" rx="2" fill="#FFFFFF"/>
  </svg>
  ```
- 🛠 **재배포 절차** (📄 확인된 동작):
  1. HTML 수정(스크래치패드 작업본 또는 아티팩트 갱신).
  2. `index.html`로 복사한 배포 디렉토리에서 `vercel deploy --prod` (Vercel 계정 `qtw9723`, 프로젝트 **`coginsight-overview`**).
  3. `curl -s -o /dev/null -w "%{http_code}" https://coginsight-overview.vercel.app` 가 **200**인지 확인(인증 벽 없음).
  4. 같은 변경을 claude.ai 아티팩트에도 반영(`url=` 동일 아티팩트로 재배포)하면 원본·공개본 동기화. **이 단계 생략 금지** — v0.4.0·v0.4.1 때 이 단계를 빼먹어 아티팩트가 v0.3.0로 드리프트했다(2026-07-20에 재동기화로 해소). 아티팩트 갤러리 파비콘은 **📊로 고정**(Vercel용 SVG 파비콘과 별개).
- 📸 **매뉴얼 스크린샷 재촬영 절차**(📄 2026-08-03 확립, 2026-07-03 패턴 일반화): UI 개편 릴리스(v0.5.1 앱 셸 등) 뒤에는 매뉴얼 캡처가 전부 낡으므로 함께 다시 찍는다.
  1. 사용자 Chrome 프로필의 `Local Storage`·`Cookies`를 임시 디렉토리로 복사(`Local Storage/leveldb/LOCK` 삭제) → `--headless=new --remote-debugging-port=9223 --user-data-dir=<임시>`로 별도 Chrome 기동(테스터·admin 세션이 그대로 살아 있음).
  2. **무의존 CDP 드라이버**로 캡처(Node 25는 `WebSocket`이 내장이라 playwright 설치 불필요) — `Page.navigate` → 대기 → `Runtime.evaluate`(폼 채움·마스킹) → `Emulation.setDeviceMetricsOverride`(1440@2x) → `Page.captureScreenshot`.
  3. ⚠ `captureBeyondViewport:true`는 뷰포트 높이를 무시하고 **전체 페이지**를 담는다 — 긴 목록은 `clip:{x,y,width,height,scale}`로 상단만 잘라야 페이지가 비대해지지 않는다.
  4. 로그인 화면은 **세션 없는 깨끗한 프로필**(다른 포트)로 별도 촬영.
  5. 🔒 공개 문서이므로 캡처 직전 JS로 이메일 등 PII를 `t****@도메인`으로 치환(사용자 방침, 2026-08-03).
  6. `sips`로 폭 1440·JPEG q≈58 변환 후 base64 임베드(macOS 기본 도구만 사용 — PIL·ImageMagick 없음). 페이지 총량 2.5MB 내 목표.
  6-1. ⚠ **여백·잘림 절충**: 콘텐츠 하단 실측으로 잘라내되 **최소 높이 900px**은 유지한다(더 낮추면 사이드바 메뉴가 접혀 앱 셸이 잘린 것처럼 보인다). 실측 시 `visibility:hidden` 요소(숨긴 피드백 버튼)는 박스가 남으니 제외.
  6-2. 🔒 **마스킹은 이메일만으로 부족**: 참고자료·피드백 화면에 **고객사명·작성자 실명**이 노출된다 → 리터럴 치환 목록을 캡처 스크립트에 두고, 캡션에 마스킹 사실을 적는다.
  7. **캡처 후 프로필 사본 즉시 삭제 + 헤드리스 Chrome 종료**(쿠키 잔존 금지). 드라이버 원본은 세션 스크래치패드 `shots/cdp.mjs`.
- ⚠ **모든 탭 검토**: 문서는 `개요`·`사용 매뉴얼`·`관리자` 3탭이다. 버전/기능 반영 시 **개요 탭만 고치지 말고 매뉴얼·관리자 탭도 해당 기능을 반영**할 것. (v0.4.0·v0.4.1은 개요 탭만 갱신돼 매뉴얼이 v0.3.0에 멈춰 있었음 → 2026-07-20 보강. 위 진행 로그 참고.)
- 🧠 수정 시 **아래 버전 히스토리 표 + 공개 페이지의 "버전 히스토리" 섹션**을 함께 갱신한다(둘이 mirror).
- 📄 (2026-07-03) **본문을 v0.2.0 기준으로 개정**: 히어로 배지·통계(662커밋·26함수·63마이그레이션)·파이프라인 rail/표에 Stage 3.65/3.7/3.75 추가, 신규 섹션 "v0.2.0 — AI 자유응답(LLM 노드)"(지식소스 표·시나리오별 LLM·생성 후 키 입력 안내), 매뉴얼 A-2(AI 설문 항목)·A-5(파일명 coginsight-봇이름.json·키 입력) 보강. 아티팩트 원본도 동기화.

### 버전 히스토리 (문서·릴리스 기준선)
새 버전을 동결/배포할 때마다 **이 표**와 **공개 페이지의 버전 히스토리 섹션**에 한 줄씩 추가한다.

| 버전 | 날짜 | 기준선 | 핵심 내용 |
|---|---|---|---|
| **v0.9.0** | 2026-08-28 | main `99e8705` · PR #120 · tag v0.9.0 · 1075커밋 · 신규 함수 1종 | **기존 챗봇 업로드 후 수정 + 자산 역파생** — Added: 업로드 화면(`/upload`)·`results` POST·구조 검사기(`inspectUploadedBot` — **진짜 파손만 차단**, 미지 타입은 정보로만)·노드 타입 레지스트리(`nodeTypeRegistry` **화이트리스트**)·`flowToScenarios`(설문 없이 flow에서 시나리오 역추출)·신규 엣지함수 `derive-assets`(NLU·ESD 역파생, `generated_json` 무접촉). **핵심 불변식 = 왕복 무손실** — 원본 사본을 따로 두지 않고 `generated_json`이 곧 원본, 편집은 델타 패치로만. 회귀 3종(무편집 왕복·한 노드만 편집·잠긴 노드 필드 보존) × 실제 운영봇 4 fixture. 🐛 **그 게이트가 실제 버그를 잡았다**: `deriveStructure`가 label이 빈 노드에 표시용 기본값(`set`→"저장")을 채워 캔버스로 보내는데 `canvasToFlow`가 그걸 flow에 되썼다 — Cogi 봇은 label이 늘 차 있어 안 드러났고 실제 운영봇에서 즉시 재현. 🐛 `node.body`가 Cogi는 **객체 배열**, 솔루션은 **id 문자열 배열**이라 type 없는 '노드' 8건 발생 → 객체만 노드로 세고 문자열은 참조로 검사. ⚠ **측정 정정**: 최초 "미지 37종(74%)"은 **config 항목 타입을 노드로 잘못 센 결과**였다(dialog JSON의 `type`은 노드/항목 두 층). 정확히는 **노드 21종 · 편집 8종 · 잠김 13종**이고 생성기 파생 스펙도 21종으로 **정확히 일치**(정의 못 한 노드 0종). 재현 스크립트 `scripts/node-type-coverage.ts` 신설. 잠금 사유 분류(사용자 확인): **솔루션 저장 자원 참조**(component·docsearch·agent·campaign — 고치면 없는 자원을 가리키고 Cogi는 목록을 알 방법이 없다) / **편집할 내용 없음**(group=화면 묶음, welcome·anythingelse) / **제외**(task). 잠긴 노드도 **내용은 타입별 서술자로 읽기 좋게 표시**하고 **이름은 항상 편집**된다. 자연어·대화형 수정은 열어두되 **전체 재생성(replace_flow) 확정만 차단**(부분 패치는 applyEditPatch라 무손실). 설문 기반 수정은 원설문이 없어 **숨김**. 부채 정리 앞당김(v0.11.0 항목1): `UploadZone` 로컬 복제 제거(같은 파일 재선택 무시 버그 동반 해결)·다운로드 6곳 → `downloadFile.js`·규칙 카테고리 3곳 → `_shared/solutionRuleCategories.ts`. ⚠ **그 복제는 이미 어긋나 있었다** — learn 쪽이 7종에 머물러 학습이 `Loop Rule`·`NLP Function Reference`를 유효하지 않다고 판단했고, **테스트가 그 어긋난 값을 고정**하고 있었다. DB 무변경. 프로덕션 함수 5종 배포(results·derive-assets·coginsight-generator·admin-solution-rules·learn-solution-rules). 검증: build green · deno 802(프론트)/327(생성기) · `deno check` 클린 · dev 실측(`dc123465`: 실제 운영봇 업로드→NLU 13종/어터런스 296→ESD 5종→**`generated_json` sha256 동일·변형 노드 0**) · Vercel·사내 3006 번들 해시 `index-3yW2xqM8.js` 동일. |
| **v0.8.1** | 2026-08-28 | main `91628fb` · PR #119 · tag v0.8.1 · 1038커밋 | **NLU 기준 조건 설정(진입 `intent()` · 발화 분기 `entity()`)** — Changed: 인텐트명을 **시나리오명으로 결정론 고정**(`intentNameOf` — 한글·영문·숫자만 남김, `"A/S 접수"`→`AS접수`, 밑줄도 제거해 중복 접미사 `_2`와 구분). v0.8.0 실측에서 시나리오 "매장예약"에 LLM이 "예약하기"를 붙여 조건이 시나리오를 지목할 방법이 없었다. **NLP 파생을 `fillNodeValues` 앞으로 이동**(조건 패스가 이름을 참조해야 함 — 입력이 `collectScenarioDetails(responses)`라 플로우 결과에 의존하지 않아 이동 가능. 대신 파생 ESD 대신 선행 확정 `esdBundle.entities` 사용). 조건 프롬프트가 이름을 **"고르지" 않고 "복사"** 하게 — 루트별 `→ condition: intent("…")`를 미리 제시(`intentByRootId`). **루트↔시나리오 대응 3단 보강**(`resolveRootScenarioNames`: 태그 → 라벨 매칭(후보 정확히 1개일 때만) → 순서 짝짓기(개수 정확히 같을 때만) — 어긋나면 짝짓지 않고 비운다. 실측에서 태그가 0건인 봇이 나왔다). `NLP Function Reference`를 condition 단계에 매핑(v0.8.0의 미매핑 고정 테스트를 매핑 확인으로 반전) · 하드코딩 `[CogInsight 술어]` 줄을 `solution_rules`로 이관. Fixed: **NLP 파생 실패 시 발화 매칭 폴백**(파생 실패면 `intents.csv` 자체가 없어 학습 인텐트 0개 봇이 아예 진입 불가 — 무해 계약이 말만 남는 상태였다) / **분기 자식 조건이 통째로 비던 결함**(분기 정보가 NLP 파생에 미전달 → 분류 엔티티 미생성 → "목록에 없으면 발화로 가르지 마라"가 '아무것도 안 채움'이 됨. dev 3봇 중 2봇) / **증상 발화 오분류**("세탁기가 안 돌아가요"→FAQ. 예문 24개가 전부 기능 단어 명시. 1/3 이상을 기능 단어 없는 상황·증상 서술로 강제) / **프롬프트 예시가 주입되는 DB 규칙과 정면 충돌**(규칙은 "조건에서 `_result` 금지"인데 예시는 `_result != null` 권장). ⚠ **전제 변화: NLU CSV 미업로드 시 시나리오 진입 불가.** **🔬 실봇 검증(이번 릴리스 핵심)** — 가전 A/S 봇을 솔루션에 업로드해 대화로 확인, 런타임이 `intent()`·`entity()` 정상 평가. 결함 2건은 **생성물 구조가 완전히 정상이라 빌드·단위 테스트·dev 실측으로 안 잡히고 실봇에서만** 드러났다. DB: 마이그레이션 2건(버전 무관 — 아래 규칙 변경). 프로덕션 함수 1종 배포. 검증: build green · deno 700(프론트)/327(생성기) · `deno check` 클린 · dev 실측 **봇 4종·10회**(루트 13개 전부 `intent()`+이름 일치, `entity()` 분기 8건 전부 번들 존재, 조건에 `input.text` 0건) · Vercel·사내 3006 번들 해시 `index-Cn3xbTyN.js` 동일. |
| **v0.8.0** | 2026-08-28 | main `668e3a7` · PR #118 · tag v0.8.0 · 1015커밋 | **NLU 학습 데이터(인텐트·엔티티) 생성 + CSV 다운로드** — Added: 파이프라인에 `deriveNlpData` 단계 신설(기존 `deriveEsdSchemas`·`deriveApiDefs`와 같은 자리, `fillNodeValues` 이후, LLM 1회 호출로 인텐트·엔티티 동시 수신). try/catch로 감싸 **실패해도 봇 생성은 무해하게 완료**(`generation_tiers.nlp_error`에 사유만). 모델은 **인텐트 = 시나리오 1:1(대분류), 엔티티 = 세부 구분**(사용자 확정) — 사용자 제공 샘플(`intent 매장정보` + `entity 정보`)이 이미 이 구조였다. CSV 직렬화는 `src/lib/nlp/{nlpCsvRules,toNlpCsv}.js`(순수) — 샘플을 **바이트 단위 실측**한 규격 그대로 UTF-8 BOM·LF·전 셀 인용·후행 개행 없음, `intents.csv` 2컬럼 / `entities.csv` **13컬럼 고정**(entity·value·type + 동의어 10칸). ⚠ 기존 ESD 업로드 CSV(`uploadCsvRules.js`)는 **BOM 없음**이 사양이라 상수를 공유하지 않는다. 어터런스 규격(2026-08-28 확정): 인텐트당 **20~30개**, **인텐트 예문은 오타 없이** 말투·문형(명령형·의문형·명사구·구어·존댓말/반말)으로 다양성 확보, **오타·자모 변형은 엔티티 동의어에만**(샘플 관행과 동일: `윛치`·`저나번호`·`addres`), 같은 문장 틀에 숫자·값만 바꿔 개수 채우기 금지(dev 실측에서 `예약번호 <숫자>` 12개가 나와 추가), 동의어 value당 10개 상한(13컬럼 절단을 사후 경고가 아니라 사전 예방). DB: `NLP Function Reference` 카테고리 + 함수 규약 5행(`intent`/`intents`/`entity`/`entities`/와일드카드) 등록 — **참조 전용, `RULE_STAGE_BY_CATEGORY` 미매핑이라 어느 프롬프트에도 미주입**(테스트로 고정). 조건 전환은 v0.8.1. ⚠ **`generated_json` 스키마 무변경** — 솔루션 임포터가 미지 필드를 거부하므로 산출물은 `generation_tiers.nlp` 번들에만(회귀 가드). 부수: `VITE_SUPABASE_SERVICE_ROLE_KEY` 폐기(코드 참조 0건인데 문서 6곳이 "Vercel에 서비스 롤 키를 VITE_ 변수로 등록"을 안내 — 따르면 번들 유출). 프로덕션 함수 1종 배포(coginsight-generator). 검증: build green · deno 700(프론트)/283(생성기) · dev 실측 2회(`cd996b17`·`a0acd4aa` — 인텐트 24/24/24개·중복 0·오타 0, 동의어 10개 상한 준수·CSV 절단 0건) · Vercel·사내 3006 번들 해시 `index-BkNMK3KF.js` 동일. |
| **v0.7.1** | 2026-08-27 | main `7c9545c` · PR #117 · tag v0.7.1 · 963커밋 | **설문 기반 수정 버그 + 생성 소요 시간** — Fixed: `ResultSurveyEdit`가 `QuestionCard`에 질문을 날것으로 넘겨 `input_type==='templated' && question.template` 분기가 조용히 실패(질문 목록은 `template_id`만 주고 템플릿 본문은 `TemplatesContext`에 별도) → 시나리오 입력이 `[object Object]`로 표시. **표시만의 문제가 아니었음** — `validateAllRequired`의 TEMPLATED 분기도 같은 `q.template`에 의존해 `validateScenarios`가 **한 번도 실행되지 않음**(시나리오 이름·진입 발화가 비어도 재생성 통과 = 조용한 검증 누락). 생성 설문(`QuestionnaireForm`)에는 인라인으로 있던 결합을 새 소비처에서 빠뜨린 것이 원인 → 순수 헬퍼 `attachTemplate`으로 추출해 양쪽 공유. Added: **생성 소요 시간**(`generation_tiers.usage.duration_ms`) — 결과 상세 "LLM 사용량"에 `· 생성 시간 25.2초`, 측정 범위는 엣지함수 진입~저장 직전(서버 시간, 네트워크 왕복 제외, 줄 `title`로 명시). `serializeUsage` 3번째 인자 선택적이라 기존 호출부 무변경, 값 없으면 키 미생성 → **측정 이전 결과 78건은 UI가 줄을 숨김**(0초 표시는 거짓). **DB·마이그레이션 무변경**. 프로덕션 함수 1종 배포(coginsight-generator). 검증: build green · deno 678(프론트)/258(생성기) · `deno check` 클린 · dev 실측 후 프로덕션 배포(Vercel·사내 3006 번들 해시 `index-BCninRgV.js` 동일). |
| **v0.7.0** | 2026-08-27 | main `b43d897` · PR #116 · tag v0.7.0 · 959커밋 | **생성 결과 수정 + 다이어그램 편집 + 시나리오 표기·분기 안전장치** — ① **결과 수정 3방식**: 자연어 지시(`result-edit-parse`, 부분 패치/재생성 + 미리보기 후 확정 + `edit_history` 되돌리기)·설문 재편집(`ResultSurveyEdit`)·대화형(`ResultDialogEdit`), 결과 ESD·API 편집. ② **다이어그램 편집**: 노드 추가(실사용 8종)·삭제·연결(`canvasToFlow` 역반영), 타입별 노드 내용 편집(`NodeEditor`), 연결선 조건 가이드 빌더(`EdgeConditionEditor`), 반복 본문 편집, 재검증 5종(조건식 문법·미정의 변수·고립 노드·미완성 신규 노드·모호 분기). ③ **시나리오 표기**: LLM이 FlowSpec 진입 노드에 `scenarioName` 태깅(입력 이름 있으면 verbatim) → `generation_tiers.scenarios`, 프론트 3단 폴백(번들→조건 파생→루트 라벨)이라 **기존 결과도 즉시 개선**, 구조도·흐름도 이름 통일, 진입 조건을 루트 노드에 표시. ④ **분기 안전장치**: 조건 없는 갈래 1개는 `그 외`로 표기, **런타임이 `then` 순서대로 조건 확인**(2026-08-27 사용자 확인)이라 else를 항상 마지막으로 결정론 정렬(생성기 `guardApiResults` 뒤 + 편집기 진입/편집 시), 조건 없는 시나리오 루트 경고. ⑤ 문서→ESD QA 12건(PR #115, 중복·병합 헤더 데이터 소실 등). ⚠ **`generated_json` 스키마 무변경** — 솔루션 임포터가 미지 필드를 거부하므로 이름은 번들에만(회귀 가드 테스트). **DB·마이그레이션 무변경**. 프로덕션 함수 5종 배포(coginsight-generator·results·admin-results·result-edit-parse·nl-scenario-parse). 검증: build green · deno 664(프론트)/255(생성기) · `deno check` 클린 · dev 실측 생성 2회. |
| **v0.6.0** | 2026-08-04 | main `1e5d53d` · PR #114 · tag v0.6.0 | **ESD·API 선행 정의·매핑 + 멀티파일 지능형 수집** — 생성 앞단에 ESD(스키마)·API를 먼저 확정하는 선택적 단계(`EsdFrontStage`, 옵트인 토글 "ESD 및 API 먼저 정의", 기본 off·기존 경로 회귀 없음), 확정 ESD·API를 생성기에 인-프롬프트 주입해 변수·멘트 매핑에 실사용(`proposeMapping`) + 옵션 생성 전 2-pass 매핑 확정(`MappingStep`·`EsdMappingView`). ESD는 별도 테이블 없이 결과(`generation_tiers.esd`)에 번들(`results` PATCH). **멀티파일 지능형 수집**(`MultiFileUpload`) — ESD·API·시나리오 파일을 한 번에 올려 확장자+내용 휴리스틱(모호 시 LLM `ingest-classify`)으로 자동 분류·배지 재지정·라우팅, API 문서는 하이브리드(OpenAPI 결정론 + `api-doc-parse` LLM 폴백)로 `api_def` 추출(`.json/.yaml/.pdf/.xlsx/.csv/.md/.txt`). 편집기 용어 통일 "ESD 편집"→"**ESD·API 편집**"·"엔티티"→"**스키마**". Fixed(기능 검증에서 발견): `.json/.yaml` 텍스트 추출 불가로 OpenAPI JSON API 인입 실패 / CSV cp1252 오독으로 한글 필드명 깨짐 → 둘 다 수정. DB: 규칙 마이그레이션 `20260731130000_mapping_rules`(매핑 지침 3종, 버전 무관). 프로덕션 함수 4종 배포(coginsight-generator·results·ingest-classify·api-doc-parse). 검증: build green · deno 358/0 · dev 기능 검증 실측(멀티파일 분류·하이브리드 API 추출·한글 CSV). |
| **v0.5.1** | 2026-07-29 | main `345fa96` · PR #113 · tag v0.5.1 · 868커밋 | **UI/UX 개편 + 문서→API 도구화** — 헤더 nav → **그룹형 사이드바 앱 셸**(`AppShell`/`Sidebar`, 생성·부가도구 그룹, 접기/펼치기 `localStorage.sidebarCollapsed`, 레일 툴팁, 버전 배지 좌하단→우상단), 라우팅 개편(`/`=자연어 생성 기본·`/survey`=설문·`/nl`→`/` 리다이렉트·`/doc` 사이드바 승격·`/api` 신규), 모든 생성 동작에 **전역 로딩 오버레이**(`LoadingProvider`). 신규 **문서→API 생성 도구**(`/api`, `ApiGenPage`) — 한 문서에서 여러 `api_def`를 하이브리드 추출(`parseApiDocToDefs` OpenAPI 결정론 파서 우선 → 신규 LLM 엣지함수 `api-doc-parse` 폴백). Fixed: Tailwind v4가 `tailwind.config.js` 색상을 못 읽어 생긴 투명 버튼(`@theme`에 primary 스케일 정의). **DB·마이그레이션·`solution_rules` 무변경**. 검증: build green. |
| **v0.5.0** | 2026-07-28 | main `1e3237d` · PR #111 · tag v0.5.0 | **입력 소스 다양화** — 설문 폼 하나뿐이던 생성 입구를 4갈래로 확장: ① 엑셀(.xlsx/.csv)→ESD 업로드 CSV·스키마 JSON(`/convert`) ② API 인터페이스 문서(OpenAPI)→`api_def`(어드민 레퍼런스 등록) ③ 자연어→시나리오(`/nl`) ④ POC 문서(엑셀·PDF·MD·txt)→챗봇 생성(설문화면 "POC 문서로 생성"). ③④는 신규 `-dev` 엣지함수 2종(`poc-doc-parse`·`nl-scenario-parse`, prod 슬러그 동반, `src/lib/pocDoc` 순수모듈 공유). **DB·마이그레이션·`solution_rules` 무변경**. 검증: build green·deno 247/0. |
| **v0.4.2** | 2026-07-21 | main `2986e1f` · PR #108 · tag v0.4.2 · 802커밋 | **결과 확인 창 UI 개선** — 결과 상세(`/results/:id`)의 `입력한 응답` 시나리오를 이름 헤더 카드로 구분·접기(기본 접힘), 상단 요약 헤더(봇 이름 + 메타 칩)·섹션 바로가기 추가, 버튼 색 `#0052CC` 통일. 메타 계산 `utils/resultMeta.js` 공용화. 프론트 전용. |
| **v0.4.1** | 2026-07-15 | main `3b68501` · PR #107 · tag v0.4.1 | **결과 탭 사용자별 보기** — `/results`(`ResultsList`)에 사용자 필터 드롭다운(전체/각 `created_by`, 없으면 '(미상)') + "사용자별로 묶어 보기" 그룹 토글(사용자 이름순 섹션 헤더). 기존 검색·정렬과 함께 동작. 프론트 전용, main 직접 릴리스(카테고리 기준은 제외 — 사용자만). |
| **v0.4.0** | 2026-07-15 | main `52a0f59` · PR #106 · tag v0.4.0 · 795커밋 | **플로우 시각화** — react-flow(`@xyflow/react` v12 + `@dagrejs/dagre`) 캔버스 뷰어: 구조 다이어그램 + 사용자 흐름도 2뷰 토글, PNG 내보내기·풀스크린(뷰포트 보존)·팬/줌. **진입점 4곳**: 설문 시드카드·라이브러리(레퍼런스, [[올림푸스-Olympus]] 자율 개발) + **생성 결과 상세·목록 모달**. 구조 뷰: 표준 플로우차트 도형·범례, 라벨 호버, 분기 조건, 시나리오=단일 흐름(반복 구획화·`__init` 브리지), 드래그·패닝, **턴 교대(⏳ 응답 대기)**. 사용자 흐름도: 시나리오별 목록·전문·턴 교대. **프론트 전용**(Vercel 자동 배포). 검증: deno 260/0·build green. 잔여(v0.5): 편집 역반영·DRY 추출·중첩 반복·이미지 외 내보내기. |
| **v0.3.1** | 2026-07-09 | main `4429c25` · PR #105 · tag v0.3.1 | **LLM 모델 gpt-4o → gpt-5.2** — 생성기 백엔드 5개 엣지함수 전부 전환 + OpenAI 키 로테이션(Supabase 시크릿 `OPENAI_API_KEY`, 구 키 revoke는 계정 측 조치). v0.4.0 dev 사이클과 무관한 독립 패치(격리 브랜치 `fix/llm-gpt-5.2`). 검증: OpenAI 200, flow 테스트 54 green. ⚠ `flow/usage.ts` 단가표 미갱신 → `estimated_cost_usd` 부정확(gpt-5.2 실단가 확인 후 갱신 TODO). |
| **v0.3.0** | 2026-07-09 | main `ae99f4d` · PR #103 · tag v0.3.0 · 741커밋 | **시나리오 레퍼런스 라이브러리 테스트·고도화** — 레퍼런스 6종 등록·few-shot 실검증, 구조 시드(STAGE 3.68)·시드 UX·피드백 스크린샷(Storage 전환·보존 정책), 생성 관측성·회귀 하네스, **조립 57조합 전수 검증(루프 body 버그 수정)**. 릴리스 검증: deno 233·하네스 4/4·프로덕션 스모크 통과. 레퍼런스 5종 승격(도매 제외). 잔여(항목 4·6)는 백로그. |
| **v0.2.2** | 2026-07-09 | main `9a99e18` · PR #101 · tag v0.2.2 | **프로젝트명 전면 변경 — CogInsight Generator**(구명 사용 불가 판정). 코드·문서 122파일 치환, 엣지함수 슬러그 `coginsight-generator(-dev)` 신규 배포·구 슬러그 삭제, DB 객체(테이블 8·제약 12·인덱스 20·정책 8) rename(라이브 직접 실행), GitHub repo `CogInsight-Generator`, Vercel `coginsight-generator`·`coginsight-overview`(구 URL 폐기). 기능 무변경, deno 210 green. |
| **v0.2.1** | 2026-07-08 | main `46bb57f` · PR #100 · tag v0.2.1 | **ESD 스키마 파생 핫픽스** — `collectEsdFields`가 schemaName을 `config.query.schemaName`에서 읽도록 교정(그전엔 `config.schemaName`만 봐서 ESD 노드 스킵 → `esd_schemas` 항상 빈 배열) + 바인딩된 필드만 수집(레퍼런스 잔재 빈필드 제외). 프로덕션 `coginsight-generator` 재배포, 재생성 검증(id e72f4e26, 상담기록 스키마 정상). deno 223 green. |
| **v0.2.0** | 2026-07-03 | main `36d0181` · 662커밋 · 마이그레이션 63 | **AI 자유응답(LLM 노드) 블록** — 지식소스 3종(문서/일반/혼합) 전역·시나리오별 선택, 시나리오별 LLM(Q&A형 + 수집형 **LLM-구동 플로우 체인**), llmloop 레퍼런스 골격(ask_docs+docsearch 2패스), STAGE 3.65(anythingelse 1회성)·3.75(api 결과 예외 처리) 안전장치, DEV 테이블 모드, apiKey·model·storeId 사용자 입력 불변식. |
| **v0.1.0** | 2026-06-30 | 엣지함수 coginsight-generator **v87** · 610커밋 · 마이그레이션 54 | 프로토타입 동결(SemVer 0.x 시작, tag·GitHub Release). 결정론 생성 안전장치 체인(Stage 2.9~3.6) 완비, API 결과 멘트 노출·placeholder 정리. **첫 보고·테스트 기준선.** |

## 로드맵 (현재) — 2026-08-28 재편

> 📄 **SoT는 저장소 [ROADMAP.md]** — 여기는 미러. 2026-08-28 사용자 확정으로 v1.0.0까지 세움.
> ⚠ 재편 이유: v0.6.0·v0.7.0·v0.8.0이 **모두 태그까지 나갔는데 ROADMAP은 셋 다 "(계획)"** 으로 남아 판단 근거로 쓸 수 없었다. 릴리스 규약을 5단계 → **6단계로 늘려 ⑥ROADMAP 갱신**을 넣어 재발을 막았다.

| 버전 | 내용 | 상태 |
|---|---|---|
| **v0.8.1** | NLP 기준 조건 설정 — 진입 `intent()`, 발화 분기 `entity()` | ✅ 2026-08-28 릴리스 |
| **v0.9.0** | 기존 챗봇 업로드 후 수정 + 자산 역파생 | ✅ 2026-08-28 릴리스 |

| **v0.10.0** | 생성 데이터 관리 & 자산 모듈화 | 계획 |
| **v0.11.0** | 로직 정합화·부채 정리 | 계획 |
| **v0.12.0** | UI 전면 정리 | 계획 |
| **v1.0.0** | 정식화(날짜 아님 — 조건 기준) | 기준 |

**핵심 근거 (📄 2026-08-28 코드·DB 실측)**

- **v0.9.0이 싸게 되는 이유** — 편집 4경로 중 **3개가 `responses` 없이 `generated_json`만으로 동작**한다. 자연어 수정(`result-edit-parse`)은 `{flow, instruction, esd, mode}`만 받아 **결과 행·`reference_id`도 불요**. 설문 기반 수정만 원설문이 없어 불가. → 업로드 봇에 기존 편집 도구를 거의 그대로 붙일 수 있다.
- **v0.9.0의 핵심 불변식 = 왕복 무손실** — 지금까지 "솔루션 임포터가 모르는 필드를 거부한다"가 제약이었는데 여기서는 **Cogi가 임포터 쪽**이 된다. 파싱해 아는 것만 재직렬화하면 운영 봇 설정이 조용히 사라진다. 원본 보존 + 편집 노드만 교체. 📄 운영 리스크 자체는 **사용자가 관리**(받아서 다시 올리는 흐름) — 도구 책임은 "산출물이 정확히 나오는 것" 하나(2026-08-28 사용자 확정).
- **v0.10.0이 필요한 이유** — `generation_tiers`가 스키마 없는 단일 jsonb로 자라 **결과 행마다 내용이 다르다**(프로덕션 40행 표본: `esd_schemas` 19행 / `usage` 18행 / `api_defs` 3행). **중복 지표 쌍이 실재** — `tier3_rules_executed`(수) ↔ `tier3_executed_rules`(배열), `tier3_rules_skipped` ↔ `tier3_skipped_rules`. `flow` ↔ `stage1_flow`도 중복. 스테이지는 함수명 기반으로 전환했는데 **메타데이터 키는 `tier*` 그대로**. 결과 78행에 보존 정책도 없어 테스트 생성물과 실무 산출물이 섞여 있다.
- **v0.12.0이 필요한 이유** — v0.5.1이 앱 셸은 바꿨는데 스타일 체계가 안 따라왔다. **`BTN_PRIMARY`가 4개 파일에 각각 로컬 `const`로 복제**됐고(`ResultDetail`·`ResultSurveyEdit`·`ResultDialogEdit`·`DiagramEditPanel`) **이미 어긋났다** — `BTN_PRIMARY_SM`의 `disabled:opacity-50`이 파일마다 있고 없다. 주 색상 3변형(`#0052CC` 49 / `#0047B3` 22 / `#003d99` 8)으로 hover가 화면마다 다르고, CSS 파일 5개(`src/index.css`와 `src/styles/index.css`가 따로), **어드민 화면군은 디자인 상수 0**.
- **모듈화 시 주의** — 인텐트·엔티티를 **완전히 분리하면 안 된다**. 인텐트 간 예문 중복 금지·분기 분류 엔티티 생성이 전체 그림을 요구하고, 이걸 못 봐서 **분기 조건이 통째로 비는 결함이 v0.8.1에서 실제로 났다**. "엔티티 도구가 인텐트 목록을 입력으로 받는" 순차 의존 구조로.

## 로드맵 (이력) — v0.3.0: 시나리오 레퍼런스 라이브러리 테스트·고도화
> ⚠ 아래는 **2026-07-06 당시 계획 기록**이다(v0.3.0은 2026-07-09 릴리스 완료). 현재 계획은 위 "로드맵 (현재)" 참고.
> 📄 **2026-07-06 사용자 확정**: v0.3.0에서는 **시나리오 라이브러리 기능을 테스트하고 고도화**한다. 현재 레퍼런스가 하나도 등록돼 있지 않아 이 기능으로 테스트된 적이 없고, 조합(조립) 사용 테스트도 미진행 — v0.3.0에서 **시나리오 라이브러리를 활용한 결과 생성**을 테스트한다.
> 📄 저장소에 **`ROADMAP.md` 신설**(+CLAUDE.md 상단 포인터) — PR #99 **머지 완료**(2026-07-06, main `14cca10`, 문서 2파일만·코드 무변경). **저장소 ROADMAP.md가 계획의 SoT.**
> ⚠ 📄 **v0.3.0 작업은 프로덕션 무배포 (2026-07-06 사용자 확정)** — 테스트·고도화 전 과정 **dev 전용**(테스트 브랜치·`dev_` 테이블·`-dev` 슬러그·`VITE_DEV_TABLES=true`). 프로덕션 반영은 사용자가 "프로덕션에 머지"를 명시 요청할 때만(4축 절차). 이번에 배포된 것은 **로드맵 문서뿐**.

**배경 (📄 코드 확인, 2026-07-06)** — 라이브러리는 v0.1.0부터 두 경로로 구현돼 있으나, 레퍼런스 0건이라 둘 다 실데이터 검증이 없음:
1. **생성 파이프라인 few-shot 주입(Mode A)**: 설문 응답에서 산업군(금융/물류/소매/도매/의료/기타) 추출 → `coginsight_scenario_references`에서 사용자 시나리오 이름 관련도 상위 3개 선택 → 보일러플레이트(welcome·anythingelse) 제외한 시나리오 부분을 Stage 1 프롬프트 예시로 주입(`flow/scenarioExamples.ts`). **레퍼런스가 없으면 조용히 skip → 지금까지의 모든 생성은 few-shot 없이 이뤄졌다.**
2. **사용자 라이브러리 `/scenarios`**(`ScenarioLibrary.jsx`): 카테고리별 미니봇 탐색, 단일 다운로드 또는 여러 개 조립(조립 경고 안내 포함).

**작업 항목** (🧠 사용자 목표를 세분화한 제안 — SoT·상세는 저장소 ROADMAP.md. 진행 표시는 2026-07-07 기준 ROADMAP 미러)
1. ✅ **레퍼런스 등록** (2026-07-06, dev) — 산업군별 미니봇 6종 제작(생성기 초안→수동 교정→품질 게이트)·`dev_coginsight_scenario_references` 등록. 프로덕션 승격은 "프로덕션에 머지" 시 선별.
2. ✅ **단일 레퍼런스 생성 테스트** (2026-07-06, dev) — 회귀 하네스 전/후 비교로 3 fixture 전부 `injected` false→true, `rules_hash` 완전 동일(순수 레퍼런스 효과 분리). ⚠ api-esd `placeholder-leak` 신규 1건 → 항목 6 백로그.
3. ✅ **조립(조합) 생성 테스트** (2026-07-09, dev) — 6종 전 조합 57건 전수 `assemble` 실호출 검사(`assembleCheck.ts`). 🐛 **조립기가 루프 body 서브트리를 누락·미재작성하던 실버그 발견·수정**(46/57 FAIL → 수정 후 57/57 PASS) — 아래 [[#진행사항 업데이트 로그|7/9 조립 로그]]. ✅ (2026-07-07 추가 구현, 사용자 제안) 설문에서 레퍼런스 직접 선택 → **구조 시드**(STAGE 3.68 결정론 복제) — 위 [[#진행사항 업데이트 로그|7/7 로그]]. ⚠ 실사용(런타임 로드) 확인은 잔여(사용자 몫).
4. 🔶 **선택 로직 검증** (부분 완료 2026-07-06) — `extractCategory`·`selectExamples`가 3 fixture에서 산업군별 올바른 레퍼런스를 선택함을 확인. 다중 후보(산업군당 2개+) 관련도 스코어 검증은 잔여.
5. **v0.2.0 기능과 결합 회귀** — LLM 노드(지식소스·시나리오별 LLM)·API·ESD 병행 생성(잔여).
6. **고도화** — 누적 백로그(📄 ROADMAP): 라이브러리 **미리보기 부재**(7/7 사용자 피드백 — 다운로드·조립 전 구조 확인 모달 검토) / few-shot 도입 후 placeholder-leak 원인 분석 / 도매 레퍼런스 배열 누적 품질.

**주의·스코프**
- ⚠ `coginsight_scenario_references`는 dev 사본 없는 **프로덕션 공유 테이블**(DEV 규약) — 레퍼런스 등록·변경은 사용자 확인 후 진행.
- 🧠 기존 "v0.3 후보"(수집형 체인 분기·이탈 tool, docsearch·`_llm.tool.name`·`_llm.terminate` 등)는 v0.3.0 스코프 확정에 따라 **백로그(버전 미정)**로 이동.

## 다음 버전 확인·개선 항목 (v0.1.0 이후 백로그)
> 🧠 내부 개발 백로그 — **공개 페이지엔 싣지 않음**(LLM 의존성·무한반복 위험 등은 회사 솔루션 내부·약점이라 공개 부적합). 다음 버전 작업/검증 시 이 목록을 기준선으로 본다.

### ✅ v0.2.0 — AI 자유응답(LLM 노드) 블록 (2026-07-03 프로덕션 릴리스)
> 📄 2026-07-02 하루에 설계→구현→main 머지·릴리스(PR #94~#96)까지 갔다가 **같은 날 PR #97로 전량 롤백**. 프로덕션은 v0.1.0 유지, v0.2.0은 CHANGELOG상 **"미릴리스(dev 테스트 중)"** — v0.2.0 태그 없음. 이후 작업은 `feat/llm-v0.2.0-testing` 브랜치 + dev 환경에 누적.
> 📄 **2026-07-03 릴리스**: 아래 7/3 확장 전부(생성 결함 3건 수정 + 지식소스 + 시나리오별 LLM + LLM-구동 체인 + model 빈 값 + api 예외 처리)를 담아 **프로덕션 릴리스 완료**(tag `v0.2.0`). llm 마이그레이션 6개도 프로덕션 적용·검증 완료.
> 📄 **머지 전 최종 검증 통과 (7/3, dev API 전 기능 매트릭스)**: 시나리오 **6종**(docs/general/mixed+수집·검증루프/LLM 미사용/**API 연동**/**ESD 연동+LLM 결합**) + 전역 "둘 다"(docs)를 한 봇으로 생성해 전수 점검 — 이 과정에서 **메뉴 llmloop 주입이 시나리오 llmloop에 가려지는 결합 버그를 발견·수정**(`9a5e96a`, 시나리오 패스 선행 + 비시나리오 판정). 최종 결과 `8598c9c5`(최종검증봇_v020, llmloop 6개: 시나리오 4+메뉴+폴백, api·esd 노드 각 1) **전 항목 통과** — API 정의(`api_defs`: getMember, URL·${memberId} 바인딩)와 ESD 스키마(`esd_schemas`: 상담기록/memo)는 봇 JSON이 아니라 **generation_tiers의 별도 산출물**(CogInsight import용)로 나가는 설계임을 확인. 이후 **LLM-구동 플로우 체인 규격**(아래 확장 2)과 **STAGE 3.75 api 결과 예외 처리 보장**(`c4b97bf` — 레퍼런스 관용구 [성공 자식(저장 변수 조건)→catch-all 실패 output]을 모든 api 노드에 보장, 재검증 `d7083216` 전수 통과)까지 반영하고, 결과 JSON 다운로드 파일명을 봇 이름 기반(`coginsight-{봇이름}.json`)으로 개선(`87d2a23`)해 최종 홀드 지점 = **`87d2a23`**.

#### 7/3 확장 — 생성 결함 수정 + 지식소스 + 시나리오별 LLM (📄 git log `04ff579`~`3ca4282`, dev 검증 완료)
- 📄 **생성 결함 3건 수정** (`04ff579`, 검증봇_V3 생성물 피드백): ① **anythingelse 1회성 보장** — welcome처럼 다이얼로그당 1개(루트)만 유효. Stage 1 카탈로그에서 제외 + 신규 **STAGE 3.65**(normalizeAnythingElse: 중간 잔존분은 자식 있으면 컨디션 노드로 전환, 없으면 제거). ② **제작 챗봇 정보 prompt 주입** — 설문의 시나리오 상세(진입 발화·수집 항목·완료 결과)를 '챗봇 정보'에 나열 + "기능 요청은 진입 발화로 안내" 지침. ③ **llmloop 레퍼런스 풀 body** — tool `[ask_docs, no_answer]` + body `[ask_docs 핸들러→답변 reset→정보찾기 subdialog(docsearch 2패스)] + [LLM reset(_llm.terminate)→no_answer output]` (한화라이프 봇·LLM 노드 샘플 구조 그대로).
- 📄 **LLM 지식소스 3종 + 시나리오별 LLM** (`ca13dc4`, 설계 spec `docs/superpowers/specs/2026-07-03-llm-knowledge-source-and-scenario-llm-design.md`):
  - **지식소스**: `문서 검색(docs)`=ask_docs 골격+"문서 내용만 근거"(내부 정보 한정) / `일반 LLM(general)`=tool·body 없이 일반 지식 / `혼합(mixed)`=골격+"문서 우선, 없으면 일반 지식 보완". 기본값 general(도구 모르는 잔존 llmloop 포함 — storeId 없는 docsearch 런타임 실패 방지). ⚠ "웹 검색" 논의는 **LLM 일반 답변**을 의미(별도 웹 검색 기능 아님 — 사용자 확인).
  - **시나리오별 LLM (한화 봇 패턴)**: 시나리오 필드 "AI 자유응답 사용=예"면 그 시나리오 흐름 **마지막 잎 output 뒤에** 주제 전담 Q&A llmloop. **하이브리드**: Stage 1 규칙 지시 + STAGE 3.7 결정론 보장(있으면 소스별 정규화, 없으면 주입). 시나리오 식별은 진입 발화 조건 매칭.
  - **설문**: 전역 "AI 지식소스" 질문 + 시나리오 템플릿 필드 2개("AI 자유응답 사용"/"AI 지식소스"). ⚠ 템플릿은 **공유 templates 테이블에 라이브 반영됨**(사용자 승인) — 프로덕션 설문 UI에도 필드 노출(구 프론트는 showWhen 미지원이라 항상 표시, v0.1.0 생성기는 무시하므로 생성 영향 없음).
- 📄 **model도 빈 값 불변식** (`3ca4282`): 키에 따라 쓸 수 있는 모델이 달라 **apiKey·model·(docsearch) storeId 전부 사용자가 CogInsight에서 직접 입력** — 정규화가 model="" 강제(기본값 gpt-4o 주입 제거).
- 📄 **검증**: deno 테스트 183개(신규 ~30개 TDD) + 실데이터(문제났던 coginsight-49420202.json 재통과) + **dev 생성기 API 실호출 2회** — 최종 샘플 `dev_coginsight_results` **09bde7a9**(지식검증봇_V5: FAQ 시나리오=docs 골격+주제 한정 prompt, 폴백=general 도구 없음, model·apiKey 전부 빈 값). Stage 1이 갱신된 규칙만으로 시나리오 끝 llmloop을 스스로 배치한 것도 확인(하이브리드 양 경로 모두 동작).
- 🧠 **머지 후 확인거리(minor)**: Stage 1이 분기·자식에 같은 조건을 중복 부여해 잉여 else 노드가 생기는 사례(도달 불가·무해) / llmloop stream 값이 파생 스펙(false)과 주입(true)에서 불일치.
- 📄 **구현 내용 (PR #94·#95)**: 질문지 "AI 자유응답(LLM) 사용" 선택 시 생성 시나리오에 `llmloop` 노드 보장 — 메뉴형(메뉴 분기 "AI 상담" 주입)·폴백형(anythingelse 안내를 llmloop으로 치환)·둘 다 지원. 신규 결정론 단계 **STAGE 3.7** `flow/applyLlmBlocks.ts`(주입·치환·정규화), Stage 2.5 `FILLABLE_TYPES`에 `llmloop` 허용. DB: AI 자유응답 질문 2행 + llmloop 규칙 2행(Node Usage·Value Generation).
- 📄 **핵심 안전 불변식 (구현됨)**: 모든 llmloop에 `config.apiKey = ""` 강제(레퍼런스 실키 유출 차단) + model/type 기본값·대소문자 교정 + 빈 prompt 템플릿 보충.
- 📄 **DEV 테이블 모드 (7/2 도입)**: `-dev` 슬러그 함수 5개(coginsight-generator·admin-questions·admin-solution-rules·results·admin-results) + `dev_questions`/`dev_solution_rules`/`dev_coginsight_results` + 로컬 프론트 `VITE_DEV_TABLES=true`(버전 배지 DEV 표시). "실행-후-머지" 워크플로우 — 프로덕션 슬러그·테이블 무접촉. 상세 규약은 저장소 `CLAUDE.md` "DEV 워크플로우 규약" 섹션(7/3, SoT).
- 📄 **dev에서 이어진 튜닝 (7/2 오후)**: 폴백 치환 시 output 자식 가진 anythingelse 선택(Stage 1산 빈 anythingelse에 막히던 문제), llmloop prompt 백틱 템플릿 리터럴 정규화, **프롬프트 샘플 섹션 구조**(챗봇 성향/챗봇 정보/응답 지침 — 챗봇 정보 나열 + 시나리오 비답습 지침, dev 규칙에 반영).
- 📄 **범위 밖(v0.3 후보)**: 툴 정의·docsearch·`_llm.tool.name` 분기·`_llm.terminate` 루프 제어.
- ✅ **(해결) 프로덕션 마이그레이션**: llm 마이그레이션 6개 릴리스 때 전부 적용·재조회 검증 완료(UPDATE 체인 no-op 아님 확인, 템플릿 멱등 가드 정상).
- ✅ **(해소 2026-07-08, 사용자 결정) 레퍼런스 상태**: "LLM 노드 샘플 (7/2 발췌)"의 nodeSpecs 파생을 실행 — `derive-node-specs` 호출로 `pending` → `completed`(nodespecs-1, 노드 타입 7종: docsearch·set·group·node·output·llmloop·subdialog, 경고 0, 재조회 검증). 이로써 `coginsight_references` 4건 전부 `completed`.

#### 7/3 확장 2 — LLM-구동 플로우 체인(수집형 LLM 시나리오 새 규격) (📄 `886f55f`, dev 검증 완료)
- 📄 **배경 (사용자 재정의)**: 시나리오 LLM은 "흐름 끝 Q&A 부착"이 아니라 **llmloop이 플로우 자체를 구성** — tool 분기 + body의 set/output으로 기존 결정론 플로우를 구현. 순서 수집은 **항목마다 전담 llmloop**(이름 받는 LLM → 연락처 받는 LLM), 각 단계에 기본 응답(고정 질문)이 있고 답변에 따라 다르게 진행. ⚠ **이 규격은 LLM 노드 내부 진행 시나리오(수집형)에만 적용**(사용자 확정) — Q&A형·미사용·전역은 기존 유지.
- 📄 **체인 규격** (`llmFlowChain.ts`, 설계 spec `2026-07-03-llm-driven-flow-scenarios-design.md`): 항목별 `[기본 응답 output("되묻는 말" 우선) → 수집 판정 llmloop]` 쌍을 then으로 연결. llmloop은 올바른 값이면 `save_{변수명}` tool 호출 → body `[핸들러 node → set(local.{변수명}=_llm.tool.args.{변수명} + _llm.terminate=true)]` → 다음 단계, 아니면 terminate 없음 = 자연 반복(재요청). **형식 검증은 LLM 판정으로 이동**(전화번호 등 prompt+tool 인자 힌트), 필수=반복/선택=빈 값 허용. 원본 api/esd 노드는 보존해 체인 끝 재배선(local 바인딩 호환), 완료 output은 "완료 시 결과"로 생성. 수집형은 지식소스 도구 미부착.
- 📄 **결정론 전담(이 규격 한정 접근 A)**: STAGE 3.7이 수집형 서브트리를 통째 교체(진입만 유지). **루트 부재 보장** 추가: Stage 1이 시나리오를 누락해도 진입 컨디션 노드를 결정론 생성(수집형·Q&A형 공통). Stage 1 카탈로그에서 **docsearch 제외**(llmloop body 전용 — anythingelse 전례).
- 📄 **검증**: deno **197 tests**(체인 빌더 6 + 통합 6 신규) + dev API 매트릭스 `bc678750` — 2단계 체인(이름 필수→연락처 선택·전화번호·되묻는 말) + 상담기록(체인→esd→완료 재배선) + Q&A/미사용/API/ESD/전역 회귀 **전수 통과**. 규칙 2행 갱신(dev 반영 + 마이그레이션 `20260703130000`).

1. 📄 **탈출 set 누락 (LLM 의존, 미해결 — 우선)**: flag 루프의 **구조는 결정론적으로 보장**되지만, **LLM이 본문에 탈출 flag set 자체를 안 만들면 무한 반복**. `normalizeLoopExit`는 *틀린* flag만 고칠 뿐 **없는 set은 만들지 못함**. → 다음 버전 확인: **앱에서 flag 루프 생성 시 본문에 탈출 set이 있는지 여전히 눈으로 확인 필요**. (검증루프·API·ESD는 결정론적이라 항상 안전 — 이 위험은 LLM이 설계하는 flag 루프에 한정.) ↔ 기존 메모 "런타임 탈출 의미 미검증"과 같은 결.
2. 📄 **자동 회귀 검증 부재 (🧠 옵션 2 — 급하지 않음)**: 코드가 바뀔 때마다 polarity·flag 흐름을 **다시 수동 라이브로 확인**해야 함. 지금은 "동작하는 거 확인했다"는 **1회 관측**이라 회귀에 약함. **런타임 평가를 모사하는 시뮬 하네스**가 있으면 자동화됨. → 우선순위 낮음: **루프 로직이 또 크게 흔들릴 때 도입**해도 됨.

🧠 (참고) 위 둘 외 이미 기록된 한계: **변수/JSON 출력 처리 미숙**(JSON 자동 출력 불가→키 직접 지정), 둘 다 위 [[#현재 상태 스냅샷 — v0.1.0 프로토타입 배포 (2026-06-30)|현재 상태 스냅샷]] 한계 참고.

3. ⭐ 🧠 **(2026-08-10 신규) QA 설계 원칙 — 생성 모델과 검증 모델을 분리한다**: 위 1·2번은 *"결정론 코드가 구조를 보장하고, LLM 산출물은 사람이 눈으로 확인"* 구조인데, **LLM에게 검수를 맡기는 방향으로 확장할 때 같은 모델에 자기 산출물을 채점시키면 안 된다.**
   - 📄 근거 ①(실무): [[AI-주간-소식-2026-W33]] (W33-KR13) — 약국 실무 칼럼이 상담 카드를 **제작에 쓰지 않은 다른 AI(예: Claude)로 교차 검증**하는 워크플로를 보도. 규제·안전 도메인의 최소 구현.
   - 📄 근거 ②(논문): [[AI-주간-소식-2026-W32]] ㊴ — Trident·SABRE(*평가자를 피평가자와 분리하지 않으면 견고성은 검증되지 않은 채 남는다*), ㉕·㊲(*판정을 모델 밖으로 · 홀드아웃 채점*).
   - ⚠ 🧠 반대편 제약도 같이 본다: **㉚(멀티에이전트 집단 동조)** 때문에 *"LLM 여러 개 다수결"* 은 게이트로 못 쓴다. 즉 처방은 **다수결이 아니라 「다른 모델 1개 + 결정론 검증」** 조합이다.
   - 🧠 [[웹-크롤링-기초]] 규약 **②-h**가 바로 이 원칙을 안 지켜서 난 사고다(자동 위키화가 자기 요약을 자기가 채점 → 4건 누락을 「처리 완료」로 분류).
   - 🆕 ⭐ **(2026-08-11 추가) 검증자를 여러 개 둘 때의 규칙**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN10) — arXiv:2608.07280 *「창발을 연구할 게 아니라 규제하면 되지 않나」*(보상 예측으로 멀티에이전트 정렬)는 ㉚(집단 동조)에 처음으로 **금지가 아닌 처방 축**을 제시한다. ✅ 그래서 검증자를 2개 이상 둘 경우 **합의(agreement)를 신호로 쓰지 말고, 각 검증자의 판정 기준을 서로 다르게 설계**한다(예: 하나는 스키마·순서 결정론 검증, 하나는 원문↔필드 대조). ⚠ 📄 단 이 논문은 시뮬레이션 도메인이라 LLM 에이전트 직접 이식 근거는 없다 → **미검증 가정으로 표시**.

4. 🆕 ⭐ 🧠 **(2026-08-11 신규) 산출물 수용 기준 = 「편집 가능(editable) + 추적 가능(traceable)」**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN2) — OpenAI 사례(Model ML × GPT-5.6 Sol)가 *리서치·분석 → **편집 가능하고 추적 가능한** PowerPoint 덱·Excel 워크북* 을 제품 문구로 내걸었다.
   - 🧠 [[AI-주간-소식-2026-W32]] ⑯(궤적 기록)·㉟(고정 출력이 아니라 반박 가능한 논증)이 **논문 어휘에서 상용 제품 문구로 굳은 첫 사례**다 — 즉 이건 이제 "연구 아이디어"가 아니라 **경쟁 제품의 기본 사양**이다.
   - ✅ **CogInsight 적용 지점**: 생성된 flow/`generated_json`에 대해 ① **어느 원문 한국어 구절이 어느 필드가 됐는지** 대조 가능(= ㉛의 다국어 손실 구간 방어와 **같은 작업**으로 해결됨) ② 사람이 고친 흔적이 남을 것(v0.7.0 생성 결과 수정 3방식의 **diff·되돌리기** 미확정 항목과 직결).
   - 🧠 즉 v0.7.0에서 *"전체 재생성 vs 부분 패치"* 를 고르는 문제는 **추적 가능성 요구가 답을 좁힌다** — 전체 재생성은 궤적을 끊는다.
   - 🆕 🧠 **(2026-08-12 추가) 「검증·전달·기록」이 산출물 밖의 요구로 확장된다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN24) — arXiv:2602.17902(El Agente Gráfico) *LLM은 워크플로를 계획하고 코드를 생성할 수 있지만, **과학적 상태를 어떻게 검증·전달·기록하는가는 규정하지 않는다***. 🧠 즉 추적 대상은 **최종 산출물만이 아니라 단계 간 실행 상태**다.

5. 🆕 🚨 ⭐ 🧠 **(2026-08-12 신규) 파이프라인의 「단계 사이」도 검사 지점이다 — 노드 분리만으로 부족하다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN17) — arXiv:2607.19430v2 **ChannelGuard: *Safe Models Do Not Compose into Safe Multi-Agent Systems*** — *플래너·워커·검증자·합성자를 엮으면 **에이전트 간 모든 홉이 감시되지 않는 채널**이고 거기로 지시를 밀어넣을 수 있다. 기존 방어는 **입력 경계만** 지킨다.*
   - 🧠 위 3번(생성 모델 ≠ 검증 모델)은 **노드 분리**였다. 이 논문은 **엣지도 검사 대상**이라고 말한다 → ✅ 문서→ESD 파이프라인에서 **단계 간에 넘기는 중간 산출물 자체를 검사 지점**으로 둔다(단계 *입력*만 검사하지 않는다).
   - 🧠 함께 온 (W33-EN17) MasDrift(arXiv:2608.07556)는 다른 각도다 — 📄 *위임된 목표가 **원래의 권한 경계를 반드시 물려받지는 않는다**.* 🧠 LLM 호출을 여러 단으로 쪼갤 때 **"이 단계가 무엇을 해도 되는지"가 함께 넘어가지 않는다**는 뜻이고, `/convert` 같은 단계에서 **단계별 허용 범위를 명시적으로 전달**할 근거다.

6. 🆕 ⭐ 🧠 **(2026-08-12 신규) 모델 티어는 「태스크 난이도」가 아니라 「파이프라인 위치」로 정한다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN18) — arXiv:2608.09155 **Beyond Tier Labels** *다중 호출 LLM 시스템은 **쿼리 단위 라우팅이 담지 못하는** 문제를 낸다 — 모델의 가치는 **의존적 계산의 어느 지점에 투입되는지**와 **그 호출을 둘러싼 배포 환경**에 달려 있다.*
   - 🧠 [[AI-주간-소식-2026-W31]]에 기록한 *단계별 모델 티어링*(가격 격차 600배)에 **근거가 붙었다** — 티어를 *"이 작업이 어려운가"* 로 정하지 말고 **"이 출력에 몇 단계가 의존하는가"** 로 정한다. 🧠 상류 단계에서 싼 모델로 아낀 비용은 하류 전체의 재작업으로 되돌아온다.
   - 🧠 (W33-KR1)(AI 라우터 급부상 — Claude Code 장시간 자율 과제 후 고비용)의 논문 판본이다.

7. 🆕 🚨 ⭐⭐ **(2026-08-13 신규) QA 자동화의 전제부터 검증해야 한다 — 「자동 채점기를 쓴다」는 「품질이 측정된다」가 아니다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN29) — arXiv:2604.16706 **AgentProp-Bench** *도구 사용 LLM 에이전트의 **자동 평가는 신뢰할 수 있다고 널리 가정되지만, 이 가정이 인간 주석과 대조해 검증된 적은 거의 없다*** (14,750개 실행 추적의 진단 벤치마크 · 오류 전파 · 런타임 완화).
   - ✅ **실무 순서**: ① QA 자동 채점기를 붙인다 → ② **사람이 라벨링한 표본으로 그 채점기를 먼저 검증한다** → ③ 그 다음에 채점 결과를 품질 지표로 쓴다. 🧠 ②를 빼면 (W33-KR13) 약국의 교차 검증·규약 ②-b(*평가자를 피평가자와 분리*)를 **형식만 따르고 효과는 미확인**인 상태가 된다.
   - 🚨 📄 **함께 온 반대편 축 — (W33-EN39) The Deliberative Deficit**(arXiv:2608.10186): *배치에 대한 신뢰는 대체로 **검증 가능한 과제 벤치마크(수학·코딩·조정 게임)** 에 기반하는데, 실제 배치는 **가치가 얽힌(value-laden)** 문제다.* 🧠 CogInsight에 그대로 걸린다 — **시나리오 품질을 스키마 통과·링크 정합(검증 가능한 축)으로 재고 있는데, 실제로 중요한 것은 「어떤 분기를 둘 것인가·무엇을 먼저 물을 것인가」(판단이 얽힌 축)** 다. ✅ **스키마 검증 100%가 시나리오 품질을 보증하지 않는다는 것을 릴리스 노트에 명시**한다.
   - 🧠 (EN29)와 (EN39)를 합치면: **틀린 자를 쓰고 있고, 그 자가 재는 것도 재고 싶은 게 아니다.**

8. 🆕 🚨 ⭐ **(2026-08-13 신규) 단계 간 공유 컨텍스트에 「누가 이 근거를 볼 수 있는가」를 함께 실어라 — 요약이 제약을 삼킨다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN26) — arXiv:2608.10509 **MAP-Graph: Provenance-Aware Shared Memory** *공유 메모리는 긴 워크플로에서 정보 재사용을 돕지만, **관련 증거가 특정 에이전트·행동에는 허용되지(admissible) 않을 수 있다.** **제약이 파생(derivation)을 통해 전파되기 때문에, 요약이 비공개·오염된 것을 감출 수 있다.***
   - 🧠 위 5번(ChannelGuard: 홉이 감시되지 않는 채널)·(W33-EN17) MasDrift(위임하면 권한 경계가 안 따라온다)의 **메모리 판본**이다 — *파생하면 증거 제약이 안 따라온다*.
   - ✅ **검사 지점**: `/convert`·요약·정규화 단계가 **상위 제약 표시를 지우지 않는지**. 🧠 요약은 정보를 줄이면서 *"이건 근거로 쓰면 안 됨"* 표시도 같이 지운다 — 그러면 하류 단계가 그것을 정상 근거로 쓴다.
   - 🧠 그리고 이건 이 vault의 `CLAUDE.md` §7(📄 자료 / 🧠 판단)이 하는 일과 같은 구조다 — [[웹-크롤링-기초]] ②-h(*잔여 버킷이 누락을 흡수*)·②-g(*인용이 수록으로 읽힌다*)가 정확히 *"요약이 감춘다"* 의 실제 사례다.

9. 🆕 ⭐ **(2026-08-13 신규) 레퍼런스 검색은 「관련 있는 것」이 아니라 「제약을 만족하는 것」을 찾아야 한다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN37) — arXiv:2604.08849 **SatIR** *많은 실제 검색·매칭 문제는 **주제 관련성 이상**을 요구한다 — 후보는 **여러 프로필 중 특정 하나의 구체적 제약을 충족**해야 하며, 단지 관련 있는 것으로는 안 된다.*
   - ✅ **구조 처방**: **고재현율(high-recall)로 먼저 넓게 뽑고, 제약으로 걸러라.** 🚨 유사도 top-k로 좁힌 뒤 제약을 검사하면 **조건을 만족하는 후보가 top-k 밖에 있을 때 영원히 못 찾는다** — v0.3.0 시나리오 레퍼런스 라이브러리 설계에 직접 걸리는 순서 문제다.
   - 🧠 (EN26)의 *admissible* 과 같은 발상이다: **관련 있어도 쓸 수 없는 증거** / **관련 있어도 조건을 안 맞는 후보**.

10. 🆕 ⭐ **(2026-08-13 신규) 산출물 기준어에 두 축이 더 붙었다 — 「보정된 예측」과 「청중별 서술」**: 위 4번(*편집 가능 + 추적 가능*)의 연장.
   - 📄 [[AI-주간-소식-2026-W33]] (W33-EN31) **CARE-X**(MS Research, 8/12) — *방사선 AI는 **보고서 생성을 넘어** 진화 중. **유연한 추론 · 보정된 예측(calibrated predictions) · 측정 기반 도구**를 결합한다.* ✅ 산출물에 **"이 판단의 확신도"** 를 함께 낸다. ⭐ 그리고 **Tool-Augmented Measurement** = **수치는 모델이 세지 말고 도구가 재게 한다**(🧠 이 vault가 4건 누락을 놓친 원인이 정확히 *"모델이 26건을 세어봤다고 썼다"* 였고 처방이 *"검산 한 줄"* 이었다).
   - 📄 (W33-EN30) **Who Are You Explaining To?**(arXiv:2608.11033) — *SHAP 같은 수치 출력만으로는 **전문성·목표·오해 위험이 다른 청중**에게 좀처럼 충분하지 않다* → **청중 인식(audience-aware) 서술**. ✅ 같은 근거를 **시나리오 설계자용 / 기획자용 / 검수자용**으로 다르게 서술한다. ⚠ 핵심은 길이가 아니라 **틀리게 읽히는 방식이 청중마다 다르다**는 점이다.

11. ⚠ 🆕 **(2026-08-13 관찰) 흐름도 이미지를 모델에 그대로 던져 분기를 추출하는 설계는 위험하다**: 📄 [[AI-주간-소식-2026-W33]] (W33-EN32) **MindTopo**(MS Research, 8/13) — *길, 울타리, 매듭. AI가 **위상(topological) 관계**를 어떻게 이해하는지 시험하는 새 벤치마크 — **공간 추론·계획**을 강화할 기회를 드러낸다.*
   - 🧠 *길·울타리·매듭* = **연결 · 차단 · 교차**다. 즉 **VLM은 그래프의 연결 관계를 생각만큼 못 읽는다**는 것을 재는 벤치마크이고, 흐름도 이미지 → 분기 추출은 정확히 그 능력에 의존한다. ✅ 이미지 입력을 쓸 경우 **추출 결과를 구조적으로 재검증**하는 단계를 필수로 둔다(→ 위 7번의 채점기 검증과 같은 층).
   - 🧠 (W33-EN8) GeoPT(물리 감각)·(W33-EN25) `2608.08077`(부분 관측 하 공간 이해)와 같은 축 — **VLM의 약점이 「인식」이 아니라 「관계·계획」** 이라는 진단이 세 소스에서 모였다.

## 진행사항 업데이트 로그
### 2026-08-05 — v0.7.0 블록 E 구현: 문서→ESD(`/convert`) QA 대응 (📄 QA 11파일 실행·수정, dev 브랜치)
- **요청**: QA 데이터 세트(`~/Downloads/qa-excel-test`, 11파일 — 헤더구조·중복/빈헤더·병합·숫자오판·날짜/수식·불리언/좌표·개인정보/키·다중시트·숨은시트·특수파일명·대용량 12000행)로 문서→ESD 생성을 테스트하고 문제 확인 → 이어서 개선.
- **검증 방식**: 실제 파이프라인 모듈을 그대로 호출하는 헤드리스 하네스(`scratchpad/qa-convert-harness.mjs`, untracked)로 11파일 전건 + 로컬 UI(localhost:5173)로 핵심 케이스 실측(스크린샷·콘솔).
- 🐛 **치명 — 데이터가 조용히 사라짐**: `rows`가 `Record<헤더,값>`이라 헤더가 겹치면 뒤 열이 앞 열을 덮어썼다(`normalizeSheet.js:42`). 중복 `고객명` 2열에서 1열 값 소실, **병합 헤더 시트에서 전화·수량 열이 통째로 소실**(5열 중 3열만 남음), 제목행이 헤더가 된 파일에선 한 값이 4열에 복제. 게다가 `fieldSpecs`가 원본 헤더명 키라 **UI에서 두 행이 한 상태를 공유** → 이름 중복 오류를 영구히 해소할 수 없어 "설정 완료"가 계속 비활성(탈출구는 그 열을 아예 제외하는 것뿐) + React 중복 key 에러 45건.
- **수정**: 파싱 경계에서 헤더 키를 유일하게 만든다(트림 → 빈 헤더 `열N` → 중복 `_2` 접미, 원본은 `headerSources`로 함께 반환해 UI가 "원본: …" 배지로 설명). 개명 충돌(`applyFieldSelection`)도 접미로 유일화 + `collisions` 보고. **헤더 행 자동 감지**(`detectHeaderRow`, 0행이 충분히 채워졌으면 그대로 — 보수적 판정) + 직접 선택 UI로 제목행·병합헤더 문서를 살렸다.
- 🐛 **그 외 수정**: number 판정과 검증 규칙 불일치(지수표기 `1E+15`에서 "타입은 number인데 숫자 형식이 아니다" 자기모순) → 기준 함수 1개로 통합 / 예약 타임스탬프 열이 투영에 남아 미리보기 열 수 ≠ CSV 열 수·`createdAt` 2회 표시 → 투영에서 제외(11파일 전부 일치 확인) / 엑셀 줄바꿈 헤더가 CSV 헤더 줄을 쪼갬 → 공백 접기 + `serializeHeader` / 제로폭 공백이 트림·빈행 제거를 통과 / 숨은 시트가 기본 선택(→ `숨김` 배지 + 보이는 시트 기본) / `연락처`·`연락망`·`비상연락` PII 누락.
- **안전장치 추가**: boolean·geo 값 경고(값 변형 없이 노란 셀 + 사유 요약), number 위험 경고(선행 0 `00123`·15자리 초과 정밀도), 엑셀 오류 셀(`#N/A`) 알림, 스키마명·긴 필드명(150자 헤더) 경고, 워크북 단일 파싱(`openWorkbook` — 12000행×80열 3.2MB 파싱 5.9초 → 2.7초).
- **결과**: 브랜치 `fix/convert-esd-qa-hardening` 커밋 `7bfe07b`(17파일, 신규 `numberRisk.js`). 검증 = `deno test src/lib/*.test.js` **243 passed/0 failed**(+20 회귀 테스트) · `npm run build` green · QA 11파일 재실행 전건 통과 · 로컬 UI 콘솔 클린. **프로덕션 무배포**(v0.7.0 dev 진행 중, 머지·릴리스는 사용자 승인 시).
- 🧠 남긴 항목: 2자리 연도 서식(`26/07/31`)은 정규화 대상 아님(세기 추정 위험), 카드사명 같은 crypt 과탐은 보수적으로 유지(암호화가 안전한 방향), 다중 시트 기본값은 "보이는 첫 시트"까지만(데이터 유무 판정은 미도입).

### 2026-08-04 — v0.6.0 프로덕션 릴리스 (ESD·API 선행 정의·매핑 + 멀티파일 지능형 수집)
> 📄 사용자 "릴리스 규약대로 릴리스" → dev 기능 검증 후 프로덕션 5축.
- **선행 게이트**: ①②③ 기능 브랜치를 `feat/v0.6.0-combined-dev`로 통합(충돌 4파일 수동 해결, deno 358/0·build green) → dev 함수(`ingest-classify-dev`·`api-doc-parse-dev`) 배포 → **브라우저 자동화로 통합 dev 기능 검증 실측**(샘플 4종 업로드: 자동 분류 csv→ESD·OpenAPI json→API·txt→시나리오, 배지 수동 재지정, 하이브리드 API 추출 = OpenAPI 결정론 2 + `api-doc-parse` LLM 폴백 2, 조립·라우팅, 라벨 통일).
- **기능 검증에서 버그 2건 발견·수정**(단위 테스트가 텍스트 직접 주입해 놓친 것): ① `extractFileText`가 `.json/.yaml/.yml` 미지원 → OpenAPI JSON/YAML API 인입 전면 실패 → text 경로 추가. ② `parseExcelFile`/`extractFileText`가 CSV를 cp1252로 오독 → 한글 필드명 mojibake → 바이너리 외 텍스트는 UTF-8 디코딩(`/convert` 등 CSV 전반 개선).
- **프로덕션 5축**(백엔드 먼저 순서로 런타임 안전 확보): ②**DB** `20260731130000_mapping_rules`(멱등 upsert 3규칙) `db push` + migration list Local·Remote 확인 → ③**엣지함수** 프로덕션 슬러그 4종(coginsight-generator·results·ingest-classify·api-doc-parse) 배포 → ①**코드** `release/v0.6.0`(main 분기, combined-dev와 100% 일치) PR #114 → main `1e5d53d` + gitlab 미러 + tag `v0.6.0`(양쪽) + GitHub Release → ④**프론트** Vercel `coginsight-generator.vercel.app` 번들 0.6.0 확인(200) + 사내 온프렘 192.168.20.200:3006 = 200(프로덕션 빌드).
- **⚠ 축5(공개문서) 미완 — 사용자 몫**: `coginsight-overview.vercel.app` 히어로 배지·버전 히스토리 v0.6.0 행 추가 + `vercel --prod` + **claude.ai 아티팩트 `1e30660a…` 재동기화**(필수) + 3탭(개요·매뉴얼·관리자) 검토. overview 프로젝트 소스가 로컬에 없어 미수행. **⚠ 위키만 v0.6.0이고 공개 페이지·아티팩트는 여전히 v0.5.1**(드리프트 상태 — 축5 완료 시 해소).
- **위키 반영(이 세션)**: 버전표에 v0.6.0 행 추가, 스냅샷·진행 현황을 "현재 프로덕션 = v0.6.0 / 현재 개발 = 없음(다음 v0.7.0)"으로 교체, [[CogInsight-Generator-링크]] 갱신.

### 2026-08-28 — v0.8.0 릴리스 + v0.8.1 실봇 검증 + 로드맵 v1.0.0까지 재편 (📄 코드·DB 실측)
- **v0.8.0 프로덕션 릴리스**(PR #118, main `668e3a7`, tag v0.8.0) — 릴리스 규약 5단계 전부. Vercel·사내 3006 번들 해시 동일(`index-BkNMK3KF.js`), 개요 페이지·아티팩트·버전표 동기화.
- **v0.8.1 실봇 검증(중요)** — 가전 A/S 봇을 솔루션에 업로드해 대화로 확인: **런타임이 `intent()`·`entity()`를 정상 평가**한다. v0.7.0 `match()` 미지원 같은 문제 없음. 이로써 v0.8.1의 최대 미검증 항목 해소.
  - 🐛 실봇에서만 드러난 결함 2건: ① 분기 정보가 NLP 파생에 전달되지 않아 **분기 자식 조건이 통째로 빔**(dev 3봇 중 2봇) ② 예문이 전부 기능 단어를 명시해 **증상 발화("세탁기가 안 돌아가요")가 FAQ 인텐트로 오분류**. 둘 다 생성물 구조는 정상이라 단위 테스트·dev 실측으로 안 잡혔다.
- **테스터 가입 메일 장애 수정** — 신규 테스터에게 링크 메일이 가고 클릭 시 404. 원인 3중: ① **Confirm signup 템플릿이 Supabase 기본값**(Magic Link만 코드로 커스터마이즈돼 있었음 — 신규/기존이 다른 템플릿을 쓴다) ② `site_url`이 **폐기된 옛 도메인**(v0.2.2 리네임 때 안 따라옴) ③ `uri_allow_list`도 동일. 세 가지 교체 후 확인. 이 설정은 git에 없어 드리프트가 안 보였다 → `docs/auth-email-templates.md`로 문서화.
- **로드맵 v1.0.0까지 재편** — 위 [[#로드맵 (현재) — 2026-08-28 재편|로드맵]] 참고. ⚠ 재편 계기: v0.6.0·v0.7.0·v0.8.0이 전부 릴리스됐는데 ROADMAP은 셋 다 "(계획)"이었다. **릴리스 규약을 6단계로 늘려 ⑥ROADMAP 갱신 추가**.

### 2026-08-03 — 위키·공개문서 동기화(드리프트 해소): v0.5.1 누락 보완 + 공개 페이지 로드맵·매뉴얼 최신화 (📄 저장소·올림푸스 state 확인 + 라이브 배포·검증)
> 📄 사용자 "sj-wiki랑 공개문서 업데이트 — CogInsight Generator". 저장소·올림푸스 state를 직접 확인해 **두 surface가 라이브와 어긋난 지점**을 찾아 맞춤.
- **발견한 드리프트 3건**: ① **위키만 v0.5.0에 머물러 있었다** — 2026-07-29 v0.5.1 릴리스가 버전표·스냅샷·진행 현황·[[CogInsight-Generator-링크]]에 없음(공개 페이지는 v0.5.1로 갱신돼 있었음 → mirror 규약의 위키 쪽 누락). ② **공개 페이지 "다음 방향"이 폐기된 로드맵**(v0.6.0 = 자연어 수정)을 그대로 안내 — 2026-07-29 재편(v0.6.0 ESD 선행·매핑 / v0.7.0 결과 수정 / v0.8.0 NLP)이 미반영. ③ **공개 페이지 "사용 매뉴얼" 탭이 v0.5.1 UI를 반영 안 함** — 없어진 상단 헤더 메뉴를 안내하고 `/api` 도구 누락(2026-07-20·07-21과 **같은 유형의 재발**: 개요 탭만 갱신되고 매뉴얼이 뒤처짐).
- **위키 반영**: 버전표에 v0.5.1 행 추가, 스냅샷·진행 현황을 "현재 프로덕션 = v0.5.1 / 현재 개발 = v0.6.0 dev"로 교체, 주요 기능에 입력 소스 4갈래(v0.5.0)·앱 셸+문서→API(v0.5.1) 추가, 기술 스택 수치 갱신(엣지함수 34·마이그레이션 65), 다음 버전 계획 콜아웃에 v0.6.0 아키텍처 전환·블록 E 반영, v0.5.1 릴리스/v0.6.0 착수/블록 E 로그 항목 신설, 링크 노트 v0.5.1로 갱신.
- **공개 페이지 반영**(`coginsight-overview.vercel.app`, `vercel deploy --prod` 2회 → 라이브 **200** 확인·본문 grep 검증): "다음 방향"을 v0.6.0(ESD 선행·매핑, `개발 중` 칩)·v0.7.0(결과 수정 3방식 + 문서→ESD 파싱 견고화)·v0.8.0(NLP)로 교체 + 재편 사실 명시. 사용 매뉴얼 도입부를 **좌측 사이드바 실제 라벨**(생성 결과 / 생성: 자연어로 생성·설문으로 생성·문서로 생성·라이브러리 조합 / 부가 도구: 문서 → ESD 생성·문서 → API 생성 / 관리)로 교체, A-2+ 표를 사이드바 기준으로 정정 + **문서 → API 생성 행 신설**, 전역 로딩 안내 추가. **버전표·히어로 배지는 무변경**(프로덕션 여전히 v0.5.1 — 미출시 계획·기존 기능 서술 교정이므로).
- **아티팩트 재동기화**(규약 필수 단계): 라이브 HTML에서 `<title>`~마지막 `</script>` 추출 → `1e30660a…` 동일 URL 재발행. ⚠ 발행 전 아티팩트 원본을 fetch해 라이브와 **diff = 내 편집분뿐**임을 확인(다른 세션 변경 클로버 방지).
- 📸 **매뉴얼 스크린샷 18장 전면 재촬영**(사용자 요청, 2026-08-03): 기존 14장이 전부 **v0.5.1 이전 UI(헤더 nav 시절)**여서 폐기하고 프로덕션 v0.5.1에서 재촬영 + v0.5.x 신규 화면 4장 신설. 방식은 2026-07-03의 **"Chrome 프로필 사본 + CDP"** 패턴 재사용(사용자 확인) — 사용자 Chrome의 `Local Storage`·`Cookies`를 임시 프로필로 복사해 **헤드리스 Chrome(포트 9223)**을 띄우고, **무의존 CDP 드라이버**(Node 25 native WebSocket, `shots/cdp.mjs`)로 자동 캡처. 로그인 화면(A-1·B-1)은 세션 없는 **깨끗한 프로필(9224)**로 별도 촬영. 캡처 후 **프로필 사본 즉시 삭제**(쿠키 잔존 방지) + 헤드리스 종료 확인.
  - **교체 14장**: A-1 로그인 / A-2 설문 진행 / A-3 시나리오 카드 / A-4 라이브러리 / A-5a 결과 목록 / A-5b 결과 상세 / B-1 관리자 로그인 / B-3 질문 / B-4 솔루션 규칙(규칙 학습 패널) / B-5 참고자료 / B-6 API 레퍼런스 / B-7 시나리오 레퍼런스 / B-8 테스터 / B-9 피드백. **신규 4장**: A-2b 자연어로 생성(`/`) · A-2c 문서로 생성(`/doc`) · A-2d 문서→ESD 생성(`/convert`) · A-2e 문서→API 생성(`/api`).
  - 🔒 **PII 마스킹**(사용자 선택): 캡처 직전 DOM 텍스트·input 값의 이메일을 정규식으로 `t****@도메인`으로 치환 — 결과 목록 6건·테스터 관리 4건 실제 치환 확인. 무계정 공개 페이지라 사내 이메일 노출을 차단.
  - 🧠 **자동화 함정 2건**: ① 설문은 단계마다 필수값이 있어 그냥 `다음`을 눌러선 진행 안 됨 → 라벨 기준으로 값을 채워 5단계 전진 후 시나리오 카드를 조립(수집 정보·외부 연동 API·AI 자유응답=예)해야 A-3이 나온다. 처음엔 채움값이 아무 칸에나 들어가 **"API 이름에 한글 불가" 빨간 경고가 찍혀** 재촬영했다. ② `Page.captureScreenshot`의 `captureBeyondViewport:true`는 **뷰포트 높이를 무시하고 전체 페이지를 담는다** → 결과 목록이 10,096px·923KB로 잡혀 페이지가 3.1MB로 비대해짐. `clip`으로 상단 900px만 잘라 157KB로 해결(최종 페이지 **2.39MB**).
  - 🔁 **브라우저 실렌더 확인에서 3차 보정**(사용자 "배포해서 확인할래"): ① 로그인·설문 등 **콘텐츠가 짧은 화면이 여백 덩어리**로 찍혀 있었다 → 리프 요소 기준 콘텐츠 하단 실측으로 잘라냄. 이때 자체 가드(`> 500`)가 작은 값을 버려 적용이 안 되던 버그도 발견·수정. ② 너무 타이트하게 자르면 **뷰포트가 낮아져 사이드바 메뉴가 접히고**(앱 셸이 잘린 것처럼 보임) → **최소 높이 900px** 보장으로 절충. ③ 숨긴 피드백 버튼이 `visibility:hidden`이라 **박스는 남아 하단을 늘리던** 것도 제외 처리.
  - 🔒 **2차 마스킹(실렌더 검토에서 발견)**: 이메일만으론 부족했다 — **참고자료 관리에 고객사명(생명보험사)·실명**이, **피드백 관리에 작성자 실명 9건**이 그대로 보였다. 무계정 공개 문서라 리터럴 치환(`박상준`→`박○○`, 고객사명→`○○사`)을 캡처 스크립트에 추가하고 B-5·B-9 재촬영, 캡션에 마스킹 사실 명시. ⚠ **남은 판단거리**: API 레퍼런스(B-6)의 `openEMR_*` 엔드포인트 이름·`실시간 주차장 정보 확인`은 제품/공공API 이름이라 그대로 뒀다 — 가릴지는 사용자 판단.
  - 배포·검증: `vercel deploy --prod` → 라이브 200 + 이미지 18개·신규 캡션·캡처 기준일 grep 확인, 아티팩트 `1e30660a` 재동기화. 매뉴얼 두 탭 도입부에 **"캡처는 2026-08-03 · v0.5.1 기준, 이메일 마스킹"** 안내 추가.
- 🗑 **폐기 Vercel 프로젝트 삭제**(사용자 요청 — 이력만 남김): `overview-deploy`(31일 전 같은 실수의 잔재)가 **구 이름 "Cogi POC Generator" 개요 문서를 무계정 200으로 계속 공개**하고 있었음 → v0.2.2 리네임 때의 **구 URL 폐기 원칙 위반** 상태라 삭제(배포 1건 포함). 같은 세션에서 잘못 만든 `deploy`도 삭제. 남은 프로젝트는 실사용 7개(coginsight-overview·coginsight-generator·smarthub·mailer·notepad·schedule-reporter-kakao·bible-quest)만.
- ⚠ **작업 중 실수·정리**: 스크래치패드 배포 디렉토리가 `.vercel` 링크 없이 있어 첫 `vercel deploy --prod`가 **새 프로젝트 `deploy`를 만들어버림**(공개 URL과 무관). `vercel link --project coginsight-overview`로 재링크해 정상 배포하고, 잘못 생긴 `deploy` 프로젝트는 삭제 완료. 🧠 재발 방지: 새 세션에서 이 페이지를 재배포할 땐 **디렉토리를 먼저 `vercel link --project coginsight-overview`** 할 것(스크래치패드는 세션 임시라 `.vercel`이 남지 않는다). 🧠 참고: 이전 세션이 남긴 미사용 프로젝트 `overview-deploy`도 대시보드에 남아 있음(공개 URL과 무관, 정리 여부는 사용자 판단).

### 2026-07-31 — v0.6.0 착수: ESD 아키텍처 전환(테이블 폐기 → 결과 번들) + 블록 A 완료 + 매핑 T1~T4 (📄 git log·올림푸스 state 직접 확인, dev 전용·프로덕션 무배포)
> 📄 v0.6.0 사이클 착수(`package.json` 0.5.1 → **0.6.0**, 커밋 `2b3f92f` — 배지 `v0.6.0 DEV`). 브랜치 `feat/v0.6.0-esd-mapping`(+ `feat/v0.6.0-esd-store`), **main 미머지**. [[올림푸스-Olympus]] 스펙 3종(`v0.6.0-1-esd-store`·`-2-multifile-ingest`·`-3-esd-mapping`)으로 진행.
- **⚠ 아키텍처 전환(커밋 `66b0819`·`a32bff1`)**: 2026-07-29 원설계의 "새 `esd` 테이블 저장소"를 **과설계로 폐기** → ESD를 **생성 결과에 번들**(`coginsight_results.generation_tiers.esd`, 기존 jsonb 재사용·**신규 컬럼 없음**·키 없으면 하위호환). "선행"의 의미도 *저장 라이브러리* → **생성 마법사의 세션 단계**로 바뀜. 폐기물: `esd`/`dev_esd` 테이블·마이그레이션, `esd`/`esd-dev` CRUD 함수, `EsdManager`, `/esd` 라우트·`useEsd`. 살린 것: `EsdEditor`·`buildEsdJson`·`esdValidation`·`apiDefEditor`.
  - 편집 경로: `results`(+`-dev`) 함수에 **PATCH** 추가 — 본인 결과의 `generation_tiers.esd`만 jsonb read-modify-write 병합/제거(DDL 없음 = 공유 DB 새 컬럼 회피 규약 준수), 결과 상세에 "ESD (편집 가능)" 섹션 + `EsdEditor` 모달.
  - **핵심 불변식**: ESD 미연결이면 기존 생성 경로 **완전 무변경**(회귀 없음). 매핑 "지침 문구"는 `solution_rules`, 강제 "로직"만 코드.
- **블록 A(ESD 선행 저작·검증) 완료** — 올림푸스 spec 1 백로그 T1~T4 소진(`all_done`, critic GREEN, deno 288/0). 생성 진입에 선택적 "ESD 먼저 정의" 앞단(`EsdFrontStage`) + 직접입력/문서업로드 초안 + `esdValidation` 검증 → 세션 ESD.
  - ⚠ **미결 질문 3건(비블로커, 사람 확인 대기)**: Q1 앞단을 자연어 진입에만 붙였는데 설문·문서 진입에도 노출할지 / Q2 검증 범위를 이름·중복·예약열 5종에서 타입·암호화 형식까지 넓힐지 / Q3 문서업로드 UX를 `EsdEditor` 내장 업로드로 갈지 `esdFromDocuments`를 UI 경로로 쓸지.
- **블록 B+C(ESD 기반 매핑) T1~T4 완료, T5 대기** — spec 3 진행:
  - **T1** `proposeMapping` 순수함수(`src/lib/mapping/`) — ESD 필드 ↔ 시나리오 수집변수를 이름 정규화 완전일치+타입일치면 score 1.0·1:1 고유 시 `auto:true`, 부분일치(Dice ≥ 0.3)·타입불일치·다대다는 후보 목록, 미매핑 필드/변수 분리 반환. deno 21케이스 + src/lib 전체 309/309.
  - **T2** 매핑 지침 `solution_rules` 행 + 마이그레이션(`20260731130000_mapping_rules.sql`) — 지침은 하드코딩 아닌 DB(규약 준수).
  - **T3** 생성기 **인-프롬프트 ESD 주입** — `esdBundle`이 있을 때만 4개 빌더(flow/config/output/condition)에 ESD 필드 계약 섹션 주입(`flow/esdContract.ts`), 없으면 **프롬프트 바이트 동일**(회귀 어서션 AC1). 관측성 `generation_tiers.esd_mapping`에 매핑 결과 기록. `proposeMapping`을 Deno TS로 동일 이식.
  - **T3b(F1 수정)** `extractCollectVarsFromJson`이 수집변수 타입을 `"string"` 하드코딩하던 것을 이름 일치 ESD 필드 타입으로 override — `number` 필드가 `auto:true`로 매칭되게. esd 미연결·미매칭은 종전 유지.
  - **T4** `createResult` 배선(세션 ESD → 생성기 `esd` 인자, `generatorBody.js`). critic GREEN 314/314.
  - **T5(다음)** 진입 확장 — 설문(`QuestionnaireForm`)·POC 문서 진입에도 "ESD 먼저 정의" 토글(**기본 off** = 회귀 유지) 추가.
- **블록 D(입력 강화, spec 2 `multifile-ingest`)는 미착수** — `/nl` 파일첨부·POC 멀티파일 자동분류(`ingest-classify`)·한 업로드로 ESD+시나리오 동시 산출.
- 🧠 규모(브랜치 기준): 888커밋, 엣지함수 34(prod 23 + dev), 마이그레이션 65.

### 2026-07-31 — v0.7.0에 블록 E 추가: 문서→ESD 파싱 견고화 (📄 저장소 커밋 `95f01b3`, 브랜치 `docs/v0.7.0-esd-parsing-hardening` — main 미머지)
> 📄 v0.6.0 코드리뷰 + 같은 날 `/convert` QA 11종 검증(아래 항목)에서 드러난 **문서(엑셀)→ESD 자동생성의 결함**을 v0.7.0 스코프에 "블록 E"로 등록. 각 항목 근거를 `파일:라인`으로 고정.
- **왜 v0.7.0인가**: v0.6.0 스코프(A/D/B+C)가 이미 크고, 이 항목들은 "결과가 틀렸을 때 사용자가 알아채고 고칠 수 있게 한다"는 v0.7.0(결과 수정) 주제와 성격이 같음.
- ⚠ **공통 성격**: 파싱 에러가 아니라 **조용히 틀린 ESD가 만들어지는** 문제 → 파싱 실패보다 위험(검토 없이 저장 시 잘못된 데이터 계약이 생성 전체로 전파). 개선의 절반은 판정 로직, 절반은 **"이렇게 판정했다"를 드러내는 UX**.
- **E1** 첫 시트 하드코딩(`EsdEditor.jsx:200-202`·`EsdFrontStage.jsx:77-78`) → `/convert`에 이미 있는 `SheetSelect` 재사용, 다중 시트 선택 시 시트당 엔티티 1개(순수모듈 `esdFromDocuments`가 이미 `sheets[]` N개 지원). **E2** 헤더 행 1행 고정 → 헤더 행 지정 UI + 휴리스틱 후보 + 병합 헤더 경고. **E3** 중복·빈 헤더가 `normalizeSheet.js` 레코드 조립(`{헤더명: 값}`)에서 뒤 열이 앞 열을 덮음 → 임포트 즉시 감지·자동 교정 제안(현재는 저장 시점 `esdValidation`에서야 차단). **E4** 예약 타임스탬프 열 무안내 제외 → 제외된 열 이름 명시.

### 2026-07-31 — `/convert`(엑셀→ESD) QA 함정 파일 11종 검증 (📄 로컬 dev v0.6.0 DEV, 코드 무수정)
> 📄 QA용 함정 엑셀 11개(헤더구조·중복빈헤더·병합빈칸·숫자오판·날짜수식·불리언좌표·개인정보키·다중시트·숨은시트·긴파일명·대용량 12,000행×80열)를 로컬 `localhost:5173/convert`에 실업로드해 단계별 거동 확인. v0.6.0이 `/convert`를 재사용하므로 착수 전 기준선.
- 🐛 **차단급 — 이름이 같은(또는 둘 다 빈) 컬럼**: `normalizeSheet.js`가 행을 `record[headers[i]]`로 만들어 **마지막 열이 앞 열을 덮어씀(데이터 유실)** + 필드명 입력 상태까지 같은 키를 공유해 **개별 이름 지정 불가 → "이름이 중복됩니다"에서 탈출 못 하는 데드락**. 실사용 엑셀(중복 헤더·빈 헤더)에서 변환 자체가 불가.
- 🐛 **헤더 행 고정(첫 행)** — 1행 제목/2행 부제/병합 헤더 파일은 제목·병합값이 헤더가 되고 실제 헤더는 데이터로 밀림. 헤더 행 선택 UI 없음.
- 🐛 **타입 추론**: 선행 0(`00123`)·16~17자리 정수를 `number`로 판정(안내문 "숫자처럼 보이는 문자열은 string"과 모순, 우편번호만 컬럼명 규칙으로 string) → ESD 등록 후 값 훼손 위험, 게다가 키로도 자동 지정. `boolean`/`geo`는 값 검증이 없어 `1`·`Y`·`O` 원문이 오류 0건으로 통과(number만 검증). 수식·`#N/A` 셀은 경고 없이 빈칸. 날짜 정규화가 `26/07/31`(2자리 연도) 미지원.
- 🐛 **미리보기 ≠ 실제 CSV**: 미리보기는 원본 `createdAt` 열을 남긴 뒤 자동 열을 덧붙여 `createdAt`이 2번·82열, 실제 `excelToUploadCsv`는 예약열을 필터해 81열.
- ⚠ 🔒/🔑 자동 지정이 **컬럼명 키워드 기반** — `연락처`·`여비상연락망`(실제 010 번호) 놓치고 `카드사명`·`주소지코드` 과탐지, 키는 `USER_ID`(대문자·언더스코어) 놓치고 우연히 고유한 `번호2` 선택(`userId`는 정상 인식). 숨은 시트가 목록에 노출·기본 선택되고 숨김 표시 없음.
- ✅ 정상: 예약 타임스탬프 열 자동 처리, 빈 행·빈 열 제거·셀 트림·제로폭 공백, `island`/`issue`의 boolean 오판 회피, 시트 보호·틀 고정·필터 무해, number 컬럼 비-숫자 값(`1E+15`) 검증 하이라이트, 대용량 12,000행×80열 로딩 표시 후 ~8초 내 파싱·미리보기 100행 캡·추론 정상.
- 🧠 미검증: 대용량 파일의 3000자 초과 긴 문자열·이모지/다국어 함정(생성 스크립트가 해당 값을 실제 행에 안 넣어 파일에 없음).

### 2026-07-29 — v0.5.1 프로덕션 릴리스: UI/UX 앱 셸 개편 + 문서→API 생성 도구 (📄 git·CHANGELOG·공개 페이지 라이브 확인)
> 📄 PR **#113** → main `345fa96`, **tag `v0.5.1` + GitHub Release**. 헤더 nav 중심이던 화면을 **그룹형 사이드바 앱 셸**로 재구성하고, 생성 진입을 라우팅으로 정리. 신규 엣지함수 `api-doc-parse`(prod 슬러그 동반) 외 **DB·마이그레이션·`solution_rules` 무변경**. 릴리스 검증: `npm run build` green.
- **앱 셸**: `AppShell`/`Sidebar`/`SidebarNav` — 생성·부가 도구 그룹, 로고+제목 헤더, 데스크톱 접기/펼치기(`localStorage.sidebarCollapsed`), 접힘(레일) 시 아이콘 hover 툴팁, 모바일 오프캔버스 유지. 버전 배지 좌하단 → **우상단**.
- **라우팅 개편**: `/`=자연어 생성(기본), `/survey`=설문, `/nl`→`/` 리다이렉트, `/doc`=문서 생성(사이드바 승격), `/api`=문서→API 생성(신규).
- **문서→API 생성 도구**(`/api`, `ApiGenPage`): 문서 붙여넣기 + 파일(`.json/.yaml/.txt/.md/.csv/.xlsx/.pdf`) → "API 추출" → api_def별 편집 카드로 검토·수정 → JSON 저장/복사. 한 문서의 **다중 API**를 한 번에. 하이브리드 — `parseApiDocToDefs`(OpenAPI 결정론) 우선, 실패 시 신규 LLM 함수 `api-doc-parse` 폴백.
- **전역 로딩 오버레이**: `LoadingProvider`/`useLoading` — `useApi.request`가 `loadingMessage`를 받아 요청 전 표시·완료 시 해제, `createResult` 등 생성 경로 연결.
- 🐛 **Fixed — 투명 버튼**: `bg-primary-500` 등이 색을 못 받아 "API 추출" 버튼이 안 보이던 문제. 근본 원인은 **Tailwind v4가 `tailwind.config.js` 색상을 읽지 않음** → 브랜드 블루 스케일을 `theme.css`의 `@theme` 블록에 정의(버튼·사이드바 활성·포커스 링·스피너 전부 정상화). 그 외 문서 미입력 시 버튼 비활성화, 전역 버튼 커서(`pointer`/`not-allowed`).
- **공개 개요 페이지**: 릴리스 규약 ⑤단계대로 v0.5.1 반영 완료(히어로 배지·통계·`v0.5.1` 섹션·버전표 행). ⚠ 위키 버전표에는 이번(2026-08-03) 갱신에서야 추가 — **9일간 위키만 v0.5.0에 머물러 있었음**(공개 페이지 ↔ 위키 mirror 규약의 위키 쪽 누락).

### 2026-07-29 — 사내 GitLab 소스 미러링 구성 (📄 세션 작업, 인프라 상세는 레포 DEPLOYMENT.md)
> 📄 사용자가 할당받은 **사내 GitLab 회사 프로젝트**에 CogInsight-Generator 소스를 추가로 올림(기존 GitHub 개인 origin은 Vercel 배포용으로 유지, GitLab은 별도 remote).
- **미러 결과**: 전 브랜치 31 + 태그 11(`v0.1.0`~`v0.5.1`) push. `main` = 로컬·GitHub·GitLab 삼자 일치 검증. GitLab이 자동 생성했던 빈 껍데기 `master`(별개 뿌리 Initial commit)는 기본 브랜치를 `main`으로 바꾼 뒤 삭제.
- **인증**: SSH 포트(22/2222/443)가 서버 방화벽으로 전부 차단 → **HTTPS + Personal Access Token**(macOS 키체인 저장)으로 push. ⚠ 사내 GitLab 호스트·프로젝트 경로·회사 계정·토큰 등 인프라 상세는 **기밀 분리 원칙상 레포 `DEPLOYMENT.md`에만** 두고 이 동기화 vault엔 미기재.
- **파이프라인 실패 메일**: 저장소에 `.gitlab-ci.yml` 없고 프로젝트 Auto DevOps도 off → 상위(그룹/인스턴스) 강제주입 CI가 브랜치 rules로 일부 브랜치에만 실행되어 실패하는 것으로 추정(미러용이라 무시 가능, 메일은 GitLab Notifications에서 차단). 토큰 스코프 부족으로 API 확정은 못 함.
- **위키 반영**: 위 [[#현재 상태 스냅샷 — v0.1.0 프로토타입 배포 (2026-06-30)|무엇이 어디에]]에 "소스 저장소" 항목 추가, 이 로그 항목 추가. (버전·프로덕션 무변경 — 인프라 구성 작업.)

### 2026-07-29 — 로드맵 v0.8.0 추가: NLP 생성 & NLP 기준 조건 설정 (📄 사용자 확정, 저장소 ROADMAP·CLAUDE 반영)
> 📄 사용자 "로드맵에 다음 버전으로 하나 추가 — NLP 생성 기능". 인텐트·엔티티를 어터런스와 함께 **CSV로 제공**해 솔루션 시스템에 업로드하고, 생성 시 조건을 **발화 기준이 아니라 이 NLP 기준으로 설정**하고 싶다는 요구. 확정 다음 버전 `v0.8.0`으로 등록.
- **v0.8.0 (계획) = NLP 생성 & NLP 기준 조건 설정** — ① 시나리오에서 인텐트·엔티티 추출·정의 + 인텐트별 어터런스(예문) 생성 → 솔루션 업로드용 CSV. ② 플로우 진입/분기 조건을 발화 매칭이 아니라 생성된 인텐트/엔티티에 바인딩(조건 술어가 NLP 참조). ③ NLP 엔티티 ↔ ESD 필드(v0.6.0 매핑)·조건 규칙(`solution_rules` Condition Rule) 정합. 미확정: NLP CSV 실규격·어터런스 생성 기준, 런타임 조건 계약(현 `match()` 미지원 등) 정합, 엣지함수·DB·dev 4축.
- **저장소 반영**: `ROADMAP.md` v0.8.0 섹션 신설(배경·작업 항목·설계 미확정), 백로그 운영 방침을 "확정 버전 v0.6.0/v0.7.0/v0.8.0 셋"으로 갱신. `CLAUDE.md` 상단 포인터에 v0.8.0 추가. (릴리스 전 계획이라 버전표·매뉴얼·공개 개요 무변경 — 프로덕션 여전히 v0.5.1.)
- **위키 반영**: 위 [[#진행 현황|진행 현황]] "다음 버전 계획" 콜아웃에 v0.8.0 줄 추가 + 운영 방침 셋으로 갱신, 이 로그 항목 추가.

### 2026-07-29 — 로드맵 재편: v0.6.0 = ESD 선행 생성·매핑, v0.7.0 = 생성 결과 수정 (📄 사용자 확정, 저장소 ROADMAP·CLAUDE 반영)
> 📄 사용자 "로드맵에 추가하고 싶은데 최종 다음 버전으로 해줘". 두 항목(①ESD 선행 생성 & 매핑 ②결과 수정 3방식)을 **볼륨·범위 고려해 두 개 버전으로** 등록. 기존 v0.6.0(자연어 수정)은 v0.7.0에 흡수·확장.
- **v0.6.0 (계획) = ESD 선행 생성 & 매핑 기반 설정** — 생성 앞단에 ESD(데이터/서비스 정의)를 1급 단계로. ①직접 입력(폼/에디터) ②문서 업로드 자동생성(엑셀·API 문서 → 파서/LLM, v0.5.0 `/convert`·`api_def` 재사용·통합). 확정 ESD 기준으로 수집 변수·값·output·연동을 필드에 매핑(자동 + 수동 조정). 미확정: ESD 저장 위치(새 테이블 vs 스키마 JSON/`api_def` 확장), 매핑 UX, 엣지함수·DB·dev 4축 범위.
- **v0.7.0 (계획) = 생성 결과 수정 (3방식)** — flow/`generated_json`을 ①자연어 지시 ②설문 기반(원설문 항목 편집→부분 재반영) ③다이얼로그 기반(챗 UI로 노드·멘트·분기 대화형 교정)으로 수정. 백로그 다이어그램 편집과 상보적. 미확정: 전체 재생성 vs 부분 패치, `checkBot` 재검증, 수정 이력(diff)·되돌리기.
- **저장소 반영**: `ROADMAP.md` v0.6.0 섹션 교체(배경·작업 항목·설계 미확정) + v0.7.0 섹션 신설, 백로그 "다이어그램 편집"·"장기 방향"의 버전 참조를 v0.7.0/v0.6.0로 정합화. `CLAUDE.md` 상단 포인터 갱신(다음 버전 v0.6.0 ESD 선행 → v0.7.0 결과 수정).
- **위키 반영**: 위 [[#진행 현황|진행 현황]]의 "다음 버전 계획" 콜아웃을 v0.6.0/v0.7.0로 교체, 이 로그 항목 추가. (릴리스 전 계획이라 버전표·매뉴얼·공개 개요는 무변경 — 프로덕션 여전히 v0.5.0.)

### 2026-07-23 — v0.5.0 항목① 확장: 엑셀 변환에 **ESD 스키마 JSON 동시 산출** (📄 dev 브랜치, 미릴리스)
> 📄 v0.5.0 「입력 소스 다양화」 항목①(엑셀 → 업로드용 CSV)에 **스키마 JSON 산출**을 추가. 데이터(CSV)만 만들던 것을 "그릇(스키마) + 데이터" 한 흐름으로 확장 — ESD 매니저에서 스키마를 손으로 만들 필요가 없어짐. 브랜치 `feat/v0.5.0-excel-esd-json`, **프론트엔드 전용**(DB·엣지함수 무변경), **아직 main 미머지·미릴리스**.
- **산출물 계약**: 생성 파이프라인(`deriveEsdSchemas.ts`의 `EsdSchema`)과 **키 집합·순서·값 형식 동일** — `crypt`는 문자열 `"true"/"false"`, `resultSamples`는 빈 배열, `createdAt`/`updatedAt` 계열 열은 필드에서 제외. 다운로드는 `{스키마명}_schema.json`(결과 상세의 ESD 카드와 같은 규약).
- **판정 방식**: 🧠 LLM 대신 **로컬 결정론 휴리스틱 + 사용자 편집**(사용자 확정). 생성기 LLM 프롬프트(`buildSchemaPrompt`)의 추론 규칙을 코드로 이식 — 네트워크·비용·지연 0, 프론트 전용 유지. 우선순위 geo → boolean → string강제(전화·우편번호) → number → string. `key`는 식별자 이름 + **비개인정보** + 값 전부 고유인 첫 열 하나만.
- **신규 순수 모듈 3종**(기존 CSV 트리오와 대칭, 기존 모듈 무수정): `esdFieldRules.js`·`inferEsdFields.js`·`buildEsdSchema.js`. 영문은 **토큰 완전일치** 매칭으로 `hotel`→`tel`, `island`→`is`, `productName`→개인정보 오탐 차단.
- **UI**: ③단계가 "컬럼 타입 설정"→**"ESD 필드 설정"**(타입 4종 select + 🔑 키 단일 지정 + 🔒 암호화), ④단계에 스키마명 입력·JSON 미리보기·복사·다운로드. CSV 경로는 `csvTypeOf` 매핑으로 파생해 기존 동작 그대로.
- **검증**: `deno test --no-check src/lib/` **110 passed / 0 failed**(기존 70 + 신규 40, 생성기 계약 회귀 테스트 포함), `npm run build` green, 샘플 데이터 end-to-end 실행으로 CSV·JSON 산출 확인. ⚠ 브라우저 UI 클릭 검증은 확장 미연결로 미실시.
- 설계·계획 문서: 저장소 `docs/superpowers/specs/2026-07-23-excel-esd-schema-json-design.md`, `docs/superpowers/plans/2026-07-23-excel-esd-schema-json.md`.
- **(이어서) 샘플 데이터·필드명 추천·복합키** — ③단계 표에 **컬럼별 실제 값 3개**를 칩으로 표시(신규 `columnSamples`), 필드명은 업로드 즉시 **영문 추천값이 자동으로 채워지고** 수정 가능(추천 실패 행은 "직접 입력하세요" 힌트, 고치면 사라짐). 📄 **정정: ESD는 키를 여러 개 지정할 수 있다**(사용자 확인) → `buildEsdSchema`의 단일 키 클램핑 제거 + UI 🔑를 독립 토글로. 자동 판정은 보수적으로 하나만 유지 — 🧠 복합키는 개별 열이 아니라 **조합해야** 고유해서 "값 전부 고유" 기준으로 구성원을 못 고름(실제로 `주문번호`+`상품코드` 예시에서 자동 KEY 0개 → 사용자가 2개 지정). `deno test` **136 passed / 0 failed**.
- **(같은 날 이어서) 컬럼 제외·개명 UI 추가** — ③단계 표에 **사용** 체크박스 + **ESD 필드명** 입력. 제외·개명이 CSV·스키마 JSON **양쪽에 동일 반영**(신규 `applyFieldSelection` 투영을 둘이 공유 → 구조적으로 어긋날 수 없음). `전체 영문 이름으로 변환` 버튼(신규 `toEnglishFieldName`: 사전 최장 일치 분절, `전화번호`→`phone`·`주문번호`→`order_no`·`가입여부`→`is_signup`). ⚠ **반쪽 변환 금지** 설계 — 사전에 없는 조각이 있으면 원본 유지 + 실패 개수 안내(일부만 영문 되어 "다 됐다" 착각 방지, 🧠 사용자에게 미리 고지한 리스크의 대응). 검증: 빈 이름·중복·예약어(`createdAt`/`updatedAt`)·사용 0개면 진행 차단. `deno test` **128 passed / 0 failed**, build green. 문서 `docs/superpowers/specs|plans/2026-07-23-convert-column-rename-exclude*.md`.

### 2026-07-21 — v0.4.2 결과 확인 창 UI 개선 프로덕션 릴리스 + 공개문서·위키 동기화 (📄 4축 실행·라이브 검증)
> 📄 사용자 승인 후 v0.4.2 프로덕션 릴리스. 결과 상세(`/results/:id`)의 시나리오 식별·가독성·탐색성 개선(프론트 전용).
- **① 코드**: PR **#108** → main `2986e1f` 머지, **tag `v0.4.2` + GitHub Release**, CHANGELOG `[0.4.2]`. `npm run build` green.
- **기능**: 입력한 응답 시나리오 카드화(번호·이름 헤더 + `#0052CC` 액센트, `ScenarioAnswer`)·접기(개별/전체, **기본 접힘**) / 상세 상단 **요약 헤더**(봇 이름 + 메타 칩, 계산 `utils/resultMeta.js`로 공용화 → 목록 카드와 동일) / **섹션 sticky 네비**(`top-16`·`scroll-mt-32`) / 버튼 색 `#0052CC` 통일.
- **② DB·③ 엣지함수**: 변경 0 → 해당 없음. **④ 프론트**: Vercel 프로덕션 배포 success(sha `2986e1f`).
- **dev 리셋**: 이번 사이클 dev 드리프트 0이라 **사용자 승인 하에 스킵**.
- **공개 개요 페이지**(https://coginsight-overview.vercel.app): 전 항목을 **v0.4.2 기준**으로 갱신(히어로 배지·통계 802커밋·인트로·진행현황 h3 + v0.4.2 소개 블록·버전표 행·매뉴얼 A-5). `vercel deploy --prod` 재배포 → 라이브 curl 검증(배지·히스토리·매뉴얼·favicon 200).
- **아티팩트(`1e30660a`) 재동기화 완료** ✅ — 이전에 막혔던 **이중 래핑 문제 해결**: 라이브 HTML에서 `<title>`~마지막 `</script>`만 추출해 Artifact 재발행(`url=` 동일). 드리프트 해소.
- **위키 동기화**: [[CogInsight-Generator-링크]]·[[프로젝트-포트폴리오]]·[[index]] 현행 버전 v0.4.2로 갱신(포트폴리오·index는 v0.3.0에 멈춰 있던 것 현행화).

### 2026-07-21 — 다음 버전 계획 확정: v0.5.0 입력 소스 다양화 · v0.6.0 결과 자연어 수정 (📄 사용자 확정, 저장소 ROADMAP·CLAUDE 반영)
> 📄 사용자 "로드맵 뿐 아니라 sj-wiki 문서도 다 맞춰서 수정해줘". 다음 두 버전 스코프를 확정.
- **v0.5.0 (계획) = 입력 소스 다양화** — ① 엑셀 → 업로드용 CSV 변환 ② API 인터페이스 문서 → 업로드용 JSON ③ POC 문서(시나리오 정의서·흐름도) → 챗봇 생성 ④ 자연어 시나리오 생성(설문 폼 대체). 공통 테마 = "가진 자료를 올리면 업로드 산출물이 나온다".
- **v0.6.0 (계획) = 생성 결과 자연어 수정** — 생성된 flow/`generated_json`을 자연어 지시로 수정. v0.4.0 다이어그램 편집(백로그)과 상보적.
- **저장소 반영**: `ROADMAP.md`에 v0.5.0·v0.6.0 섹션 신설(배경·작업 항목·설계 미확정) + v0.4.0 "릴리스 준비"→"릴리스됨" 정정·v0.4.1/v0.4.2 릴리스 브리프 추가·기존 v0.5 잔여(다이어그램 편집 등)를 백로그로 이동. 2026-07-20 "상황 적응형 생성" 3항목은 **장기 방향(버전 미정)** 백로그로 보존(main ROADMAP에 실재하지 않던 참조 정합화). `CLAUDE.md` 상단 포인터도 v0.5.0/v0.6.0로 갱신.
- **위키 반영**: 위 [[#진행 현황|진행 현황]]의 "다음 버전 계획" 콜아웃 갱신, [[프로젝트-포트폴리오]] CogInsight 행에 다음 방향 추가, [[#진행사항 업데이트 로그|이 로그]] 항목 추가.
- **공개 개요 페이지 반영** (https://coginsight-overview.vercel.app): 개요 "다음 방향" 절의 기존 3카드(상황 적응형 3방향)를 **v0.5.0 입력 소스 다양화(4카드) + v0.6.0 결과 자연어 수정**으로 교체, 상황 적응형 생성은 하단 "장기 방향" 1줄 note로 강등. 미출시 계획이라 매뉴얼·관리자 탭·버전표는 무변경(프로덕션 여전히 v0.4.2). 라이브 SoT HTML의 authored 콘텐츠(`<title>`~마지막 `</script>`)만 추출해 편집 → `vercel deploy --prod`(프로젝트 `coginsight-overview`, ⚠ 동명 프로젝트 `overview-deploy`와 혼동 주의 — 명시적 링크 후 배포) → 라이브 200·마커 검증. **아티팩트(`1e30660a`) in-place 재동기화 완료**(url 동일, 추출-재발행 방식 — 드리프트 방지).

### 2026-07-21 — 공개 개요 페이지 v0.4.1 전체 복구 + 다음 방향 반영 (📄 라이브 배포·로컬 렌더 검증) ⚠ 기록 정정
> 📄 **기록 정정**: 아래 2026-07-20 "매뉴얼 탭 v0.4.x 최신화 + 아티팩트 드리프트 해소" 및 위 v0.4.1 마일스톤의 "공개 개요 페이지 v0.4.1 반영" 기록은 **실제 라이브·아티팩트에 반영되지 않았음**을 2026-07-21 확인. 편집 원본 아티팩트(`1e30660a`)·라이브(`coginsight-overview.vercel.app`) 둘 다 **v0.3.0에 머물러 있었다**(v0.4.0 "예정"·v0.4.1 없음, 매뉴얼도 v0.3.0). 지난 갱신이 실제 배포/아티팩트에 도달하지 못한 것으로 보임.
- **복구(라이브)**: 배포 HTML을 v0.3.0 → **v0.4.1**로 끌어올림 — 히어로 배지·통계(797커밋·프로덕션 21)·진행현황 v0.4.0/v0.4.1 블록·버전표 2행 추가(“예정” 제거)·닫는 note + 매뉴얼 탭 A-2/A-4/A-5 보강·**A-7 신설(플로우 다이어그램)**·FAQ(다이어그램 편집). 같은 페이지 모순(남은항목의 “라이브러리 미리보기”=v0.4.0 구현됨) 교정.
- **다음 방향(공개 수위)**: 개요 탭에 “다음 방향” 3카드 추가(상황 적응형 진행 / 분기 단순화 / 라이브러리 UX). 내부 백로그 비공개 정책에 맞춰 약점·LLM 의존성·열린 질문은 제외하고 긍정 방향만 노출.
- **배포**: 프리뷰 배포 → 로컬 렌더 시각 검증(전 구간) → `vercel deploy --prod`(프로젝트 `coginsight-overview`) 승격 → 공개 URL 200·히어로 v0.4.1 재검증 완료.
- ⚠ **아티팩트(`1e30660a`) 미동기화**: 배포 HTML이 frame-runtime로 이중 래핑된 export라 Artifact 재발행 시 재래핑·손상 위험 → 자동 동기화 보류. 다음에 아티팩트로 편집할 땐 **라이브(v0.4.1) 기준으로 재작성** 필요. (드리프트 재발 방지: 라이브 HTML을 SoT로 두는 방안 등 별도 검토.)
- 저장소 문서(ROADMAP·PROJECT_SUMMARY·시연 가이드)의 다음 방향 반영은 아래 2026-07-20 (오후) 항목 참고.

### 2026-07-20 (오후) — 다음 방향 3항목 브레인스토밍 + 저장소 문서 반영 (📄 저장소 커밋 `efed680`)
> 📄 사용자와 브레인스토밍으로 향후 개선 3항목을 구체화해 저장소 문서에 기록. 큰 흐름 = **순차 플로우 → LLM 주도 상황 적응형 생성**. (SoT = 저장소 `ROADMAP.md` "다음 방향" 절.)
- **3항목**: ① **LLM 노드 상황 적응형 진행**(단일 agentic 노드로 다분기 + 조건 탈출, 현재 다중노드 `llmFlowChain` 일반화) ② **컨디션 노드 진입 라우팅 전용화**(중간 분기는 개별 노드 자체 조건) ③ **라이브러리 생성 UX**(다중 선택 → 관련 추가 설정 → 생성 전 예상 결과 미리보기).
- **저장소 반영** (브랜치 `docs/v0.4.1-refresh-and-demo`, 커밋 `efed680`): `ROADMAP.md`에 "다음 방향 (v0.5+ 후보)" 섹션 신설(항목별 현재/목표/관련코드/열린질문 + 백로그 교차참조), `PROJECT_SUMMARY.md`·시연 가이드에 요약 반영, 시연 가이드 스테일 교정(레퍼런스 플로우 미리보기=이미 구현).
- **위키 반영**: 위 [[#진행 현황|진행 현황]] 끝에 "다음 방향" 콜아웃 추가.
- **공개 개요 페이지**: 2026-07-21에 별도 반영 완료(내부 백로그 비공개 정책에 맞춘 공개 수위) — 아래 [[#진행사항 업데이트 로그|2026-07-21 로그]] 참고. 이 과정에서 라이브가 v0.3.0에 머물러 있던 드리프트를 발견·복구.

### 2026-07-20 — 공개 개요 페이지 "사용 매뉴얼" 탭 v0.4.x 최신화 + 아티팩트 드리프트 해소 (📄 라이브 배포·시각 검증) ⚠ 실제 반영 안 됨 — [[#진행사항 업데이트 로그|2026-07-21 정정]]
> 📄 사용자 "공유문서에 반영은 되었는데 사용자 메뉴얼이 최신화되지 않았어". 확인 결과: v0.4.0·v0.4.1 페이지 갱신은 **개요 탭(히어로·통계·버전표)만** 손댔고 **`사용 매뉴얼` 탭은 v0.3.0 기능에 멈춰 있었음**(플로우 시각화·결과 탭 사용자별 보기 둘 다 매뉴얼에 없음). 편집 원본 아티팩트 `1e30660a`도 전체가 v0.3.0로 남은 **알려진 드리프트**(위 7/15 v0.4.0 로그 참고).
- **매뉴얼 탭 보강(6곳)**: ① A-2 레퍼런스로 시작 — 요약 카드 `크게 보기`로 다이어그램 미리보기(v0.4.0) ② A-4 라이브러리 — 항목별 `미리보기`(v0.4.0) ③ A-5 결과 상세 "생성된 JSON" — `JSON/다이어그램` 뷰 토글(v0.4.0) ④ A-5 결과 목록 — `사용자` 필터 + `사용자별로 묶어 보기` 토글(v0.4.1) ⑤ **신설 A-7. 플로우 다이어그램 보기(v0.4.0)** — 진입점 4곳·구조/사용자흐름 2뷰·범례·PNG·풀스크린·읽기전용 ⑥ FAQ에 "다이어그램 편집 가능?"(읽기전용) 항목.
- **배포**: 라이브 HTML을 편집 → `coginsight-overview` Vercel 프로젝트에 프리뷰 배포 → **로컬 렌더로 매뉴얼 탭·A-7·플레이스홀더 figure 시각 검증** → 프로덕션 승격. ⚠ 이날 Vercel 빌드가 Initializing에 ~7–10분 지체(플랫폼 지연). 공개 URL(https://coginsight-overview.vercel.app) 6개 항목 전수 재검증.
- **아티팩트 재동기화**: `1e30660a`를 라이브(v0.4.1+매뉴얼)와 동일 내용으로 재발행 → **개요 탭 v0.3.0 드리프트도 함께 해소**(이제 아티팩트=라이브 일치). 파비콘 📊.
- **교훈**: 공개 페이지 갱신 시 **개요 탭만이 아니라 `사용 매뉴얼`·`관리자` 탭도 함께 검토**하고, `vercel --prod` 후 **아티팩트(source of truth)도 반드시 재동기화**할 것(안 하면 이번처럼 드리프트 누적). SoP 반영.
- **(같은 날 후속) A-7 그림 실제 캡처 채움**: A-7 figure가 플레이스홀더(빈 박스)여서 사용자 요청으로 **가장 최근 생성 결과("올인원 물류봇", `/results/e72f4e26…`)의 다이어그램 뷰**를 라이브 앱에서 캡처. 앱의 `PNG 내보내기`로 받은 이미지(범례·5개 시나리오 플로우·미니맵·컨트롤 포함, 1592×920)를 base64 PNG로 A-7에 임베드(페이지 1.78→2.27MB). 로컬 렌더 검증 → `vercel --prod` 재배포 → 라이브 시각 확인 → 아티팩트 재동기화. **관리자 탭도 v0.4.x 검토 완료 = 반영 대상 없음**(v0.3.1→v0.4.1 admin 코드 변경 0건, FlowCanvas를 import하는 admin 화면 없음).

### 2026-07-15 — v0.4.1 결과 탭 사용자별 보기 (📄 저장소 직접 구현·main 직접 릴리스)
> 📄 사용자 "0.4.1로 바로 마스터에 적용 — 결과 탭에서 사용자별·카테고리별로". 확인 결과 결과에 명시 '카테고리' 필드 없음(산업군은 일부만 기록) → 사용자 확정 **"사용자별로만"**. 표시 = **필터 + 그룹 토글**.
- **구현**: `ResultsList`(`/results`)에 ① **사용자 필터 드롭다운**(전체/각 `generation_tiers.created_by`, 없으면 '(미상)') ② **"사용자별로 묶어 보기" 토글**(켜면 사용자 이름순 섹션 헤더 `👤 사용자 (N)`로 그룹). 기존 검색·정렬 유지. 프론트 전용(백엔드·DB 무변경).
- **릴리스(main 직접, 사용자 요청)**: PR **#107** → main `3b68501`, tag **v0.4.1** + GitHub Release, package.json 0.4.1. dev 사이클 생략(프론트 전용·저위험). 검증 build green + deno lib 27/0. Vercel 자동 배포(앱 200).
- **공개 개요 페이지 v0.4.1 반영(사용자 "반영해줘")**: 히어로 배지·버전 통계(v0.4.1)·커밋(797), 버전표 v0.4.1 행("결과 탭 사용자별 보기"), 푸터 노트 갱신 후 `vercel --prod` 재배포·라이브 검증. (기능 본문은 v0.4.0 플로우 시각화 기준 유지 — v0.4.1은 버전표·현행 표기만.)

### 2026-07-15 — v0.4.0 프로덕션 릴리스 + 공유 노트 최신화 (📄 4축 실행·라이브 검증)
> 📄 사용자 "이걸로 릴리스하자, 공유 노트도 최신화". **프론트엔드 전용**이라 4축 중 ②DB·③엣지함수는 해당 없음.
- **① 코드**: PR **#106** → main `52a0f59` 머지, **tag `v0.4.0` + GitHub Release** 생성. CHANGELOG `[0.4.0]` 날짜 2026-07-15 확정. 릴리스 게이트: `npm run build` green + `deno test` **260/0**.
- **② DB / ③ 엣지함수**: **해당 없음**(마이그레이션·`supabase/functions` 변경 0 — `git diff main..HEAD` 확인). dev 테이블·슬러그도 무변경이라 dev 리셋 실질 no-op.
- **④ 프론트**: main 푸시 → **Vercel 자동 배포**, https://coginsight-generator.vercel.app 200 확인.
- **공유 노트 최신화(사용자 요구)**: ⓐ **공개 개요 페이지**(https://coginsight-overview.vercel.app) — 페이지 **전체를 프로덕션 = v0.4.0 기준**으로 정정: 히어로 배지·버전 통계(v0.4.0, 2026-07-15)·커밋 795, 인트로·진행현황 h3, 버전표 v0.4.0 행(예정→릴리스)·v0.4.0 소개 섹션. ⚠ 1차 배포 때 v0.3.0 버전표 행 커밋수를 795로 잘못 바꿨던 것 741로 복구. `vercel --prod` 재배포·라이브 전 항목 검증. ⓑ **[[CogInsight-Generator-링크]]** 위키 노트 v0.4.0 갱신. ⚠ 개요 아티팩트(1e30660a)는 배포본 직접 수정이라 v0.3.0 기준으로 남음(드리프트 — 링크 노트에 기록).
- ⚠ **릴리스 후 확인(수동, 잔여)**: 사용자 흐름도 PNG 외관(OQ2). 잔여 기능은 v0.5(편집 역반영·DRY 추출·중첩 반복·이미지 외 내보내기).

### 2026-07-15 — v0.4.0 구조 다이어그램에도 턴 경계(사용자 응답 대기) 표시 (📄 저장소 직접 구현, 커밋 `cb92631`)
> 📄 사용자: 구조 다이어그램에도 사용자 응답 대기 플로우가 보여야 함.
- **봇 응답(output/llmloop) 노드에서 나가는 엣지 = 사용자 응답 대기 경계**로 판단 → **점선(파란색) + `⏳ 응답 대기` 라벨**(분기면 조건 라벨=사용자 선택 유지). ⚠ **API 결과 분기 등 내부 분기(condition/node 출발)는 실선 유지**(사용자 턴 아님 — 예: 조회 성공/실패). 본문(반복 내부) 엣지도 동일 적용. 범례에 '사용자 응답 대기(점선)' 항목 추가. build+lib green. 🧠 위 [[#진행사항 업데이트 로그|턴 교대 모델]](발화↔응답) 원칙을 사용자 흐름도에 이어 구조 뷰에도 일관 적용.
- **후속 수정(커밋 `cf020a7`)**: "응답 대기" 등 엣지 라벨이 노드에 겹치는 경우 → 라벨을 **두 노드 사이 정중앙**(source·target 좌표 중점, 랭크 간 빈 공간)에 배치하고 `ranksep` 56→72로 여유 확보.
- **재수정(커밋 `e209d26`)**: 정중앙 배치로도 **좁은 간격(반복 본문 ~22px)에선 텍스트가 여전히 겹침** → 턴 경계는 텍스트 없이 점선으로만 표시(임시).
- **최종(커밋 `cefbd9a`)**: 점선이 **좁은 간격에서 잘 안 보임** → 봇 응답 뒤 턴 경계에 엣지 중앙 **`⏳ 응답 대기` 파란 배지**(`WaitEdge`)로 변경 + 배지 여유 위해 **간격 확대**(`ranksep` 84·반복 본문 46). 범례도 배지로 갱신. 분기 조건 라벨 유지. 🧠 dev는 소스 직접 편집→vite HMR 반영(강력 새로고침 필요할 수 있음).
- **반복 본문 겹침 최종 수정(커밋 `61281a1`)**: 사용자 재보고 — s2 반복 본문에서 응답 대기 배지가 "수집 종료 처리" 노드 위에 겹침. 원인: 본문 입력받기(output)가 **[수집 종료·값 저장] 두 갈래**인데 **세로 스택**이라 입력받기→값저장 엣지가 사이 노드를 건너뜀. → **본문도 dagre로 배치**(갈래 나란히) + 본문 분기 조건 라벨(`refDiagram` bodyEdges에 condition 추가) + `conditionLabel` 부정 인식(`그만`/`그만 아님`). deno 260/0.

### 2026-07-15 — v0.4.0 사용자 흐름도: 턴 교대(발화↔응답) 모델 반영 (📄 저장소 직접 구현, 커밋 `e32c91f`)
> 📄 **사용자 제공 도메인 원칙**: 이 챗봇은 기본적으로 **사용자 발화 ↔ 챗봇 응답의 왕복**이라, 봇이 한 번에 두 답을 못 하고, 답 이후엔 사용자 응답을 기다린다. 이를 흐름도에 반영 요구.
- **내부 처리 접기**: api(조회)·esd(기록 저장)는 별도 봇 답변이 아니라 **다음 봇 응답의 처리 주석**(`⚙ 처리: 조회 · 기록 저장`)으로 접음.
- **턴 교대 강제**: 봇 답변이 연달아 나오면(=두 번 답) 사이에 **`⏳ 사용자 응답을 기다림`** 구분선 삽입 → 봇-봇 인접 제거(`interleaveWaits`).
- 테스트 2건 추가, deno **260/0** + build green. 🧠 이 원칙은 흐름도뿐 아니라 생성 로직 이해에도 쓰이는 [[CogInsight-Generator]] 도메인 상식.
- 🧠 **동향 주석 (2026-08-04 추가)**: 이 턴 교대 전제와 **충돌하는 업계 사례가 3건** 모였다 — ① 오픈AI **GPT-Live = `turnless speech model`**(턴 개념 자체를 없앤 실시간 음성 아키텍처, → [[AI-주간-소식-2026-W32]]) ② arXiv **Transcript-Managed Transformers**(대화를 턴이 아니라 *경계 블록 채널*로 분할, W32) ③ **AI쇼핑 예측형 에이전트**(봇 선제 발화, → [[AI-주간-소식-2026-W31]]). 🧠 지금 당장 바꿀 건 없으나, **턴 경계를 코드에 암묵 전제로 두지 말고 스키마의 명시적 필드로 빼두는 것**이 음성·선제발화 채널 확장의 탈출구다(제안, 미착수).

### 2026-07-15 — v0.4.0 사용자 흐름도 목록화 (📄 저장소 직접 구현, 커밋 `ad87f0e`)
> 📄 사용자: 사용자 흐름도가 보기 어렵고 내용이 다 안 나옴 → 목록화·시나리오별·전문 표시 요구.
- **내용 잘림 해소**: `deriveUserFlow`가 봇 멘트를 **60자에서 자르던** 것 제거 → **전문 표시**(회귀 테스트 추가, deno lib 25/0).
- **목록화**: 좌/우 스윔레인 테이블 → **시나리오별 세로 목록**(단계 번호 + 화자 배지 🙋 사용자/🤖 봇 + 전문(줄바꿈) + 선택지 칩 + 반복 표시, 폰트·행간 확대). 한 쪽 칸이 비던 스윔레인 대비 가독성↑·내용 전부 노출.
- ⚠ 미확인(사용자 몫): dev에서 목록 가독성·전문 표시 육안 확인.

### 2026-07-15 — v0.4.0 릴리스 준비 (📄 문서 완성·검증 게이트, 커밋 `2453234`)
> 📄 사용자 "릴리스 준비해줘, 곧 릴리스" → 실제 릴리스(main 머지·태그·배포)는 "프로덕션에 머지" 명시 시 진행하고, 이번엔 문서·검증만 완료.
- **계획 대비 미개발 = 없음 (📄 기획서 R1~R5·backlog T1~T7 전부 done)**. 남은 건 v0.5/후속(편집·DRY 추출·중첩 반복·PDF export)과 릴리스 후 수동 확인 1건(OQ2 사용자 흐름도 PNG 외관)뿐.
- **문서 완성**: CHANGELOG `[0.4.0]`에 핵심 산출물(refDiagram·FlowCanvas·진입점 4곳·의존성) 항목 추가·"릴리스 전 TODO" 해소·잔여(v0.5)·릴리스 후 확인 명시. ROADMAP v0.4.0 `(예정)`→`(구현 완료·릴리스 준비)`. 올림푸스 backlog T7 `[doing]`→`[done]` 정정.
- **검증 게이트**: `npm run build` green + `deno test` **257 passed/0 failed**. 브랜치 main 대비 33커밋 ahead.
- 🧠 **v0.4.0은 프론트엔드 전용** → 릴리스 4축 중 ②DB·③엣지함수 **해당 없음**. 실제 릴리스 = PR 머지 → tag `v0.4.0`+GitHub Release → Vercel 자동 배포(번들 0.4.0 확인) → dev 리셋 규약 확인(프론트 전용이라 dev 테이블 diff 0) → 공개 개요 문서(coginsight-overview) 갱신. **사용자 "프로덕션에 머지" 대기.**

### 2026-07-15 — v0.4.0 구조 다이어그램: 시나리오=단일 흐름(반복 구획화) (📄 저장소 직접 구현·검증)
> 📄 사용자 관찰: "회사 솔루션은 **하나의 시나리오=하나의 플로우**인데, 다이어그램은 한 시나리오에 여러 인입이 있는 것처럼 보인다 → 하나의 흐름으로." 같이 원인 진단 후 방향 확정.
- **원인 진단 (📄 `deriveStructure`)**: 반복(`subdialog`) **본문 노드를 화면 노드로만 추가하고 연결 엣지를 안 만들어**(라인 123~) 떠 있는 노드가 됨 → dagre가 상단(진입점)에 배치 → "여러 인입"처럼 보였음. (분기는 하나의 진입에서 갈라지므로 원인 아님.)
- **해결 방향 (📄 사용자 확정: "반복 구획 안에 본문")**: 반복을 **레이블된 박스**로 렌더, 본문을 그 안에 담아 메인 흐름을 `진입→…→[반복 박스]→다음` **단일 스트림**으로.
- **구현 (📄)**: ① `refDiagram`에 `loop.bodyEdges`(본문 내부 then 엣지) 파생 추가 ② 새 `loopGroup` 노드(id=subdialog) — "🔁 반복 · {label} · 최대 N회" 박스, 본문 노드를 `parentId`+`extent:'parent'`로 박스 안 세로 스택 ③ 시나리오 dagre는 반복을 박스 크기 단일 노드로 취급(메인 엣지 그대로 연결) ④ 3계층 중첩(scenarioGroup→loopGroup→본문), loopGroup 고정·본문은 박스 내 이동 ⑤ 범례 '반복'을 구획 미니어처로 갱신.
- **검증 (📄)**: `npm run build` 2065 modules + `deno test` **256 passed/0 failed**(신규 bodyEdges 테스트 포함). 커밋 3개(spec `32c3d85`→feat `9403b5e`→changelog), 브랜치 push(`99d9bfb..1c5eb1d`).
- **추가 UX (📄 같은 날, 사용자 요구)**: 시나리오 그룹/반복 박스의 **빈 영역을 드래그하면 캔버스가 패닝(화면 이동)**되게 — 그룹 노드 wrapper를 `pointerEvents:'none'`으로 두어 드래그가 뒤의 react-flow pane으로 통과(그룹 노드 표준 패턴). 헤더 드래그(그룹 이동)·노드 상호작용은 유지. 커밋 `3636149`.
- **추가 다듬기 #2·#3 (📄 같은 날)**: ② **긴 분기 조건 호버 전문** — 커스텀 `BranchEdge`(EdgeLabelRenderer)로 CSS 말줄임 + 마우스 오버 시 전문. ⚠ 초기 구현은 호버 미동작(EdgeLabelRenderer 라벨에 `nodrag nopan` 클래스 누락) → **`nodrag nopan`+`pointerEvents:all`+커스텀 다크 툴팁으로 수정**(커밋 `41df756`). ③ **반복 박스 이동** — `loopGroup` draggable + `dragHandle`(헤더 `.loop-drag-handle`)·`extent:'parent'`로 시나리오 박스 안에서만 이동(빈 영역은 여전히 패닝).
- ✅ **#1 해결 — 반복 박스 분리(여러 인입) 버그 (📄 실데이터 진단·수정, 커밋 `1115a4f`)**: 사용자가 준 `올인원 물류봇_v2` flow_json을 `deriveStructure`로 직접 돌려 진단 → "여러 송장 조회"(s2)가 `s2 → s2_set1__collectinit → **s2_set1__collect__init(`__init`)** → s2_set1__collect(반복 박스)` 구조인데, refDiagram이 **`__init` 노드로의 엣지를 버리기만 해** 반복 박스가 진입 엣지 없이 떠(indeg 0=별도 진입점) 분리돼 보였음. **`resolveVisibleTargets`로 `__init` 스캐폴딩을 건너뛰어 실제 노드로 엣지를 브리지**(메인·본문 공통) → s2가 단일 흐름(진입점 1개)으로 연결. 회귀 테스트 추가, deno **257/0**. 🧠 이 패턴(수집/반복 init 스캐폴딩)은 다른 수집형 시나리오에도 흔해 광범위 개선.
- **추가 다듬기 (📄 같은 날, 커밋 `8381da5`)**: ① **범례 초기값 닫힘**(useState(true)). ② **풀스크린 시 현재 프레이밍 그대로 확대** — react-flow가 컨테이너가 커져도 transform을 유지해 내용이 안 커지고 여백만 생기던 문제 → `onInit`로 인스턴스 캡처 후 풀스크린 전환 시 뷰포트 재조정. build+lib green.
  - ↳ (사용자 요구로 방식 변경, 커밋 `ca0dd36`) `fitView`(전체 맞춤) → **뷰포트 중심·배율 보존**: 전환 직전 중심 flow 좌표·배율·컨테이너 크기 저장 → 전환 후 같은 중심 유지 + 컨테이너 증가 비율(작은 축 기준)만큼 배율 확대(복귀 시 원복). 지금 보던 위치 그대로 같은 비율로 커짐.
- ⚠ **한계/미확인**: 중첩 반복(본문 안 또 다른 반복)은 평면 렌더(향후). 전 라우트 OTP 게이트라 자동 구동 불가 → dev 서버에서 **반복 포함 시나리오가 단일 흐름 + 반복 박스 안 본문으로, 떠 있는 노드 사라졌는지 + 빈 영역 드래그 패닝** 육안 확인 필요(사용자 몫).

### 2026-07-15 — v0.4.0 구조 다이어그램 가독성 개선 (📄 저장소 직접 구현·검증)
> 📄 사용자 요구(구조 다이어그램 대상): ① 긴 글자 잘림 → 호버로 전문 ② 시나리오 통째 이동 ③ 색 구분 대신 **플로우차트 범례/도형**. 개발 방식 = 이 세션 직접 구현(v0.4.0 브랜치). 사용자 확정: 노드는 그룹 박스 밖으로 못 나가게, **다이어그램은 현재 상태를 보여주는 뷰라 실제 수정은 안 됨**(읽기 전용).
- **① 표준 플로우차트 도형 + 범례 (📄)**: 색만이 아니라 **타입별 SVG 도형**으로 구분 — 안내=둥근사각, 입력=평행사변형, 분기=마름모(의사결정), 저장=사각, 반복=이중테두리, API 연동=육각형, 기록 저장=원통(DB), AI 응답=사각+✦. 좌상단 **범례 패널**(도형↔의미) 추가. 도형은 배경 SVG + 라벨 오버레이(clip-path 텍스트 잘림 회피). 매핑은 새 순수 모듈 `src/lib/nodeShape.js`(`shapeForType`) + deno 테스트 3건.
- **② 긴 라벨 (📄)**: 노드 안 2줄 클램프 + **마우스 오버 시 스타일링된 툴팁으로 전문 표시**(기존 밋밋한 브라우저 title 대체).
- **③ 시나리오 통째 이동 (📄)**: 콘텐츠 노드를 그룹의 react-flow 자식(`parentId`+`extent:'parent'`)으로 편입, 그룹 `draggable` → **그룹 드래그 시 시나리오 전체 이동, 그룹 박스 밖으론 못 나감**. 읽기 전용 불변(연결/추가/삭제 없음, flow_json 미수정 — 화면상 재배치만).
- **스코프 (📄)**: FlowCanvas 구조 뷰만 수정. `refDiagram`·사용자 흐름도·결과/레퍼런스 배선 무변경. 노드 박스 크기 168×56→190×88(도형·2줄 라벨 수용).
- **검증 (📄)**: `npm run build` 2065 modules + `deno test` **253 passed/0 failed**(250+신규 3, 회귀 0). 커밋 spec `0df8612`류 3개(spec→feat `c85c845`류→changelog), 브랜치 push(`f4910fb..c85c845`).
- **UI 다듬기 후속 (📄 같은 날, 사용자 추가 요구)**: ① **범례 접기/펼치기** 토글 ② 시나리오 그룹은 **헤더(dragHandle)만** 잡아야 이동(본문 클릭 시 이동 안 함) ③ **분기 화살표에 조건 라벨** — 출력 2개 이상 분기의 각 엣지에 조건 표시(`refDiagram` 엣지에 대상 condition·label 실음 + `conditionLabel()` humanize: `includes('X')`→`X`, 조건 없으면 선택지 라벨 폴백). deno 테스트 누적 **255/0**, build green. 커밋 `99d9bfb`.
- ⚠ **미확인(사용자 몫)**: 전 라우트가 로그인(OTP) 게이트라 자동 구동 불가 — dev 서버(로그인 상태)에서 **도형·범례(접기)·호버 툴팁·그룹 헤더 드래그(박스 내 제한)·분기 엣지 조건 라벨** 육안 확인 필요.

### 2026-07-15 — v0.4.0 확장: 생성 결과에도 플로우 시각화 (📄 저장소 직접 구현·검증)
> 📄 사용자 요구: "레퍼런스에서만 되는 시각화를 **생성된 결과에서도 보고 싶다**". 개발 방식 = **v0.4.0 브랜치에 포함·이 세션이 직접 구현**(올림푸스 X, 사용자 확정). v0.4.0 스코프가 "레퍼런스 + 생성 결과 플로우 시각화"로 확장됨.
- **핵심 (📄)**: 생성 결과 `result.generated_json`이 시나리오 레퍼런스와 **동일한 `{ dialogs:[{id:"main",...}] }` 구조**임을 확인(생성기 flow 모듈도 이 형태로 동작) → **`FlowCanvas`·`refDiagram` 그대로 재사용**(신규 파생/시각화 로직 0). 배선만 추가.
- **진입점 2곳 (📄, 사용자 확정 "둘 다")**: ① `ResultDetail.jsx`(`/results/:id` 테스터 상세) "생성된 JSON" 섹션에 `[JSON | 다이어그램]` 뷰 토글(다이어그램 시 FlowCanvas 인라인 32rem) ② `results/ResultDetailModal.jsx`(`/results` 목록 모달) 동일 토글(24rem).
- **모달 ESC 가드 (📄)**: 모달이 Radix Dialog(ESC로 닫힘)라 FlowCanvas 브라우저 풀스크린 중 ESC 중첩 방지 — 공용 `common/Modal.jsx`에 선택적 `onEscapeKeyDown` 패스스루(추가·하위호환) + 모달은 `document.fullscreenElement`면 preventDefault(v0.4.0 T7 방어 가드와 동일 취지).
- **가드/스코프 (📄)**: `generated_json`에 `dialogs/main` 없으면 토글 숨김(빈 다이어그램 방지). 프론트 전용 — DB·엣지함수·마이그레이션 무변경. API 정의·ESD 스키마는 별도 산출물이라 시각화 대상 아님(JSON 그대로).
- **검증 (📄)**: VERIFY_CMD 전부 통과 — `npm run build` **2065 modules** + `deno test` **250 passed/0 failed**(회귀 0, refDiagram/FlowCanvas 무변경). 커밋 3개(spec `0df8612` → feat `0b174a2` → changelog `f4910fb`), 브랜치 push 완료(`410e8c2..f4910fb`).
- ⚠ **미확인 (사용자 몫)**: dev 서버(`VITE_DEV_TABLES=true`)에서 실제 결과 1건 열어 두 뷰·PNG·풀스크린 **육안 확인** — 사용자가 개발 서버 확인 중.
- 🧠 다음 결: 릴리스 전 CHANGELOG [0.4.0] Added를 v0.4.0 전체 산출물로 채우기(현재 이번 항목만 기입, 레퍼런스 시각화 항목 미기입 명시).

### 2026-07-14~15 — v0.4.0 레퍼런스 플로우 시각화: [[올림푸스-Olympus]] 자율 개발 완료 (📄 저장소·올림푸스 state 직접 확인)
> 📄 7/9 저녁 착수(기획서만 작성)한 v0.4.0을 **올림푸스가 자율 개발해 dev에서 완주**. **main 미머지·프로덕션 무배포**(dev 전용, 사용자 "프로덕션에 머지" 시 4축 릴리스). 브랜치 `feat/v0.4.0-reference-visualization`(main 대비 8커밋 `a3f53df`~`1286a7b`), working tree clean.
- **구현 산출물 (📄 `git diff --stat main...HEAD`, 총 +1,565줄)**:
  - `src/lib/refDiagram.js`(신규 220줄) + `refDiagram.test.js`(신규 286줄) — **구조/usecase 두 모델 파생 순수 함수**. `deriveStructure`(시나리오 그룹·노드·엣지·루프)와 `deriveUserFlow`(user/bot 교대 스텝, 반복 접기, 내부 노드 숨김). v0.3.0 `refSummary.js`와 동일 파생 기준(welcome/anythingelse 제외·then-우선 DFS·`__init` 숨김). ⚠ TYPE_KO/walk/firstOutputText는 refSummary에서 **복사**(공유 모듈 미추출 — v0.5로 연기, OQ1).
  - `src/components/flow/FlowCanvas.jsx`(신규 649줄) — **react-flow 캔버스 뷰어**. 뷰 토글 [구조 다이어그램 ↔ 사용자 흐름도], dagre 자동 레이아웃(세로 계층·시나리오 그룹 구획), 피그마류 UX(휠줌·팬·fit-view·도트그리드·노드>30 미니맵), 타입별 노드 스타일. 사용자 흐름도 = **산출물 품질 스윔레인**(문서형 헤더·범례·흰 배경·브랜드톤 `#0052CC`·개발용어 노출 금지). **PNG 내보내기**(기존 `html-to-image` 재사용, 흰배경·2배·`coginsight-flow-{레퍼런스명}.png`, 컨트롤/미니맵/그리드 제외), **풀스크린**(Fullscreen API·ESC). 읽기전용이되 `readOnly` prop + `onNodesChange` 체계 유지(v0.5 편집 확장 대비).
  - `ScenarioRefSelect.jsx`(+78) — 설문 시드카드에 소형 구조 미리보기 + "크게 보기" → 전체화면 뷰어("흐름: a→b" 텍스트 대체).
  - `ScenarioLibrary.jsx`(+48) — `/scenarios` 카드마다 "미리보기" 버튼 → 뷰어(다운로드·조립 동작 불변).
  - `package.json`(+deps `@xyflow/react` ^12.11.2, `@dagrejs/dagre` ^3.0.0 — 프로젝트 첫 시각화 의존성) + `scripts/ensure-deps.mjs`(predev/prebuild가 node_modules 미설치 자가치유).
- **검증 (📄 올림푸스 `state/.../verify.txt`, `handoff.json` status=green)**: **deno 250 passed / 0 failed**(기존 249 + T6 신규 1, 회귀 0), `npm run build` **2065 modules** 성공(실번들에 xyflow/dagre 포함 실증). ⚠ `supabase/functions/test/` 8 failed는 **6월 제거된 레거시 값-할당 엔진 테스트로 스코프 밖·선재**(v0.2.1부터 동일, v0.4.0 무관).
- **개발 경위 (📄 `state/.../decisions.md`)**: 7/9 최초 기동이 **greenfield 오기동**(빈 `-v0.4.0` 디렉토리를 TARGET_REPO로 물어 needs_clarification)·**검증 권한 블로커**(acceptEdits 모드가 npm/deno 프롬프트로 차단) 2회 중단 후, `run.env` 기반 올바른 env(brownfield·`GIT_BRANCH`·권한)로 **재기동해 7/14 M0 재개→7/15 완주**. 백로그 T1~T7 의존순 분해(refDiagram → 캔버스셸+구조뷰 → 사용자흐름도+PNG+풀스크린 → 시드카드 → 라이브러리 → 회귀테스트 → ESC 가드) 전부 Critic GREEN + metis 승인.
- **잔여·미확인 (📄 `state/.../open-questions.md`)**:
  - ⚠ **OQ2 (사용자 수동 확인 필요)**: 사용자 흐름도 PNG가 흰배경·컨트롤 제외로 **보고서 삽입에 적합한 외관인지 사람 눈 확인** — 자동 판정 불가 항목. → 🧠 사용자가 dev(`VITE_DEV_TABLES=true`)에서 직접 내보내 확인 권장.
  - 🧠 OQ1(v0.5): refDiagram/refSummary 공유 파생 헬퍼를 `refDerive.js`로 추출(DRY). OQ3(v0.5): `readOnly` prop이 현재 destructure만 되고 미배선(편집은 하드코딩 비활성) — v0.5 역반영 확장 시 실배선.
- 🧠 **다음 결**: v0.4.0 프로덕션 릴리스(사용자 "프로덕션에 머지" 시 4축 — 단, 프론트 전용이라 DB·엣지함수 무변경) / 사용자 흐름도 PNG 외관 확인(OQ2) / ⚠ **CHANGELOG [0.4.0] Added 항목이 아직 비어 있음**(릴리스 전 저장소에서 채워야 — refDiagram·FlowCanvas·2진입점·PNG·풀스크린).

### 2026-07-09 — v0.3.1 프로덕션 릴리스: LLM 모델 gpt-4o → gpt-5.2 (📄 git·CHANGELOG)
- **변경 (PR #105 → main `4429c25`, tag v0.3.1)**: 생성기가 OpenAI를 호출하는 **5개 엣지함수 전부**(`coginsight-generator` 공용 `callLlm` 어댑터 `LLM_MODEL`·`learn-rules` 3콜·`learn-solution-rules`·`derive-node-specs`·`admin-solution-rules`)의 모델을 `gpt-4o` → `gpt-5.2`로 전환. v0.4.0(레퍼런스 시각화) dev 사이클과 무관한 **독립 패치**로 main에서 격리 브랜치(`fix/llm-gpt-5.2`)로 릴리스 → 이후 v0.4.0 브랜치로 병합(dev도 gpt-5.2로 생성).
- **키 로테이션**: 프로젝트 전역 시크릿 `OPENAI_API_KEY`를 신규 키로 교체(dev/프로덕션 슬러그 공유). 구 키 revoke는 계정 측 조치.
- **검증**: 새 키+모델 OpenAI 200, flow 테스트 54 green.
- ⚠ **알려진 이슈**: `flow/usage.ts`의 `GPT4O_PRICING`이 아직 gpt-4o 단가(입력 $2.5/출력 $10 per 1M) 기준 → `estimated_cost_usd` 부정확. gpt-5.2 실단가 확인 후 갱신 예정.
- 🧠 생성 결과물(챗봇 llmloop 노드)의 출력 모델은 사용자가 CogInsight 솔루션에서 직접 입력하므로 무변경.

### 2026-07-09 (저녁) — v0.4.0 dev 사이클 착수: 기획서 작성(올림푸스 자율 개발 예정) (📄 사용자 지시)
- **개발 방식 (📄 사용자)**: v0.4.0은 이 세션이 직접 구현하지 않고 **[[올림푸스-Olympus]]가 자율 개발** — 기획요청서만 작성. spec 위치: `olympus/spec/CogInsight-Generator-v0.4.0/기획.md`(**버전 포함 폴더명** — state 격리로 다른 버전 기획 병행 가능, [[올림푸스-기획요청서-작성요령]] 규약 추가).
- **스코프 (📄 사용자 확정 요구)**: ① 기본 = **구조 다이어그램**(시나리오별 그룹, 전체 구조) ② **사용자 usecase 흐름도**(user/bot 스윔레인, **산출물 품질** — 보고·공유용, PNG 내보내기 = 기존 html-to-image 재사용) ③ 전체 화면 + 피그마류 캔버스 UX(팬/줌·fit-view·미니맵) ④ **v0.5 드래그앤드롭 편집 대비 구조**(react-flow onNodesChange 체계, 이번엔 보기 전용). 파생은 refSummary 기준 재사용(순수 모듈 refDiagram + deno 테스트).
- **의존성 결정 (📄 사용자 승인)**: `@xyflow/react`(react-flow v12) + dagre 도입 — 피그마류 UX·향후 편집 요구로 자체 SVG 대신 채택(프로젝트 첫 시각화 의존성).
- **환경**: 브랜치 `feat/v0.4.0-reference-visualization` 생성·push(0.4.0 선반영, 배지 `v0.4.0 DEV`), CHANGELOG [0.4.0] 미릴리스 섹션. 올림푸스 실행은 `AUTO_MERGE=0 DEPLOY_ON_DONE=0`(DEV 규약 — main 머지·배포 금지) + `PROJECT`/`TARGET_REPO` 동시 지정.

### 2026-07-09 (오후) — v0.3.0 프로덕션 릴리스: 시나리오 레퍼런스 라이브러리 (📄 4축 실행·라이브 검증)
- **릴리스 (사용자 "프로덕션에 머지" 지시)**: PR #103 → main `ae99f4d` → tag v0.3.0 + GitHub Release. CHANGELOG [0.3.0] 날짜·검증 요약 확정, ROADMAP v0.3.0 릴리스 표시(잔여 항목 4·6 백로그 이동), compare 링크 정리 — "버전 라벨링 전체 정리" 지시 반영.
- **DB**: dev↔prod diff 0(questions·solution_rules 내용 기준) → `db push`(20260707120000, screenshot_path 컬럼 재조회 검증) → **레퍼런스 5종 승격**(📄 사용자 선별: 도매 제외 — 금융·물류·소매·의료·기타, INSERT…SELECT id 유지, 프로덕션 재조회 검증).
- **엣지함수·프론트**: 전 슬러그 27종 main 기준 재배포(프로덕션 20 + dev 래퍼 7). **프로덕션 스모크 생성 1회**: collect-loop 재사용 → 201·checkBot 통과·`injected=true` `picked=[계좌 잔액 조회봇]`(승격 레퍼런스가 프로덕션 few-shot에서 실제 동작함을 확인) → 결과 행 삭제. Vercel 자동 배포, 번들 0.3.0 확인(0.2.2 흔적 0).
- **dev 리셋(개발 서버 세팅)**: 5개 dev 테이블 규약대로 재시드/비움 + 내용 diff 0 검증 + 스토리지 `dev/` 정리(Storage API — SQL 직접 삭제는 보호장치로 차단됨) + dev 슬러그 main 기준. ⚠ 질문 id 재발급. ⚠ 의도된 diff: **도매 레퍼런스는 dev 보존**(dev가 유일 소스 — 배열 누적 품질 교정 후 승격, dev 6 = prod 5 + 도매 1).
- **공개 문서**: coginsight-overview 히어로 배지 "프로덕션 v0.3.0"·통계(741커밋·엣지함수 27(프로덕션 20)·마이그레이션 64)·버전 히스토리 v0.3.0 행 릴리스 확정 → 재배포 200 + 아티팩트 동기화(label v0.3.0-release).
- 🧠 다음 결: v0.4.0(레퍼런스 다이어그램 시각화) 계획 유지, 백로그 = 다중 후보 관련도 스코어(레퍼런스 추가 제작 선행)·라이브러리 미리보기 모달·placeholder-leak 원인·도매 레퍼런스 교정·레거시 test/ 스위트 8건 정리.

### 2026-07-09 (오후) — v0.3.0 릴리스 사전점검 + 조립 생성 테스트(로드맵 항목 3 ✅) — 조립기 실버그 발견·수정 (📄 dev 실행·git)
- **사전점검 (릴리스 판단용)**: deno 스위트 366 통과(실패 8건은 v0.2.1에서도 동일한 **레거시 값-할당 엔진 테스트** — 6월 제거 기능의 낡은 테스트로 무관 확인), 프론트 빌드 통과, **회귀 하네스 4 fixture 전수 PASS**(`runs/2026-07-09-v0.3.0-precheck.json` — few-shot 산업군별 올바른 선택·시드 경로·api-esd 포함. 7/6의 placeholder-leak은 이번 실행에선 미재현 — 🧠 원인 미규명이라 백로그 유지).
- **조립 생성 테스트 (사용자 지시)**: 신규 도구 `scripts/scenario-refs/assembleCheck.ts` — dev 레퍼런스 6종의 2개 이상 **전 조합 57건**을 `scenario-references-dev?action=assemble` 실호출 + checkBot 불변식·조립 고유 검사(id 중복·welcome 유일).
- 🐛 **실버그 발견·수정**: `assembleScenarios`가 루프(subdialog)의 **`body` 참조를 도달성 탐색·id prefix 재작성 양쪽에서 누락** → 루프 봇(도매·의료) 포함 조합에서 본문 노드 소실+dangling(46/57 FAIL, 무한 반복 위험 — 개별 봇은 게이트 통과라 조립에서만 드러남). then과 동일하게 body 탐색·재작성으로 수정(TDD, deno 233 green), `scenario-references-dev` 재배포 후 **57/57 PASS**(`d5236a8`).
- ⚠ 조립 경고(설계상 사용자 확인 사항): 변수 공유 — 특히 도매·의료가 `context.phoneValid` 공유. 실사용(런타임 로드) 확인은 잔여.
- 🧠 로드맵 잔여: 항목 4 잔여(산업군당 다중 후보 스코어 — 레퍼런스 추가 제작 선행), 항목 6 백로그(미리보기 모달·placeholder-leak 원인·도매 배열 품질). 항목 5는 하네스가 LLM·API·ESD × few-shot 병행 PASS로 대부분 커버.

### 2026-07-09 — v0.2.2 프로덕션 릴리스: 프로젝트명 전면 변경 CogInsight Generator (📄 git·라이브 검증)
- **배경 (📄 사용자 확정)**: 구명이 **사용하면 안 되는 이름**으로 판정 → "모든 곳의 모든 흔적"을 새 이름 **CogInsight Generator**로 변경. 라이브 인프라까지 전부 + raw/ 포함(예외 승인), git 커밋 이력은 유지(재작성 안 함 — 커밋 메시지·과거 파일 내용에 구명 잔존은 의도된 예외).
- **코드 (PR #101 → main `9a99e18`, tag v0.2.2 + GitHub Release)**: 122파일 치환 + 함수 디렉토리·마이그레이션 파일명 rename(버전 프리픽스 불변). 과거 마이그레이션 파일도 새 이름 기준 재작성. deno 210 green(main). **v0.3.0 dev 브랜치에도 동일 적용**(134파일 + main 머지 정합, deno 228 green, push 완료).
- **DB (라이브 직접 실행, Management API)**: 테이블 8(`coginsight_references`·`coginsight_results`·`coginsight_scenario_references`·`coginsight_api_references`·`coginsight_feedback` + dev 사본 3)·제약 12·인덱스 20·정책 8 rename. ⚠ **rename 마이그레이션 파일은 의도적으로 미작성**(파일에 구명이 남는 것 방지) — fresh reset은 재작성된 과거 마이그레이션이 새 이름으로 생성. 데이터 무손실 검증(references 4·results 75·dev 레퍼런스 6).
- **엣지함수**: 전 함수(25종) 재배포, 슬러그 `coginsight-generator`·`coginsight-generator-dev` 신규·구 슬러그 삭제(404 확인). dev 래퍼 7종은 v0.3.0 브랜치 코드로 재배포. 스모크: references·scenario-references·questions 전부 200.
- **GitHub·로컬**: repo `qtw9723/CogInsight-Generator`(구명 redirect 유지), 로컬 폴더 `/Users/sangjun/IdeaProjects/CogInsight-Generator`.
- **Vercel**: 앱 프로젝트 rename → **https://coginsight-generator.vercel.app** (200, 번들 신규 슬러그 호출 확인), 구 도메인 삭제(404). 개요 페이지 신규 프로젝트 → **https://coginsight-overview.vercel.app** (200), 구 프로젝트 삭제(404). 공개 브랜딩 "CogInsight Generator"로 통일(POC 표기 제거). claude.ai 아티팩트(1e30660a) in-place 동기화(label `rename-coginsight`).
- ⚠ **구 URL 폐기에 따른 후속(사용자 몫)**: 테스터·사내 공유했던 앱/개요 링크 재안내 필요.
- 🧠 잔존(의도): git 이력(양 저장소 커밋 메시지·과거 커밋 파일 내용), node_modules 내 base64 소스맵의 우연한 문자열(이름 아님).

### 2026-07-08 — v0.2.1 프로덕션 핫픽스: ESD 스키마 파생 버그 (📄 git·프로덕션 재생성 검증)
- **발견 (📄 발표 준비 중)**: 데모 봇(올인원 물류봇)에서 ESD 연동 시나리오는 플로우에 있으나 **ESD 매니저용 JSON(`esd_schemas`)이 항상 빈 배열** — "ESD 연결" 산출물이 비어 시연 불가.
- **원인**: `collectEsdFields`가 schemaName을 `config.schemaName`에서 읽는데 **실생성 노드는 `config.query.schemaName`** → ESD 노드 스킵. 테스트 픽스처가 실구조와 달라(config.schemaName) 못 잡던 결함(프로덕션 v0.1.0부터 잠재).
- **수정·릴리스 (사용자 승인)**: `config.query.schemaName` 우선(폴백 유지) + 바인딩된 필드만 수집(레퍼런스 잔재 빈필드 제외) + 픽스처 실구조 교정·회귀테스트. deno **223 green**. hotfix 브랜치→**PR #100 머지(main `46bb57f`)→tag `v0.2.1`+GitHub Release→`supabase functions deploy coginsight-generator`(프로덕션)**. 프론트는 main push로 Vercel 자동 v0.2.1.
- **검증**: 프로덕션 재생성 id **e72f4e26** — `esd_schemas` 정상 1개("상담기록"/`inquiry`, 잔재필드 제거), `api_defs` 정상. 공개 coginsight-overview·아티팩트 v0.2.1 반영, 데모 백업·시연대본(`docs/demo/`) 갱신.
- 🧠 fix는 main(v0.2.1)+v0.3.0 브랜치 양쪽 존재 → v0.3.0 머지 시 동일 변경 충돌 가능(정리 필요).

### 2026-07-08 — 생성 파이프라인 스테이지 라벨 함수명化 + 이력 매핑표 (📄 git·deno 검증)
- **배경 (📄 사용자)**: 누적 삽입으로 뜀번호가 된 실제 코드 스테이지 번호(2.9·2.95·3.65·3.68·3.7·3.75 등)도 정리하되, 이력 추적 위해 기존 번호 매핑 유지(A안).
- **작업**: coginsight-generator 로그·주석·테스트명의 스테이지 라벨을 **함수명 기반**(designFlow·fillNodeValues·normalizeAnythingElse·applyLlmBlocks·guardApiResults 등)으로 일괄 치환(17파일). `index.ts` 상단에 **이름↔레거시 STAGE 번호 매핑표**(구 STAGE 1~3.75) 추가 = 이력 추적 단일 출처. `STAGE1_EXCLUDED_TYPES` 식별자는 보호.
- **무영향·검증**: 런타임 로직·DB·테스트 단언에 번호 미사용 → 기능 무변경, deno **221 green**. **v0.3.0 dev 브랜치(`feat/v0.3.0-observability-regression`)에 ff-머지·push(`7cf1d75`)** (사용자 "빠르게 반영" 지시). **main·프로덕션은 미반영**(정책상 승인 시) — 단 **CHANGELOG [0.3.0]에 기재(`134b9ca`)**하여 **다음 v0.3.0 프로덕션 릴리스 때 함께 반영**되도록 스코프에 포함(사용자 지시).
- 🧠 번호 3종 관계: **코드=함수명(+매핑표)** / **공개 doc=표시용 순차번호(1·2.1~3.8)** / 위키 §주요기능·§생성 파이프라인 서술은 레거시 STAGE 번호 잔존 → 셋 다 **함수명이 공통 앵커**(위키 서술 번호는 필요 시 점진 정리).

### 2026-07-08 — 발표용 공개 개요 페이지 v0.3.0 진행분 반영 (📄 vercel 재배포·라이브 검증)
- **배경 (📄 사용자)**: 오늘 발표(공개 문서). 현 개발분(v0.3.0 dev)까지 정리해 공개 페이지에 반영 — 청중=사내 실무/보고용.
- **갱신 (coginsight-overview.vercel.app)**: 히어로 배지 "프로덕션 v0.2.0 · v0.3.0 개발 중", 통계(713커밋·엣지함수 29(프로덕션 21)·마이그레이션 64), "진행 현황 & 한계"에 **v0.3.0 진행 섹션 신설**(레퍼런스 6종 등록 ✅·few-shot 실검증 ✅·구조 시드·선택 UX·피드백 스크린샷·생성 관측성/회귀 하네스) + 남은 항목 재정리, 버전 히스토리 v0.3.0 행 (계획→개발 중)·잔여 명시, 작성기준 2026-07-08.
- **검증**: `vercel deploy --prod`(프로젝트 coginsight-overview, 계정 qtw9723) → 짧은 URL 200 + 라이브 마커 6종 grep 확인. claude.ai 아티팩트(1e30660a) 동일 URL in-place 동기화 완료(label `v0.3.0-dev-progress`). **내부 백로그(LLM flag 루프 무한반복 위험 등)는 공개 페이지 비게재 원칙 유지**.

### 2026-07-07 (저녁) — 피드백 스크린샷 첨부 (v0.3.0 추가 기능, dev 전용) (📄 git log·dev API 검증)
- **기능 (📄 사용자 제안)**: 피드백 팝오버에 "지금 보는 화면 첨부" 체크박스 — 체크 **시점**에 뷰포트를 DOM 렌더 캡처(`html-to-image`, 피드백 UI는 `data-feedback-ui` 마커로 제외, Tailwind 4 oklch 호환) → **미리보기+다시 찍기** → 전송 시 JPEG data URL로 저장. 어드민 피드백 탭에 썸네일+클릭 확대. **best-effort**(캡처 실패·과대(1.5MB 가드→0.6 축소 재시도)가 텍스트 전송을 막지 않음). DOM 캡처 한계(펼친 드롭다운·픽셀 버그 미재현)는 사용자가 인지·수용.
- **백엔드**: `dev_coginsight_feedback` 사본(+screenshot 컬럼, 프로덕션 8건 미러) + `feedback` 함수 T() 경유 + `feedback-dev` 슬러그(dev 테이블 5개·래퍼 7개로 — CLAUDE.md 규약 갱신). **프로덕션용 마이그레이션 파일 작성만**(20260707120000, 머지 때 적용 — "dev 반영+마이그레이션 짝" 규약).
- **검증**: 뷰포트 크롭 순수 함수 deno 테스트 3종 + dev API 4종 통과(스크린샷 201 저장 / GET 포함 / png 접두는 스크린샷만 무시·텍스트 저장 / **프로덕션 격리 0건**). 화면 실검증(체크→미리보기→전송→어드민 썸네일)은 사용자 로컬(`VITE_DEV_TABLES=true`) 몫.
- ✅ **(해소 2026-07-08, 사용자 결정) 별건 2건 처리**: ① `node_modules` 6,780파일 추적 해제 — 사용자 선택대로 **v0.3.0 브랜치에서** `git rm -r --cached` 정리 커밋(`209995d`, push 완료. ⚠ v0.3.0 프로덕션 머지 PR diff에 -6,780파일 포함됨 — 의도된 선택). ② `AGENTS.md`는 `.gitignore`에 등록(로컬 유지·git 무시, 같은 커밋).

### 2026-07-07 (오후) — 시드 UX 반복 개선 5건 (📄 사용자 실사용 피드백 → 즉시 반영)
- **버전 배지 0.3.0 선반영**: package.json 0.3.0 + CHANGELOG [0.3.0] 미릴리스 섹션(v0.2.0 dev 사이클 전례) — 로컬 배지 `v0.3.0 DEV`.
- **드롭다운 미노출 버그 수정**: 주입 지점이 실제 렌더 경로가 아니었음(시나리오 카드는 `ScenarioQuestionCard`가 직접 렌더 — GROUP_LIST 분기는 도달 불가 레이어). 🧠 빌드만 확인하고 렌더를 안 본 검증 공백.
- **산업군 그룹화**: 설문에서 고른 산업군 레퍼런스를 상단 optgroup으로(스펙 §1 M-c 해소), 교차 선택 가능 유지.
- **무시 필드 비활성화**: 레퍼런스 선택 시 반영 안 되는 필드(수집 정보·완료 결과·외부 연동)를 흐림+클릭 차단 + 안내 배너, 검증도 skip. 활성 유지 4종 = `SEED_ACTIVE_FIELDS`(시나리오 이름·진입 발화·AI 자유응답 2종) — 생성기 v1 경계와 짝.
- **흐름 요약 카드**: 레퍼런스 선택 시 flow_json에서 자동 파생한 요약(흐름 스텝·수집·첫 멘트·분기 수) 표시(`src/lib/refSummary.js`). 📄 **v0.4.0 계획(사용자)**: 이 요약을 **다이어그램 시각화**로 발전 — ROADMAP 기록, 파생 로직 재사용 전제.

### 2026-07-07 — 레퍼런스 구조 시드 생성 (사용자 제안 기능, dev 전용) (📄 git log·dev 실검증)
- **기능 (📄 사용자 제안·의미론 확정)**: 설문에서 시나리오 추가 시 **레퍼런스를 직접 선택** → 그 플로우가 **구조 시드**로 생성됨(few-shot 참고가 아니라 결정론 복제 — 구조·멘트는 교정된 레퍼런스 그대로, 진입 발화만 설문 값). 신규 **STAGE 3.68**(`applyScenarioSeeds.ts`, 3.7 llmloop 부착과 호환), 프론트 드롭다운은 **공유 templates 무접촉**(코드 주입 — 응답 JSON에만 실림), `scenario_examples.seeded` 관측성, 하네스 실측 어서션(`checkSeededStructure`)+`seed-collect` fixture.
- **최종 리뷰가 잡은 결함 3건 (수정 완료)**: ⚠ 3중 검증(단위·하네스·실검증)이 **같은 사각지대**(설문 발화=레퍼런스 트리거로만 테스트)를 공유해 전부 통과했던 것을 최종 브랜치 리뷰가 발견 — ① C1: 이중 트리거 게이트로 설문 발화가 다르면 시드 시나리오 도달 불가 ② I1: "AI 자유응답=예"+수집형 조합에서 3.7이 시드 서브트리를 파괴 ③ I2: seeded 어서션이 메타 재확인(동어반복). 전부 수정 + **다른 진입 발화("내 택배 어디야") 실검증 PASS**. 🧠 교훈: 검증 레이어를 늘려도 같은 가정을 공유하면 무의미 — 대표 사용 케이스(불일치 입력)를 fixture에 박아둠.
- v1 경계(📄 확정): 레퍼런스 수집 구조 우선(설문 수집항목 불일치는 `mismatch` 경고만), 시드 시나리오는 few-shot 후보에서도 제외(이중 주입 방지). 유닛 221+어서션 20 테스트, 4-fixture 회귀 전체 PASS, `coginsight-generator-dev` 재배포. 총 25커밋(브랜치), main 미머지.
- 🧠 사용자 로컬 확인 방법: `VITE_DEV_TABLES=true`로 로컬 프론트 실행 → 설문 시나리오 항목의 "레퍼런스 선택" 드롭다운 → 생성 → 결과 확인.

### 2026-07-06 (밤) — 레퍼런스 6종 제작·등록 + few-shot 첫 실검증 (로드맵 항목 1·2 ✅) (📄 dev 실행·git log)
- **제작**: 산업군별 미니봇 6종을 "생성기 초안(6회 생성) → 수동 교정 → 품질 게이트(`scripts/scenario-refs/gate.ts` = checkBot+scenarioPortion) → `scenario-references-dev` 등록". 게이트 6/6 PASS, dev 6건·**프로덕션 0건 유지**. 도구로 러너 `--save-json`·게이트 CLI 추가(커밋), 미니봇 JSON은 미커밋(dev 테이블이 소스, 승격 시 데이터 마이그레이션).
- **few-shot 전/후 비교 (항목 2)**: 기준선(전) vs `runs/2026-07-06-after-refs.json`(후) — 3개 fixture 전부 `injected` false→true, **산업군별 올바른 레퍼런스 선택 확인**(금융→계좌 잔액 조회봇/소매→반품 접수봇/물류→배송 조회봇 — 항목 4 부분 완료), **`rules_hash` 완전 동일**(규칙 무변경 상태에서 순수 레퍼런스 효과만 분리 — 관측성 스냅샷 설계 의도 그대로 실증).
- ⚠ **발견 2건 (하네스 실전 성과)**: ① 도매 초안에서 **백로그 1번 "LLM flag 루프 탈출 set 누락"이 실재현** — `loop-exit-set` 어서션이 자동 검출("육안 확인"의 자동화가 실제로 작동), 교정에서 종료 발화 분기+탈출 set 추가로 해소. ② few-shot 도입 후 api-esd 생성에 `placeholder-leak` 신규 FAIL — **few-shot 주입이 다른 출력 품질에 영향을 주는 Instruction Bleed형 부작용**을 하네스가 포착. 로드맵 항목 6(고도화) 백로그로 이동.
- 🧠 남은 결: 항목 3(조립 생성 테스트), 항목 4 잔여(산업군당 다중 레퍼런스 시 관련도 스코어), 항목 5(v0.2.0 결합 회귀), 항목 6(placeholder-leak 원인·도매 배열 누적·레퍼런스 품질 가이드).

### 2026-07-06 (저녁) — 시나리오 레퍼런스 dev 사본 체계 구축 (📄 git log·dev 스모크 검증)
- **배경 (📄 사용자 확정)**: 로드맵 항목 1(레퍼런스 등록)을 프로덕션 공유 테이블이 아닌 **dev 사본에서 테스트 후 승격(데이터 마이그레이션)**하는 방식으로.
- **구축 내용**: ① `dev_coginsight_scenario_references` 테이블(프로덕션 미러, `LIKE … INCLUDING ALL` — 기존 dev 테이블처럼 repo 마이그레이션 없이 DB 직접 생성) ② generator Mode A·scenario-references 함수 5곳을 `T()` 경유로(dev 슬러그만 dev 테이블, 프로덕션 무변경) ③ `scenario-references-dev` 래퍼 + 프론트 `SCENARIO_REFERENCES` devable 전환 ④ 회귀 러너 `--only <fixture>` 필터 ⑤ 저장소 CLAUDE.md DEV 규약 갱신(dev 테이블 4개·래퍼 6개·**승격 절차**: 사용자 선별 확인 → INSERT…SELECT(id 유지) → 재조회 검증 → 머지 후 미러 리셋).
- **dev 스모크 전수 통과**: 등록(의료 카테고리)→dev 목록 1건·**프로덕션 0건(격리 ①)**→조립 정상→few-shot 생성 `injected=true`·`picked=[스모크-진료예약봇]`(관측성 스냅샷으로 확인 — 오전 구축분과 맞물림)→정리 후 dev 0건·**프로덕션 0건 재확인(격리 ②)**. 프론트 빌드 그린. 기존 fixture 기대값 오염 방지를 위해 스모크는 의료 카테고리 사용(fixture는 금융).
- ⚠ **운영 메모**: DB 직접 SQL(DDL·승격·리셋)은 Management API + `mailer/.env`의 `SUPABASE_ACCESS_TOKEN` 방식(과거 세션 방식 재발견) — 자동 모드 분류기가 타 프로젝트 env를 차단하므로 사용자 `!` 실행 또는 CogInsight `.env.local`에 토큰 복사 필요.
- 🧠 다음 단계: 로드맵 항목 1 — 산업군별 미니봇 레퍼런스 제작·dev 등록 → 항목 2 — collect-loop fixture `injected: true` 갱신 후 기준선("전") 대비 "후" 실행 비교.

### 2026-07-06 (오후) — 생성 관측성 + 프롬프트 회귀 하네스 구현 (Instruction Bleed 대응, dev 전용) (📄 git log·dev 실행 검증)
- **배경**: [[AI-주간-소식-2026-W26]]의 Instruction Bleed(프롬프트 모듈 교차 간섭) 논의에서 출발 — 📄 코드 확인으로 CogInsight의 실제 bleed 벡터 확인(`Variable Usage Rule`이 flow·config·output·condition 4단계 동시 주입 / 규칙 학습이 규칙 교체 / v0.3.0 few-shot 주입이 Stage 1의 새 벡터). W26의 처방("단계별 회귀 테스트")을 실구현한 것.
- **Part C — 생성 관측성** (`flow/observability.ts` + index.ts): 모든 생성 결과 `generation_tiers`에 ① `scenario_examples`(산업군·후보 수·선택 레퍼런스·주입 여부·skip 사유 — few-shot "조용한 skip" 제거, 로드맵 항목 2·4의 전제) ② `rules_snapshot`(규칙 세트 SHA-256 지문 — `ruleText` 기반이라 content-폴백 규칙 수정도 포착 + **스테이지별 해시**로 다단계 규칙의 blast radius 노출 + examples 해시·모델) 기록. DDL 없음(jsonb 관례), 실패해도 생성 무해(try/catch).
- **Part A-lite — 프롬프트 회귀 하네스** (`scripts/prompt-regression/`): fixture 3종(수집형+전화번호 검증루프 / LLM Q&A docs+폴백 / API+ESD) → `coginsight-generator-dev` 실호출 → **속성 어서션**(exact-match 금지: welcome 루트·anythingelse 1회성·단일부모 트리·도달성·llmloop apiKey/model 빈 값·tool→body 골격·**flag 루프 탈출 set 존재**·placeholder leak). 질문은 **text로 매칭**(dev 리셋 시 id 재발급 대응). exit 규약: 실패 1 / 환경 미비 2. 🧠 백로그 1번 "flag 루프 탈출 set 육안 확인"이 이 어서션으로 자동화됨.
- **기준선 확보**: 레퍼런스 등록 前 3 fixture **전부 PASS**(`runs/2026-07-06-baseline.json`, injected=false) — 로드맵 항목 2 "주입 전/후 비교"의 '전' 데이터 완료. 하네스 자체 검증(기대값 변조→FAIL 검출) 통과.
- **규모·상태**: 브랜치 `feat/v0.3.0-observability-regression` 13커밋(스펙·계획 문서 포함), **origin 푸시 완료·main 미머지**(dev 전용 규약 — v0.2.0 때 `feat/llm-v0.2.0-testing` 패턴과 동일). deno 테스트 211+14 전부 통과, `coginsight-generator-dev` 재배포됨. 서브에이전트 구동 개발(태스크 6개, 태스크별 리뷰 + 최종 브랜치 리뷰 **Ready**).
- ⚠ **발견 2건**: ① `.env.local`의 `VITE_SUPABASE_SERVICE_ROLE_KEY` **무효(401)** — dev_questions는 anon 키로 읽혀 우회했으나, 서비스 키가 진짜 필요한 작업 전에 재발급 필요. ② 기존 코드-스키마 불일치: `deriveApiDefs.ts`가 참조하는 'API 이름'·'받을 정보' 필드가 현 시나리오 템플릿에 없음(이번 범위 밖, 백로그).

### 2026-07-06 — v0.3.0 로드맵 수립(시나리오 라이브러리) + ROADMAP.md 신설·문서 전체 배포 (📄 사용자 지시)
- **v0.3.0(계획) = 시나리오 레퍼런스 라이브러리 테스트·고도화**로 확정(사용자). 레퍼런스 0건·조립 미테스트 상태 → 라이브러리를 활용한 결과 생성 테스트가 목표. 상세는 위 [[#로드맵 — v0.3.0 (계획): 시나리오 레퍼런스 라이브러리 테스트·고도화|로드맵 섹션]].
- 📄 **사용자 확정(같은 날 정정)**: v0.3.0 작업 자체는 **프로덕션 무배포·dev 전용**. 배포 대상은 로드맵 "문서"뿐 — ROADMAP.md에 명문화(`3082ca9`).
- 저장소에 **ROADMAP.md 신설 + CLAUDE.md 포인터** — **PR #99 머지 완료**(사용자 승인, main `36d0181`→`14cca10`, 문서 2파일 +35줄·코드/버전 무변경). 기존 v0.3 후보는 백로그(버전 미정)로 이동.
- 공개 개요 페이지: 버전 히스토리에 "v0.3.0 (계획)" 행 추가 → **`vercel --prod` 재배포 완료**(200 확인, v0.3.0 행 라이브 노출) + **claude.ai 아티팩트 원본 동기화 완료**(`1e30660a…`, label `v0.3.0-roadmap-row`).

### 2026-07-03 (오후) — v0.2.0 확장(지식소스·시나리오 LLM) 후 ⏸ 홀드 (📄 git log·dev API 실검증)
- **생성 결함 3건 수정**(`04ff579`): anythingelse 1회성(STAGE 3.65 신설+카탈로그 제외) · 제작 챗봇 정보 prompt 주입(시나리오 상세) · llmloop 레퍼런스 풀 body(ask_docs/no_answer+docsearch 2패스).
- **지식소스 3종 + 시나리오별 LLM**(`ca13dc4`): 문서 검색/일반 LLM/혼합을 전역·시나리오별로 설문 선택, "사용=예" 시나리오 끝에 주제 전담 Q&A llmloop(하이브리드: Stage 1 규칙+3.7 결정론 보장). 설계 spec 커밋, 공유 templates에 필드 2개 라이브 반영(사용자 승인).
- **model 빈 값 불변식**(`3ca4282`): apiKey·model·storeId 전부 사용자 입력(키 종속).
- **검증**: deno 183 tests + dev 생성기 API 실호출(최종 샘플 `09bde7a9` — 시나리오 docs 골격/폴백 general/빈 키·모델 모두 확인).
- **⏸ 홀드**: 이 지점(`3ca4282`, 650커밋·마이그레이션 62)에서 v0.2.0 개발 동결(사용자 지시). 프로덕션 머지는 별도 승인 대기 — llm 마이그레이션 5개 미적용 주의.

### 2026-07-03 — v0.2.0 구현→main 롤백→dev 테스트 체제 + 보안 정리 (📄 git log·DB 직접 조회)
- **v0.2.0 하루 만에 구현→릴리스→롤백 (7/2)**: 설계 문서(`d6e57d5`) 당일에 applyLlmBlocks(STAGE 3.7)·DB 질문/규칙까지 구현해 PR #94(기능)·#95(model 대소문자 픽스)·#96(릴리스)로 main 머지 → **같은 날 PR #97로 전량 revert**. 프로덕션 v0.1.0 유지, v0.2.0은 "미릴리스(dev 테스트 중)"로 CHANGELOG 정정.
- **DEV 테이블 모드 도입 (`ac9ea93`)**: 같은 Supabase 안에 `dev_questions`/`dev_solution_rules`/`dev_coginsight_results` + `-dev` 슬러그 함수 5개 + 프론트 `VITE_DEV_TABLES=true`. 프로덕션 무접촉 "실행-후-머지" 워크플로우 확립.
- **dev 튜닝 3건 (7/2 오후)**: 폴백 anythingelse 선택 픽스(`00715c1`) · prompt 백틱 정규화(`e1588cd`) · 프롬프트 샘플 섹션 구조 — 챗봇 정보 나열+비답습 지침(`dde7e15`, dev 규칙에도 반영 확인).
- **DEV 워크플로우 규약 명문화 (7/3, `5c4bb3d`)**: 저장소 CLAUDE.md에 "모든 작업은 dev / 프로덕션 머지 시 4축(코드·DB·엣지함수·프론트) 전체 마이그레이션+push 후 재검증 / 머지 후 dev_ 테이블을 프로덕션 미러로 리셋" 규약 추가(사용자 지시). 이 기기 Claude 메모리에도 동일 규약 저장.
- **보안 정리 — 레퍼런스 JSON apiKey 전수 마스킹 (7/3, DB 직접)**: JSON 보유 7개 테이블 전수 스캔 → 비어있지 않은 apiKey **8건**(한화라이프 LLM 봇 5 · 노드 샘플 2 · 옛 생성 결과 1)을 전부 `""`로 마스킹, 재스캔 0건 확인. 설계 문서의 "평문 키 제거 권장" 항목 해소.
- **구조 수치**: 마이그레이션 54→60, 엣지함수 21→26(dev 슬러그 +5), 커밋 610→646(테스트 브랜치).
- 🧠 의미: 6/30 "생성 결과의 결정론 강제"에 이어, 7/2~3은 **작업 환경 자체의 결정론화**(dev 격리·머지 절차·리셋 규약) — 프로덕션 안정성을 프로세스 수준으로 끌어올린 구간.

### 2026-07-02 — v0.2.0 설계 착수(문서만) + 낡은 초안 폐기 (📄 git log)
- 🚧 **AI 자유응답(LLM 노드) 블록 v0.2.0 설계 착수** (`d6e57d5`, 브랜치 `feat/llm-response-block`): 설계 문서 1개만 추가(`docs/superpowers/specs/2026-07-02-llm-response-block-design.md`, +131줄). **코드 0줄·main 미머지·버전 v0.1.0 그대로.** 상세는 위 [[#🚧 v0.2.0 설계 착수 — AI 자유응답(LLM 노드) 블록 (⚠ 설계 문서만, 미구현·미머지)|v0.2.0 설계 블록]].
- 📄 **낡은 개요·매뉴얼 초안 `.md` 폐기** (PR #93, 2026-07-01 머지): `docs/프로젝트-개요-및-매뉴얼-초안.md` 삭제(−168줄). 초안의 잘못된 버전("1.0.1")·구식 커밋수가 실제 v0.1.0 상태와 혼동될 위험 → SoT를 공개 페이지(coginsight-overview.vercel.app)+claude.ai 아티팩트로 일원화.
- 🧠 이 기간 main 반영 실코드 변경은 **없음**(문서 정리 + 미머지 설계뿐). 버전·기능 기준선은 v0.1.0 유지.

### 2026-06-30 — v0.1.0 프로토타입 동결 + 결정론적 생성 안전장치 (📄 git log, PR #76~#85)
- **v0.1.0 프로토타입 동결 (PR #84, 가장 큰 신규)**: 버전 관리 시작 — `package.json` 0.1.0 + annotated tag `v0.1.0` + GitHub Release. 보고·테스트용 기준선(엣지함수 coginsight-generator **v87** 배포 기준). ⚠ 동결 버전은 변경 금지, 테스트는 태그 기준.
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
- **🆕 (2026-07-31) 비용 개선의 순서가 뒤바뀌어 있었다** — [[AI-주간-소식-2026-W31]] 영문 1차 소스 기준:
  - 📄 OpenAI: **API 설정 두 개(추론 상태 유지 `reasoning` + 컨텍스트 압축 `compaction`)만 켜서 ARC-AGI-3 점수 3배**. 🧠 6단계 파이프라인은 단계마다 호출을 새로 열어 추론 상태를 버리고 누적 컨텍스트를 통째로 넘긴다 → **코드 변경량 대비 효과가 가장 큰 후보**.
  - ⚠ 📄 arXiv **TRACE-ROUTER**: 기존 라우터는 **LLM 호출마다 독립적으로** 모델을 고르는데 에이전틱 앱에선 그게 문제(task-consistency). 🧠 "설계=고급 / 변환·포맷팅=저가" 단계별 티어링은 **단계 간 해석 불일치 위험**이 있으므로, 단계별 독립 결정이 아니라 **한 생성 작업 전체 단위로 프로필을 고정**하는 편이 안전.
  - 🧠 **결론(개선 순서)**: ① 설정(reasoning·compaction) → ② 작업 단위 프로필 티어링 → ③ 모델 교체. 지금까지 검토해온 건 ③뿐이었다. ⚠ 전제: `flow/usage.ts` 단가표가 gpt-4o 기준이라 **비용 비교 기준선부터 갱신 필요**(기존 TODO).
- **🆕 (2026-07-31) "규칙을 실행 가능하게 만든다"에 학술 이름표가 붙었다**: 📄 arXiv **ARCHER: Agentic Rule and Compliance Harness for *Executable Regulations*** — 수천 개 규칙을 대형 구조화 산출물(BIM)에 대조하는 노동을 에이전트에게 넘기는 프레임워크. 🧠 이 프로젝트의 `solution_rules` **DB-구동 규칙엔진**이 방향만 반대인 같은 구조(규칙에 맞는 산출물을 *생성*)다. 📄 국내 보도의 「오라클: 에이전트의 DB 활용이 새 경쟁 기준」·「AIDP(출처 제시)」와 같은 결론.
- **⚠ 🆕 (2026-07-31) 폐쇄망 납품 서사에 반대 증거가 생겼다**: 📄 arXiv **Where Facts Go Missing**(L0–L8 9계층 분류) — 에어갭·온프렘은 프런티어 API를 못 써서 **4–8B 양자화 모델**을 쓰는데, 소스 수집~최종 생성 사이 **어느 경계에서든 결정적 사실이 조용히 누락**된다. 🧠 「소버린 AI = 폐쇄망 특화 SLM + RAG가 현실적」(와이즈넛)이라는 세일즈 논리와 정면으로 부딪히므로 **둘 다 든 채로** 말해야 한다: *선택지는 그것뿐이지만 누락 계측이 필수*. L0–L8은 그때 쓸 체크리스트 후보.
- ⭐ 🚨 **🆕 (2026-08-06) QA 게이트 설계 규칙이 확정됐다 — "오류 비용이 높으면 금지"가 아니라 "높을수록 LLM을 판정에서 생성으로 좁힌다"** ([[AI-주간-소식-2026-W32]] 9차 보강, 연결점 ㉕):
  - 📄 **K방산 — LLM 기반 AI 임무계획 생성 플랫폼**이 기뢰 탐색 무인수상정 대기뢰전 시연에 성공했다. 🧠 군사는 오류 비용이 의료·금융보다 **높은데도 배치됐고**, 차이는 도메인이 아니라 **LLM에게 맡긴 역할**이다 — LLM은 *계획을 생성*했고, 판정과 실행은 결정론적 시스템이 했다.
  - ✅ 🧠 **적용 규칙**: 6단계 파이프라인의 **각 단계마다 "이 단계의 LLM은 생성자인가 판정자인가"를 먼저 명시**하고, 판정자 역할이 남아 있으면 그 자리에 결정론 게이트(zod/closed-world 검증·실행 결과 대조)를 넣는다. 이 프로젝트는 이미 *"LLM이 설계하고 zod가 구조를 강제"* 하는 구조라 방향은 맞지만, **단계별로 그 구분이 문서화돼 있지 않다**(현재는 암묵적).
  - 🧠 이건 이 위키가 여러 경로로 도달한 결론(中 DGNN+LLM 90% · MARGIN "자기보고 신뢰도는 모델 간 비교 불가" · [[올림푸스-Olympus]] `verify.sh`)의 **가장 일반적인 형태**다.
- ⭐ **🆕 (2026-08-06) 안전 게이트를 자작하지 않아도 되는 첫 부품이 나왔다** (연결점 ㉖): 📄 미스트랄이 멀티모달 안전 분류 모델 **실드스트랄(Shieldstral)을 Apache 2.0으로 공개**했고, 같은 날 📄 **엔비디아 주도 SAFE 가이드라인**이 *"AI 에이전트 행동 추적"* 을 명시했다. 🧠 W32 3차·6차 논문 3편이 요구한 **궤적 단위 검사**가 3일 만에 업계 표준 문서로 올라왔고, 그 중 *안전 분류* 층은 오픈 가중치로 존재한다 → 자작 대상 목록에서 뺄 수 있는 첫 항목(연결점 ⑥ "하네스가 자작 자산에서 남의 인프라로"의 안전 계층 버전). ⚠ 단 라이선스 계보 확인은 여전히 필요(연결점 ㉓ — 같은 날 키미 K3 무단 증류 분쟁).
- ⭐ 🚨 **🆕 (2026-08-07) QA 게이트의 "다음 단계" 형태가 나왔다 — 통과/실패 게이트에서 홀드아웃 채점 루프로** ([[AI-주간-소식-2026-W32]] 11차 보강, 연결점 ㊲):
  - 📄 arXiv **Continuous Improvement and Parallel Autonomous Exploration**([2608.04341](https://arxiv.org/abs/2608.04341)) — *홀드아웃 데이터로 채점되는 **리더보드가 보상 신호**로 작동해 각 에이전트가 **반복 제출로 자기 해답을 정련**하게 만든다.*
  - ✅ 🧠 **적용안**: 시나리오 QA를 *"zod/closed-world 검증 통과"*(이진 게이트)에서 한 단계 올려, **생성에 쓰지 않은 실제 사용자 발화 세트(홀드아웃)** 로 생성된 시나리오를 채점하고 그 점수로 후보를 고른다. 🧠 채점을 파이프라인 **안**이 아니라 **후보 선택 단계**에 두면 6단계 지연(연결점 ⑲)에 더해지지 않는다.
  - 🧠 **채점 루브릭의 출처도 같이 나왔다**: 📄 **MIDAS**([2608.04307](https://arxiv.org/abs/2608.04307))는 *지원 티켓·법률 문서·인시던트 리포트 같은 엔터프라이즈 요약은 **도메인 특화 지침의 엄격한 준수**를 요구한다*고 말한다. 🧠 즉 *[[mailer|CS SmartHub]]가 쌓은 판단 기록(연결점 ㉗ '판단 데이터') → 성문화된 지침 → 채점 루브릭*이 한 줄로 이어진다.
  - ⚠ 🧠 **금지선도 같이 그어졌다** (연결점 ㉚): 8/6 arXiv 4편(📄 Pluralistic Ignorance · Biased Consensus · Misinformation Derails Collective Fact Recovery · Group Perspective Matters)이 *"LLM 여러 개에 물어 다수결"* 을 막았다 — 📄 **상호작용이 단일 LLM의 편향을 증폭**하고 **합의가 동조의 결과**일 수 있다. **여러 모델로 후보를 생성하는 것은 되고, 여러 모델에게 판정을 맡기는 것은 안 된다.**
- 🚨 ⭐ **🆕 (2026-08-07) 이 프로젝트에 "한국어 특정 리스크"가 처음 확인됐다** (연결점 ㉛): 📄 arXiv **An Actionable Diagnosis of Multilingual, Multi-Agent Planning Failures**([2608.03735](https://arxiv.org/abs/2608.03735)) — *다국어 멀티에이전트 시스템은 **영어를 벗어나면 상당한 저하**를 보이지만, 선행 연구는 **사용자 요청이 실행 가능한 계획으로 변환될 때 과제에 결정적인 정보가 어떻게 손실되는지**를 좀처럼 특정하지 않는다.*
  - 🚨 🧠 손실 구간(*요청 → 실행 가능한 계획*)이 이 파이프라인의 **1~2단계(한국어 문서 → ESD/구조화 산출물)** 와 정확히 겹친다. 🧠 그리고 이 위키가 세운 검증 결론들(궤적 단위 검사 ⑯ · 신뢰도 비교 불가 ⑦ · 생성/판정 분리 ㉕)은 **전부 언어를 변수로 두지 않았다.**
  - ✅ 🧠 **적용안(기존 작업의 재해석)**: 궤적 기록에 **"어느 원문 한국어 구절이 어느 산출 필드가 됐는지"** 를 넣으면 궤적 검증(⑯)과 다국어 손실 방어를 **한 번에** 만족한다. 이 프로젝트는 API 호출 기반이라 OS 레벨 흔적이 없으므로(11차 보강 ㊳ 참고) **이 대조 기록이 궤적의 실체**가 된다.
  - ⚠ 🧠 과잉 해석 금지: 📄 언어별 손실 규모는 원문 절단으로 확인 불가. *"한국어면 나쁘다"* 가 아니라 **"아직 측정해본 적 없는 축이 있다"** 까지만.
- **🆕 (2026-08-07) 6단계 직렬 구조가 두 방향에서 지적됐다 — 답은 "수"가 아니라 "위상"** (연결점 ㊱): 📄 **HELENA**([2608.04634](https://arxiv.org/abs/2608.04634))는 *MAS가 보통 **단일 위상(topology)을 최적화**하는데 이는 추론을 **좁은 궤적에 가두고**, 여러 위상을 단순 병합하면 **중복 노이즈**가 생긴다*고 한다. 📄 **Group Perspective Matters**는 같은 처방을 *동조 완화* 쪽에서 낸다. 🧠 6차 보강 ⑲(깊이 = 지연 선형 비례)와 합치면 **직렬 6단계는 느리면서 좁다**. ⚠ 단 *"병렬 다수결로 바꿔라"* 는 위 ㉚에 걸린다 — 남는 방향은 **역할이 다른 소수 경로 + 결정론적 채점**(㊲).
- ⭐ **🆕 (2026-08-07) 의외의 독법 — "같은 문서로 생성했는데 결과가 갈리는 것"이 버그가 아닐 수 있다** (연결점 ㊵): 📄 arXiv **Toward Uncertainty Quantification in Modern Art**([2608.04038](https://arxiv.org/abs/2608.04038)) — *같은 작품을 다른 시드로 애니메이션하면 눈에 띄게 다른 영상이 나온다. **현대 미술은 의도적으로 애매하므로 이 불일치는 노이즈가 아니라 신호다.*** 🧠 논리를 옮기면 — **원 문서가 애매할 때 산출이 갈리는 것은 정상이고, 갈림의 크기가 입력 명세의 애매함을 재는 눈금**이다. 🧠 실행 후보(순수 제안): 같은 입력으로 N회 생성해 **산출 분산을 "요청 명세 품질 지표"로 측정** → [[올림푸스-기획요청서-작성요령]]. ㊲의 점수가 *산출물 품질*을 재면 이 분산은 *입력 품질*을 잰다.
- 🚨 ⭐⭐ **🆕 (2026-08-20) 오답의 처방이 「모델·프롬프트」가 아니라 「문안의 소유자 지정」이라는 증거 2건이 같은 날 나왔다** ([[AI-주간-소식-2026-W34]] 8차 감사 회수분):
  - 📄 **DGIST 행정 AI**(KR48 신사실) — *"**최신 자료를 담당 부서가 관리**해 생성형 AI의 잘못된 답변 가능성을 줄이고, 대학 주요 지식을 체계화한다"*. 🧠 오답을 리랭커·프롬프트·모델 교체로 막는 게 아니라 **지식 항목마다 책임 부서를 배치**해서 막는다.
  - 📄 **네이버**(KR76) — *생성형 AI 검색·지식백과의 **답변 정확도 및 품질**을 높이려 **정제된 출판·잡지 텍스트 데이터를 확보***(플랜티엠 잡지 콘텐츠 공급 계약). 🧠 답변 품질을 올리려 고른 수단이 **모델이 아니라 정제 코퍼스 구매**였다.
  - ✅ 🧠 **적용안**: `solution_rules`·시나리오 레퍼런스 라이브러리의 각 항목에 **「소유자 + 최신 확인일」 두 필드**를 둔다. 🧠 이건 [[AI-주간-소식-2026-W33]] **(EN42)** *보존만으로는 **권위 있는 상태**를 식별하지 못한다* 와 [[AI-주간-소식-2026-W34]] **(EN4)** *저장된 메모리가 열화한다* 가 요구한 층의 **가장 값싼 구현**이고, ㊲ 홀드아웃 채점(*산출물 품질*)·㊵ 산출 분산(*입력 품질*)에 이어 **「재료의 신선도」** 를 재는 세 번째 눈금이다.
  - ⭐ 🧠 **판정 쪽 보강 근거도 같은 날 도착**: 📄 (KR77) 국내 언론이 *ChatGPT·Gemini·Perplexity·Claude **4개 모델**을 병용*해 분석 기사를 냈다 — ②-b(*평가자를 피평가자와 분리*)의 **상용 구현**이 이미 지면에서 돈다. ⚠ 단 위 ㉚의 금지선은 그대로다: **여러 모델로 후보를 생성하는 것은 되고, 여러 모델에게 다수결 판정을 맡기는 것은 안 된다.**
- 🔥 🚨 ⭐⭐ **🆕 (2026-08-22) 평가 기준 자체가 틀렸을 수 있다 — 이 도구는 「자동화」가 아니라 「증강」이다** ([[AI-주간-소식-2026-W34]] 11차 보강, 영문 8/21):
  - 📄 **CentaurBench**([`2608.18554`](https://arxiv.org/abs/2608.18554)) — *대부분의 LLM 벤치마크는 **업무를 자동화하는** 능력으로 모델 순위를 매긴다. 그러나 실제로 모델은 다른 (사람 또는 LLM) 에이전트를 **보조**하는 데 쓰이는 경우가 많다. 따라서 모델 선택을 좌우하는 질문은 **"어떤 모델이 가장 좋은 결과를 내는가"만이 아니다**.*
  - 🚨 🧠 **이 도구의 산출물은 검수자가 고쳐서 쓰는 초안**이다 — 즉 증강 축인데, 지금 품질 기준(zod/closed-world 통과율 · ㊲ 홀드아웃 점수 · ㊵ 산출 분산)은 **전부 "모델이 혼자 얼마나 잘 뽑는가"** 를 잰다. ⚠ 셋 다 유효하지만 **재는 축이 하나 비어 있다**.
  - ✅ **적용안**: **「검수 비용」을 1급 지표로 추가** — 생성본 대비 *수정된 필드 수 / 수정까지 걸린 시간 / 통째 폐기 비율*. 🧠 이 수치는 이미 어드민에 로그를 남길 수 있는 위치에 있고(승인 게이트), ㊲의 *산출물 품질* · ㊵의 *입력 품질* 에 이어 **「사람에게 넘길 때의 상태」** 를 재는 네 번째 눈금이다.
  - 🧠 같은 교정이 [[mailer|CS SmartHub]]에도 걸린다 — *봇이 몇 %를 혼자 처리했는가* 만이 아니라 **상담원에게 얼마나 좋은 상태로 넘기는가**((KR15) 은행권 옴니채널의 *"상담직원에게 필요 정보를 적시 제공"*).
- 🚨 ⭐⭐ **🆕 (2026-08-22) 모델 비교에 「설정 고정」 칸이 하나 더 필요하다** ([[AI-주간-소식-2026-W34]] (W34-EN46)):
  - 📄 **Same Facts, Different Updates: Inference Setup Shapes LLM Behavior in Medical Allocation**([`2608.18108`](https://arxiv.org/abs/2608.18108)) — *선행 연구는 **입력과 시나리오 프레이밍**에 따른 모델 편향을 다루지만, 모델은 **[추론 셋업]에 따라서도** 예상치 못하게 행동할 수 있다.*
  - 🚨 🧠 **(KR25) 모델별 윤리 판단 차이 · (KR90) LLM 21개가 사용자 정치 성향에 맞춰 답을 바꾼다** 의 **「같은 모델 내부」 판본**이다 — 모델을 고정해도 **추론 설정만으로 결론이 갈린다**.
  - ✅ **적용안**: `flow/usage.ts` 기록에 **모델명 + 버전 + temperature·샘플링·배치 설정**을 함께 남긴다. 🧠 [[AI-주간-소식-2026-W33]] (EN41) *시점 고정* 에 **「설정 고정」** 이 붙어야 ㊵(산출 분산 = 입력 품질 눈금)이 성립한다 — ⚠ **설정이 흔들리면 분산이 입력 애매함인지 설정 노이즈인지 구분되지 않는다.**
- 🚨 ⭐⭐ **🆕 (2026-08-22) 「소유자 + 최신 확인일」의 상위 처방이 나왔다 — 삭제가 아니라 「되돌릴 수 있는 폐기」** ([[AI-주간-소식-2026-W34]] (W34-EN25)):
  - 📄 **Towards Reversible Forgetting: Managing Obsolete Knowledge in Continual Enterprise AI Agents**([`2608.18177`](https://arxiv.org/abs/2608.18177)) — *지속학습은 전통적으로 **망각을 실패로** 취급하며 기존 지식의 **보존**을 강조해 왔다. 우리는 **비정상 환경에서 동작하는 기업 AI 에이전트에는 이 목표가 불완전**하다고 주장한다.*
  - 🧠 **「축적의 부패」 축의 6번째이자 처음 나온 처방**이다: (W33-EN42) *보존만으로는 권위 있는 상태를 식별하지 못한다* → (W33-EN45) *저장된 메모리가 열화한다* → (W34-EN4) MobileMem → (KR48) DGIST 담당 부서 → (KR76) 네이버 정제 코퍼스 → **여기**.
  - ✅ **적용안(위 8/20 항목의 확장)**: `solution_rules`·레퍼런스 라이브러리에 **「소유자 + 최신 확인일」** 에 더해 **`deprecated` 상태와 복원 경로**를 둔다 — 낡은 문안을 지우면 *왜 그렇게 답했는지* 를 재현할 수 없고, 남겨두면 다시 검색된다. 🧠 CLAUDE.md **§7의 *"어긋나는 원본 자료는 폐기/구버전으로 표시"*** 가 이미 같은 규칙이다(문서 층에는 있고 DB 층에는 없다).
- ⭐⭐ **🆕 (2026-08-22) RAG 검색 품질을 모델 교체 없이 올리는 값싼 축** ([[AI-주간-소식-2026-W34]] (W34-EN17)): 📄 HuggingFace **Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers** — 문서를 단일 벡터가 아니라 **토큰별 다중 벡터**로 두고 질의와 **늦은 상호작용**으로 매칭. 🧠 같은 주 📄 (KR94) 디노티시아 씨홀스가 *하드웨어*로 푼 문제를 **표현 방식**으로 푼다 — 모델도 인프라도 안 바꾼다. ⚠ 대가는 **인덱스 크기·질의 비용 증가**(raw에 수치 없음 → 도입 전 실측). 🧠 (KR91) 넥스트페이먼츠의 *온톨로지 + RAG* 와 함께 **"벡터 검색 단독에서 벗어나는" 신호 2건**.
- **🆕 (2026-07-31) 입력 다양화(v0.5.0)의 학술 짝**: 📄 arXiv **Aethel** — "어휘 중복이 적은 여러 문서에 흩어진 지표·주체를 빠르게 종합"하는 **그래프 검색** 프레임워크. 🧠 POC 문서·API 문서·엑셀 ESD를 파싱해 시나리오 재료로 쓸 때 겪는 문제 그 자체(기법 후보). 🧠 또한 **Cross-organisational Process Mining**(메시지 로그에서 프로세스 역추출)은 [[mailer|CS SmartHub]]의 CS 로그 → 이 도구의 **시나리오 입력**으로 잇는 경로.

## 관련 문서
- 🆕 🚨 ⭐⭐ [[AI-주간-소식-2026-W33]] **16차 보강 · (EN40) `2608.11252` 「국소 검증은 비이식성을 탐지할 수 없다」 — QA 기준의 상위 명제** (2026-08-18): 📄 *단계마다 표현 가능성·파라미터를 확인하는 **국소 검증**으로는, 결론이 **다른 맥락으로 옮겨갈 수 있는지**를 원리적으로 알 수 없다*(코호몰로지 정리). 🧠 **스키마 검증 100%·단계별 통과는 전부 국소 검증**이다 — *"이 시나리오가 다른 채널·다른 도메인에서도 서는가"* 는 그걸로 보증되지 않는다((EN39) *Deliberative Deficit* 의 일반화). ✅ 함의: **이식성 테스트를 QA에 별도 축으로 둔다**(같은 시나리오를 다른 채널 가정으로 굴려 보기).
- 🆕 ⭐⭐ [[AI-주간-소식-2026-W34]] **(W34-EN6) 오해의 생성·증폭·탐지 분류체계**(`2608.13604`): 📄 *AI 매개 채널이 **복구(repair)가 의지하던 자원에서 사용자를 끊어놓는다*** → ✅ *"못 알아들었을 때"* 되묻기 분기를 **예외 처리가 아니라 1급 설계 대상**으로 올리고, **증폭 경로**(오해가 다음 턴으로 번지는 길)를 따로 모델링한다. 📄 대상 챗봇이 **사용자 발화↔봇 응답 엄격 교대**라 증폭 경로가 선형이어서 모델링이 오히려 쉽다.
- 🆕 ⭐ **흐름도·평가 관련 3편** — 📄 **PFD→P&ID**([[AI-주간-소식-2026-W33]] (EN49) `2608.11220`): *상위 흐름도 → 검증된 상세 명세* 변환의 자동화가 이 툴과 **구조가 같다**. ⚠ (EN32) MindTopo(*VLM은 연결·차단·교차 같은 **위상 관계**를 생각만큼 못 읽는다*)와 겹쳐 읽으면 — **흐름도는 이미지가 아니라 구조화된 표현으로 주고받아야 한다**는 근거가 2편이 됐다. 📄 **Doctorina MedBench**(`2603.25821`): 시나리오 품질은 **문항 정답률이 아니라 대화 시뮬레이션**으로 잰다. 📄 **동조 완화의 단일 프론티어**((EN50) `2608.11247`): 검증자의 저항성을 올리면 **유용한 수정도 안 받는다** → 멀티에이전트 QA에서 **검증자 완고함을 파라미터로** 둔다.
- 🆕 ⭐ **권한 설계 — 「허가 전파」 축 네 번째 칸**: (KR47) 규제 → (EN26) MAP-Graph 아키텍처 → (KR70) 픽셀 제품 → 🆕 **[[AI-주간-소식-2026-W34]] (W34-EN2) Agentao**(`2608.13574`, *도구 호출·**로컬 상태 수정**·지속 메모리가 **과다 권한** 위험을 낳는다* → 로컬 우선 거버넌스 **런타임**). ✅ 접근 통제는 동의 UI가 아니라 **데이터별 사용 허가 + 파생 전파**이고, 그 **집행 지점은 런타임**이다.
- 🆕 ⚠ **모델 비교 실험엔 유효기간이 있다**: 📄 [[AI-주간-소식-2026-W34]] (KR25)의 다중 LLM 비교가 쓴 **Gemini 3.6 Flash**는, 📄 8/14 **Gemini 3.7 Flash 발표**((W33-EN46))로 실험 기록 시점에 이미 구버전이었다. ✅ **모델 비교·산출 분산 실측은 「언제 기준」과 함께만 쓴다**((W33-EN41) *시점 고정*).
- [[프로젝트-포트폴리오]] · [[내-프로필]] · [[공통-기술스택]] · [[parking]] · [[claude-api]] · [[Claude-Code-업데이트-동향]] · [[mailer]] · [[schedule-reporter-kakao]]
- [[AI-주간-소식-2026-W31]] — 🆕 비용 개선 순서(설정→티어링→모델 교체) · ⚠ TRACE-ROUTER 티어링 주의 · ARCHER(실행 가능한 규정) · ⚠ Air-Gapped 사실 누락 L0–L8 (위 「의외의 연결점」 근거)
- [[AI-주간-소식-2026-W32]] — 🆕 🚨 **10·11차 보강: 한국어 특정 리스크(㉛ 요청→계획 변환에서 정보 손실) · QA를 홀드아웃 채점 루프로(㊲) · 「LLM 다수결 판정」 금지(㉚) · 직렬 단일 위상 지적(㊱) · 산출 분산 = 입력 품질 눈금(㊵) · 증거→확률/비용→행동 분리가 ㉕의 일반형(㉜)** · ⭐ **9차 보강: QA 게이트 규칙 = 오류 비용이 높을수록 LLM을 「판정→생성」으로 좁힌다**(K방산, 연결점 ㉕) · **실드스트랄 Apache 2.0 = 안전 게이트 오픈 부품**(연결점 ㉖) · 턴 vs 턴리스 분기(⑤) · 모델 간 신뢰도 비교 불가(⑦) · 궤적 단위 게이트(⑯) · 6단계 = 지연 6배, 스트리밍 vs 검증 충돌(⑲) · 오픈소스 티어링의 라이선스 계보 확인(㉓)
