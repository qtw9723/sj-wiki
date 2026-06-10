---
title: Cogi-POC-Generator (Dialog JSON Generator)
category: 프로젝트
tags: [프로젝트, 챗봇, 시나리오, dialog-json, llm, 핵심]
source: raw/projects/cogi-poc-generator-v1.md
created: 2026-06-09
updated: 2026-06-09
---

> [!tip] 핵심 takeaway
> ⭐ **이게 [[내-프로필]]의 "LLM 활용 챗봇 시나리오 구성 툴"의 실체로 보인다.** Cogi **Dialog JSON Generator** = 챗봇 대화 시나리오를 JSON으로 찍어내는 POC 제너레이터.
> 즉 네 커리어 전환의 **핵심 프로젝트**. NLP 챗봇 회사의 도메인 지식 + 풀스택 역량이 한곳에서 만난다.
> 다음 레버리지: 여기에 LLM 호출을 붙여 "자연어 → Dialog JSON 자동 생성"으로 키우면, [[Claude-Code-업데이트-동향]]의 LLM/에이전트 흐름과 정확히 합류한다. ([[claude-api]] 참고 여지)

## 개요
- 설명: Cogi Dialog JSON Generator — POC 제너레이터. 프론트엔드. 버전 1.0.1.
- 상태: ✅ 배포 준비 완료 (배포 문서 6종 완비: PROJECT_SUMMARY, GETTING_STARTED, DEPLOYMENT, DEPLOYMENT_CHECKLIST, MIGRATION_INSTRUCTIONS). 단 CLAUDE.md는 없음.
- 최근 2026-05-27.

## 기술 스택
[[공통-기술스택]] 기반 + 폼/검증 강화:
- Radix UI + shadcn (컴포넌트), tailwind-merge
- react-hook-form + **zod**(스키마 검증) — Dialog **JSON 구조 검증**에 핵심
- Supabase([[parking]]), TypeScript

## 왜 중요한가 (챗봇 도메인 ↔ 개발)
- "Dialog JSON"은 챗봇 대화 흐름의 정의 포맷. 이걸 생성·검증하는 도구라는 점에서, 네가 회사에서 하는 **챗봇 시나리오 구성**을 자동화/도구화한 것.
- zod로 JSON 스키마를 강제하는 구조 → 향후 **LLM이 생성한 시나리오를 zod로 검증**하는 파이프라인으로 확장하기 좋다(LLM 환각 방지의 정석 패턴).

## 의외의 연결점
- ⭐ **회사 업무와 직결**: 이 도구가 만드는 Dialog JSON = 회사에서 손으로 짜는 챗봇 **Case 시나리오**와 같은 산출물. 즉 개인 도구로 본업 시나리오 작업을 가속할 잠재력 — 사이드 프로젝트와 본업이 만나는 지점. (회사 상세는 PC 전용 `sj-wiki-work` vault)
- **zod 검증 ↔ 실전 스키마**: 실무 API/DB 스펙을 zod로 박제하면 시나리오 목업/검증에 그대로 재사용 — LLM 생성 시나리오의 환각 방지 파이프라인의 실전 입력값이 된다.
- [[mailer]]·[[schedule-reporter-kakao]]가 "업무 자동화 축"이라면, 이 프로젝트는 "챗봇 도메인 축". 둘 다 [[공통-기술스택]]+[[parking]]을 공유하므로, 너의 두 강점이 같은 기반 위에서 자란다.
- POC 단계 → [[Claude-Code-업데이트-동향]]의 `/goal`·dynamic workflows로 "스키마 채우기·테스트까지 자동 반복" 같은 개발 가속이 가능.

## 관련 문서
- [[프로젝트-포트폴리오]] · [[내-프로필]] · [[공통-기술스택]] · [[parking]] · [[claude-api]] · [[Claude-Code-업데이트-동향]]
