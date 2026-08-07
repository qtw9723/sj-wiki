---
title: Claude Code 업데이트 동향 (2026 W18–W22)
category: AI/업계 동향
tags: [claude-code, 동향, 도구, llm, 자동화]
source: "raw/What's new.md, raw/Week 18~22"
created: 2026-06-09
updated: 2026-08-07
---

> [!warning] ⚠ stale — 갱신 대기 (2026-06-15 검진)
> 이 페이지는 **W22(~5/29)까지만** 반영됨. 현재 W23~W25(6월 전반) 업데이트가 누락된 상태다. 정확한 갱신은 raw 자료(`What's new`·주차별 노트) 입수 후 진행 — 추측 작성을 피하기 위해 보류 중.

> [!tip] 핵심 takeaway
> 이 5주치 흐름의 한 줄: **"AI가 한 번에 더 큰 일을, 더 자율적으로, 더 안전하게"** — 모델(Opus 4.8)·오케스트레이션(workflows/goal)·안전망(auto mode/security plugin)이 동시에 강해졌다.
> [[내-프로필]] 관점 우선순위: ① **dynamic workflows·/goal** = 네 [[공통-기술스택]] 일괄 작업/[[CogInsight-Generator]] 개발 가속에 직결 ② **security-guidance plugin** = 네가 만드는 도구의 취약점 자동 점검 ③ **routines/schedule** = [[schedule-reporter-kakao]]식 자동화의 상위호환. 자세한 자동화 활용은 [[에이전트-자동화-도구]] 참고.

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
- 개발 가속: `/goal`, dynamic workflows, `/code-review`, ultrareview → [[CogInsight-Generator]] 같은 POC를 빠르게 키우는 데 직접 활용.
- 안전: security-guidance plugin → 직접 만든 [[mailer]]·[[notepad]] 등의 취약점 자동 점검.
- 자동화: routines/schedule(W16), Monitor/`/loop`(W15) → [[schedule-reporter-kakao]]식 작업의 상위호환.

## 의외의 연결점
- **이 위키 자체가 이 흐름의 산물**: 지금 너는 `/loop`(W15에서 self-pace 지원) + cron으로 raw→wiki 정리를 자동화하고 있다. 즉 동향 기사 속 기능을 **읽는 동시에 쓰고 있는** 셈.
- dynamic workflows는 [[공통-기술스택]]의 "전 프로젝트 동일 스택" 구조와 궁합이 좋다(일괄 마이그레이션).
- **국내 도입 본격화(2026-06-18)**: 앤트로픽 서울 오피스 개소 + **네이버가 Claude Code를 AI 에이전트로 도입**(넥슨·삼성·LG CNS도 Claude 사용) → 내가 매일 쓰는 이 도구가 국내 대기업 표준으로 자리잡는 중. 상세는 [[AI-주간-소식-2026-W25]] 「국내 동향」.
- **제품 방향 확인(2026-07)**: 📄 Anthropic 공식 블로그가 Claude Code를 **"CLI 페어 프로그래머 → 자율 소프트웨어 운영 플랫폼"**으로 규정(Code w/ Claude SF 2026), 📄 Claude 미국 모바일 챗봇 점유율 17%·웹 2.22%→8.9%, 📄 **Fable 5(Mythos 티어) 2026-06-09 출시 — SWE-bench 95.0%로 코딩 1위**(2위 Opus 4.8 88.6%). 상세·출처는 [[AI-주간-소식-2026-W31]].
- **⚠ 🆕 (2026-08-07) AI 코드리뷰를 "승인 게이트"로 쓰지 말 근거가 나왔다** ([[AI-주간-소식-2026-W32]] 10차 보강, 연결점 ㉜): 📄 arXiv **When Policies Change Probabilities: Modular Decision-Making for LLM Code Review**([2608.02677](https://arxiv.org/abs/2608.02677)) — *LLM 코드리뷰어는 **패치 위험도 추정과 승인 결정을 한 프롬프트에서** 하는 경우가 많다. **확률은 증거에 의존해야 하고, 비용이 그로부터 취할 행동을 결정해야 한다.** 우리는 **배포된 리뷰어 인터페이스 4종**이 이 분리를 보존하는지 시험한다.*
  - 🧠 시험 대상이 *"배포된"* 도구들이라는 게 핵심이다 — 시중 AI 리뷰 도구가 이 분리를 안 지킬 가능성이 연구의 전제다. 🧠 실무 규칙: **AI 리뷰는 증거 수집기로 쓰고, 승인·머지 판정은 결정론적 게이트(테스트·CI)에 남긴다.** [[올림푸스-Olympus]] `verify.sh`가 이미 그 구조이고, W32 연결점 ㉕(*오류 비용이 높을수록 LLM을 판정에서 생성으로 좁힌다*)의 코드리뷰 판본이다.
- **⚠ 🆕 (2026-08-06~07) 코딩 에이전트 경쟁이 「성능」에서 「생태계+가격」으로, Claude는 공공 조달로**: 📄 메타 **뮤즈코드**가 Claude Code를 직접 겨냥해 $12/100만 토큰으로 진입 · 📄 AWS가 앤트로픽·오픈AI **양쪽 모두와** 보안 파트너십(중립 게이트키퍼화) · 📄 알리바바 **큐원 3.8-맥스가 TerminalBench-2.1에서 86.6점 — 페이블5(84.6) 추월** · 📄 **부산 공공기관이 Claude AI 기반 디지털 역량 강화 플랫폼**을 우수사례로 발표(이 위키 기준 Claude가 국내 **공공 조달·시민 서비스 백엔드**로 잡힌 첫 기록). 상세는 [[AI-주간-소식-2026-W32]] 7~9차 보강(연결점 ⑳·㉒·㉘).
- **⚠ 규칙 문서의 비대화**: 📄 Constitutional AI 원칙이 2023년 2,700단어 → 2026년 **23,000단어**로 확장([[AI-주간-소식-2026-W31]]). 🧠 이 위키의 `CLAUDE.md`·[[올림푸스-Olympus]] 역할 지침처럼 **"에이전트를 문서로 통제한다"**는 방식이 업계 공통 경로임을 보여준다 — 규칙 문서 자체의 유지보수가 새 스킬 축.

## 관련 문서
- [[에이전트-자동화-도구]] · [[claude-api]] · [[내-프로필]] · [[CogInsight-Generator]] · [[공통-기술스택]]
- [[AI-주간-소식-2026-W32]] — 🆕 ⚠ **㉜ AI 코드리뷰는 승인 게이트가 아니라 증거 수집기로**(배포된 리뷰어 4종의 확률/행동 분리 검증) · ㉒ 생태계+가격 경쟁(메타 뮤즈코드·AWS 중립화) · ⑳ 큐원 TerminalBench 추월 · ㉘ Claude의 국내 공공 조달 진입(부산)
