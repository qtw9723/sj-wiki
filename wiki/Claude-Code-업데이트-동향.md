---
title: Claude Code 업데이트 동향 (2026 W18–W22)
category: AI/업계 동향
tags: [claude-code, 동향, 도구, llm, 자동화]
source: "raw/What's new.md, raw/Week 18~22, raw/ai-digest/naver-2026-08-08.md"
created: 2026-06-09
updated: 2026-08-08
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
- **⭐ 🆕 (2026-08-08) Claude Opus 4.8이 실제 취약점 발견에 실명으로 인용됐다 — 다만 패치보다 공격이 먼저 왔다** ([[AI-주간-소식-2026-W32]] 14차 보강, 연결점 (52)): 📄 보안 연구자 **테일러 혼비(Taylor Hornby)** 가 지난 5월 **앤트로픽 Claude Opus 4.8을 활용해** BTCPay 서버의 취약점을 찾아냈고, 그 결함으로 **실제 자금 탈취 공격이 발생**해 2.4.2 긴급 업데이트가 권고됐다. 크립토 프로젝트에서 AI 취약점 탐지 사례가 잇따르는 중.
  - 🧠 sangjun이 매일 쓰는 모델이 **보안 감사 용도로 실적과 함께 실명 인용**된 첫 기록 — Claude Code를 코드 리뷰·의존성 감사에 쓰는 것의 외부 근거. 단 위 ㉜과 함께 읽어야 한다: **발견은 시키되 승인 판정은 시키지 않는다.**
  - ⚠ 🧠 교훈은 도구가 아니라 **타이밍**이다 — LLM 취약점 탐지가 흔해지면 *공개 시점 ≒ 공격 시작 시점*이 된다. 내 프로젝트([[올림푸스-Olympus]]·[[mailer|CS SmartHub]])의 의존 라이브러리 CVE 대응을 "나중 일"로 미루기 어려워졌다.
- **🚨 ⭐ 🆕 (2026-08-11) 보안 특화 모델이 「승인 파트너 전용」으로 게이팅됐다 — 그리고 공격 측엔 게이팅이 없다** ([[AI-주간-소식-2026-W33]] 4차 보강, (W33-EN1)):
  - 📄 OpenAI 「**Expanding Daybreak as the Cyber Defense Window Narrows**」(8/10) — **GPT-5.6-Cyber**를 **Daybreak Red**를 통해 *인가된 취약점 연구·**익스플로잇 검증**·보안 테스트* 에 제공. 📄 「Putting frontier cyber models in more trusted hands」 — **승인된 파트너**만 이 모델로 통제된 보안 서비스를 제공.
  - 📄 **연속성**: [[AI-주간-소식-2026-W26]]에 기록된 Daybreak(Codex Security · **GPT-5.5-Cyber** · Patch the Planet)의 7주 뒤 후속이다. 세대 교체 + **공격 측 역량 명시** + **접근 게이팅** 3가지가 동시에 진행됐다.
  - ⭐ 🧠 **위 (52) 항목의 「타이밍」 교훈에 구조적 이유가 붙었다**: 같은 주 한국어 수집분에 📄 **北 김수키가 로컬 LLM + RAG로 공격을 자동화**한 기록이 있다([[AI-주간-소식-2026-W33]] (W33-KR2)). 🧠 **게이팅은 프런티어 모델에만 걸리고 오픈웨이트 로컬 모델에는 걸리지 않는다** — 즉 *"공개 시점 ≒ 공격 시작 시점"* 은 공격 측 도구 조달이 이미 통제 밖이라서 생기는 결과다. ✅ 실무 결론은 그대로 강화된다: **의존 라이브러리 CVE 대응을 미루지 않는다**([[올림푸스-Olympus]]·[[mailer|CS SmartHub]]).
  - ⚠ 🧠 sangjun이 쓰는 건 Claude Code security plugin 쪽이라 직접 영향은 없지만, 사내 도입 논의에서는 **"보안 특화 모델을 누가 승인해 주는가"** 가 새 질문으로 붙는다. 📄 한국 기업의 Daybreak 접근 조건은 raw에 없음 → **불명**.
- **⚠ 규칙 문서의 비대화**: 📄 Constitutional AI 원칙이 2023년 2,700단어 → 2026년 **23,000단어**로 확장([[AI-주간-소식-2026-W31]]). 🧠 이 위키의 `CLAUDE.md`·[[올림푸스-Olympus]] 역할 지침처럼 **"에이전트를 문서로 통제한다"**는 방식이 업계 공통 경로임을 보여준다 — 규칙 문서 자체의 유지보수가 새 스킬 축.

## 관련 문서
- [[에이전트-자동화-도구]] · [[claude-api]] · [[내-프로필]] · [[CogInsight-Generator]] · [[공통-기술스택]]
- [[AI-주간-소식-2026-W33]] — 🚨 ⭐ 🆕 **(W33-EN1) OpenAI Daybreak 확장 = GPT-5.6-Cyber + Daybreak Red + 승인 파트너 게이팅**([[AI-주간-소식-2026-W26]] GPT-5.5-Cyber의 직계 후속) · 🧠 같은 주 (W33-KR2) **北 로컬 LLM+RAG 공격 자동화**와 나란히 = **게이팅은 프런티어에만, 오픈웨이트엔 없다** · 📌 8/14 Auto Mode 기본 전환 확인 항목
- [[AI-주간-소식-2026-W26]] — 📄 **Daybreak 최초 기록처**(Codex Security · GPT-5.5-Cyber · Patch the Planet) — 위 (W33-EN1)의 출발점
- [[AI-주간-소식-2026-W32]] — 🆕 ⭐ **(52) Claude Opus 4.8의 BTCPay 취약점 발견(실명 인용) — 감사 용도 실증, 단 "발견↔패치" 시간차가 곧 공격 창구** · 🆕 **㊾ 나이브(Naïve) 시리즈A 2,850만 달러 = Claude Code에 붙는 프롬프트 레이어가 독립 시장으로** · 🆕 ⚠ **㉜ AI 코드리뷰는 승인 게이트가 아니라 증거 수집기로**(배포된 리뷰어 4종의 확률/행동 분리 검증) · ㉒ 생태계+가격 경쟁(메타 뮤즈코드·AWS 중립화) · ⑳ 큐원 TerminalBench 추월 · ㉘ Claude의 국내 공공 조달 진입(부산)
