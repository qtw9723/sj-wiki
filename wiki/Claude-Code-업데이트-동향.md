---
title: Claude Code 업데이트 동향 (2026 W18–W22)
category: AI/업계 동향
tags: [claude-code, 동향, 도구, llm, 자동화]
source: "raw/What's new.md, raw/Week 18~22"
created: 2026-06-09
updated: 2026-06-15
---

> [!warning] ⚠ stale — 갱신 대기 (2026-06-15 검진)
> 이 페이지는 **W22(~5/29)까지만** 반영됨. 현재 W23~W25(6월 전반) 업데이트가 누락된 상태다. 정확한 갱신은 raw 자료(`What's new`·주차별 노트) 입수 후 진행 — 추측 작성을 피하기 위해 보류 중.

> [!tip] 핵심 takeaway
> 이 5주치 흐름의 한 줄: **"AI가 한 번에 더 큰 일을, 더 자율적으로, 더 안전하게"** — 모델(Opus 4.8)·오케스트레이션(workflows/goal)·안전망(auto mode/security plugin)이 동시에 강해졌다.
> [[내-프로필]] 관점 우선순위: ① **dynamic workflows·/goal** = 네 [[공통-기술스택]] 일괄 작업/[[Cogi-POC-Generator]] 개발 가속에 직결 ② **security-guidance plugin** = 네가 만드는 도구의 취약점 자동 점검 ③ **routines/schedule** = [[schedule-reporter-kakao]]식 자동화의 상위호환. 자세한 자동화 활용은 [[에이전트-자동화-도구]] 참고.

## 주차별 핵심 (최신순)
**Week 22 (5/25–29) · v2.1.150–157**
- **Claude Opus 4.8** 기본 모델화 (Max/Team/Enterprise/API). 기본 high effort, 어려운 작업은 `/effort xhigh`. ID `claude-opus-4-8`.
- **Dynamic workflows**: Claude가 스크립트를 짜 수십~수백 서브에이전트를 백그라운드로 오케스트레이션. 코드베이스 전체 감사·대규모 마이그레이션용. `/workflows`로 관리.
- **security-guidance 플러그인**: 편집마다 패턴 점검 + 턴 종료 시 모델 리뷰 + 커밋/푸시 시 심층 리뷰. 규칙은 `.claude/claude-security-guidance.md`.
- **Fast mode on Opus 4.8**: $10/$50 per MTok (약 2배 가격, 약 2.5배 속도).

**Week 21 (5/18–22)**: Pro 플랜 **auto mode**(Sonnet 4.6 지원) · `/usage` 카테고리별 사용량 분석 · **`/code-review`**(정확성 버그 보고, `--comment`로 PR 인라인) · 백그라운드 세션 `/resume` 노출.

**Week 20 (5/11–15)**: **`claude agents`**(모든 세션 한 화면 대시보드) · **`/goal`**(완료 조건 충족까지 자동 반복) · fast mode 기본 Opus 4.7.

**Week 19 (5/4–8)**: 플러그인 `.zip`/URL 로드 · `Ctrl+R` 전 프로젝트 히스토리 검색 · `worktree.baseRef` · auto mode **hard deny** 규칙 · 훅에 effort 레벨 전달.

**Week 18 (4/27–5/1)**: Windows에서 Git Bash 불필요(PowerShell) · **`claude ultrareview`**(CI/스크립트용 클라우드 리뷰) · `claude project purge` · PR URL을 `/resume`에 붙여 세션 복귀.

## 너에게 의미 있는 변화 (요약)
- 개발 가속: `/goal`, dynamic workflows, `/code-review`, ultrareview → [[Cogi-POC-Generator]] 같은 POC를 빠르게 키우는 데 직접 활용.
- 안전: security-guidance plugin → 직접 만든 [[mailer]]·[[notepad]] 등의 취약점 자동 점검.
- 자동화: routines/schedule(W16), Monitor/`/loop`(W15) → [[schedule-reporter-kakao]]식 작업의 상위호환.

## 의외의 연결점
- **이 위키 자체가 이 흐름의 산물**: 지금 너는 `/loop`(W15에서 self-pace 지원) + cron으로 raw→wiki 정리를 자동화하고 있다. 즉 동향 기사 속 기능을 **읽는 동시에 쓰고 있는** 셈.
- dynamic workflows는 [[공통-기술스택]]의 "전 프로젝트 동일 스택" 구조와 궁합이 좋다(일괄 마이그레이션).
- **국내 도입 본격화(2026-06-18)**: 앤트로픽 서울 오피스 개소 + **네이버가 Claude Code를 AI 에이전트로 도입**(넥슨·삼성·LG CNS도 Claude 사용) → 내가 매일 쓰는 이 도구가 국내 대기업 표준으로 자리잡는 중. 상세는 [[AI-주간-소식-2026-W25]] 「국내 동향」.

## 관련 문서
- [[에이전트-자동화-도구]] · [[claude-api]] · [[내-프로필]] · [[Cogi-POC-Generator]] · [[공통-기술스택]]
