# Cogi-POC-Generator-v1

## 프로젝트 개요
- **설명**: Cogi Dialog JSON Generator — 챗봇 시나리오(대화 흐름) JSON을 LLM으로 생성하는 POC 제너레이터 + 학습/관리 어드민
- **유형**: 풀스택 (프론트 React SPA + Supabase Edge Functions 백엔드 + Postgres)
- **버전**: 1.0.1
- **경로**: `/Users/sangjun/IdeaProjects/Cogi-POC-Generator-v1`
- **마지막 raw 갱신**: 2026-06-25 (커밋 ~203개 / 2026-06-09 이후)

## 기술 스택 (확인: package.json, README, supabase/functions)
- **프론트**: React 19.2 + Vite 8 + React Router 7 + Tailwind CSS 4 + Radix UI/shadcn + lucide-react
- **폼/검증**: react-hook-form 7.76 + zod 4.4
- **백엔드**: Supabase Edge Functions (Deno/TypeScript) — 20개 함수
- **DB**: Supabase Postgres (40개 마이그레이션, RLS)
- **LLM**: OpenAI `gpt-4o` (temperature 0.1) — cogi-generator / derive-node-specs / learn-rules / admin-solution-rules. (주의: GEMINI는 mailer/grafana 프로젝트용, Cogi 아님)
- **배포**: 프론트 Vercel(main 푸시 자동), 엣지함수 `supabase functions deploy`, DB `supabase db push`

## 생성 파이프라인 (cogi-generator, 다단계)
1. designFlow (Stage 1) — LLM이 플로우 설계(FlowSpec). 검증(reachability)·repair·1회 재요청
2. expandWithSpecs (Stage 2) — FlowSpec → 노드에디터 JSON 결정론적 전개, variant(판별 유니온) 소비
3. fillNodeValues (Stage 2.5) — set/esd/api config 값 채우기 (전담 패스 + 재시도)
4. deriveEsdSchemas — ESD 스키마 동시 생성
5. deriveApiDefs (Stage 2.6) — API 연동에서 import용 API 정의 생성
6. renderPrompts/output 패스 — 멘트(말투 반영), 변수 `${var}` 보간
- LLM 토큰 사용량·예상비용 집계·표시 (flow/usage.ts)
- 생성 규칙은 코드 하드코딩 X → solution_rules(DB)에서 단계별로 프롬프트에 주입 (data-driven)

## 규칙 시스템 (data-driven, CLAUDE.md)
- source of truth = `solution_rules` 테이블. 어드민(`/admin/solution-rules`) 또는 레퍼런스 학습으로 추가
- 7 카테고리 → 주입 단계 매핑: Solution Rule/Node Usage→flow, Variable Usage→flow+config+output, Value Generation→config, Output Message→output, Condition→condition, System Variable
- 예외: 결정론적 안전장치(repairFlow의 루트 stack 제거, 변수 선언강제 등)는 코드에 유지

## Edge Functions (20)
- 생성/학습: cogi-generator, derive-node-specs(노드스펙 결정론 추출+LLM 일반화+closed-world 검증), learn-rules(레퍼런스 JSON 구조 학습)
- 레퍼런스 라이브러리: scenario-references(시나리오 미니봇 CRUD+조립), api-references(API 정의 CRUD+실호출 test 프록시)
- 어드민 CRUD: admin-questions, admin-references, admin-results, admin-solution-rules, admin-templates, admin-testers, admin-rule-field-definitions, admin-rule-templates, admin-rule-value-generators
- 공개/사용자: questions, references, results
- 인증: trusted-device(신뢰기기 등록/로그인)
- 기타: feedback, test(테스트스위트)

## DB 테이블 (주요)
- questions, templates — 설문/질문 템플릿(role: required_context/optional_context/constraint/intent/preference, group_list 중첩)
- solution_rules — 생성 규칙(7 카테고리)
- cogi_references — 학습용 마스터 레퍼런스(basic_rules/nodeSpecs/generation_template, master-child)
- cogi_results — 생성 결과(generated_json, user_responses, user_id, reference_id) — 계정별 스코프
- cogi_scenario_references — 시나리오 미니봇 학습자료(category: 금융/물류/소매/도매/의료/기타, flow_json, integration_method/api_fields/api_param_hint)
- cogi_api_references — import용 API 정의(엔드포인트당 1행)
- cogi_feedback — 사용자 피드백
- features — (구) 기능 메타. features 레이어는 2026-06-16에 제거되어 레퍼런스로 일원화
- testers — 테스터 계정 승인 워크플로(status: pending/approved/blocked, approved_by/at)
- trusted_devices — 신뢰기기 토큰(sha256 token_hash, 30일 TTL)
- rule_field_definitions, rule_templates, rule_value_generators, condition_patterns — 규칙 보조 데이터
- (레거시 제거: field_schemas/value_mappings 등 값-할당 3탭 관련은 2026-06-17 제거)

## 프론트 라우트
- 사용자(RequireAuth): `/`(QuestionnaireForm), `/results`, `/results/:id`, `/scenarios`(시나리오 라이브러리 단일/조립)
- 로그인: `/login`(테스터 이메일 OTP + 신뢰기기), `/admin/login`
- 어드민(ProtectedRoute, 8탭): questions, references, templates, solution-rules, rules, scenario-references, api-references, feedback, testers

## 인증
- 어드민: 하드코딩 자격(POC용, localStorage adminToken) — 회사 외부 노출 금지, 일반화만 위키에
- 테스터: Supabase 이메일 OTP → 신뢰기기 등록(localStorage 토큰, 서버에 sha256 30일) → 재방문 시 이메일만으로 로그인
- 승인 게이트: 가입 시 status=pending → 어드민 승인 → approved 만 사용자 페이지 접근. 결과는 계정별(user_id) RLS 스코프
- 커스텀 SMTP: OTP rate limit 회피 위해 Gmail 허브 계정으로 (앱비번/계정은 위키 미기재 — 시크릿)

## 2026-06-09 이후 주요 변경 (feature-level)
- Flow 단계 1급화: Stage1 LLM 플로우 설계 → Stage2 결정론적 JSON 전개 (legacy 전체-JSON LLM 경로 제거)
- 레퍼런스→노드스펙 파생(closed-world), 판별 유니온 variant 다중선택
- 질문 유형 시스템: group_list/select/multi_select 중첩, 시나리오 입력 UI
- 레거시 값-할당 3탭(필드스키마/조건패턴/값할당) + features 레이어 제거
- STAGE 2.5 값 채우기, ESD 스키마 동시생성, output 멘트 전담패스, 변수 `${}` 보간, use-before-declare 차단, 시스템 식별자 난수생성
- LLM 토큰/비용 집계 표시
- data-driven rules 전환(solution_rules가 SoT) + 규칙 어드민/학습 관리 원칙
- 시나리오 레퍼런스 라이브러리(few-shot 주입 + 사용자 단일/조립), API 레퍼런스 라이브러리(+ 실호출 test)
- 사용자 피드백(플로팅 버튼→팝오버, 미완료 배지)
- 테스터 이메일 OTP 인증 + 승인 게이트 + 계정별 결과 + 신뢰기기 로그인 + 어드민 테스터 관리
- 시나리오/분기/API 폼 도움말·툴팁 추가
