---
title: Claude Code 스킬 구성 (내가 쓰는 스킬 전체)
category: 도구/스킬
tags: [claude-code, 스킬, skill, superpowers, gstack, qa-only, office-hours, humanizer, orca, 검증, 오픈소스-경량화]
sources: [~/.claude/skills/*/SKILL.md, ~/.claude/plugins/installed_plugins.json, ~/.claude/settings.json, https://github.com/garrytan/gstack, https://github.com/blader/humanizer, https://github.com/anthropics/claude-plugins-official]
created: 2026-11-17
updated: 2026-11-17
---

> [!tip] 핵심 takeaway
> 직접 만든 스킬은 3개(qa-only, office-hours, humanizer)이고, 모두 오픈소스를 **통째로 설치하지 않고 한국어 경량판으로 옮긴 것**이다. 나머지는 플러그인(superpowers)·Orca 앱·claude.ai 동기화·Claude Code 기본 제공 스킬이다.
> 검증 흐름은 **기본 = superpowers:verification-before-completion, 조건 해당 시 = qa-only 승격**으로 정해 두었다. "개발 후 검증 스킬 이름이 뭐였지?"의 답은 **qa-only**.

📄 = 스킬 파일·설정에서 확인한 사실, 🧠 = 정리하며 붙인 판단. 기준일 2026-11-17.

## 1. 한눈에 보기

| 출처 | 스킬 | 언제 쓰나 |
|---|---|---|
| **직접 제작**(오픈소스 경량판) | `qa-only` | 만들어진 기능을 실제로 돌려 보며 검증, 보고만(코드 안 고침) |
| | `office-hours` | 만들 가치가 있나·방향이 맞나 검증(YC 오피스아워식) |
| | `humanizer` | AI 티 나는 글 다듬기, 주간보고 등 보고서 문장 손질 |
| **superpowers 플러그인** v7.0.2 | brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, test-driven-development, systematic-debugging, verification-before-completion, requesting/receiving-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills, diagnosing-superpowers, using-superpowers | 개발 전 과정의 작업 방식(설계 → 계획 → 구현 → 검증 → 마무리) |
| **Orca 앱** | `orca-cli`, `orca-computer-use`, `orchestration` | Orca 워크트리·터미널·브라우저 조작, 다른 에이전트(Codex 등) 워커에 일 맡기기 |
| **claude.ai 동기화**(`anthropic-skills:`) | docs, docx, pdf, pptx, xlsx, google-workspace, deep-research, chrome-browser, built-in-browser, computer-use, skill-creator, mww-ci-design-apply, morning, import-memory | 문서 파일 작업, 브라우저·데스크톱 조작, 리서치, 회사 CI 적용 |
| **Claude Code 기본** | code-review, security-review, simplify, run, init, loop, schedule, update-config, claude-api, artifact-*, dataviz, workflow-authoring 등 | diff 리뷰, 보안 리뷰, 반복 실행, 설정 변경 등 |

📄 플러그인은 `superpowers`와 `postman`(v2.3.0) 두 개가 켜져 있다(`settings.json` enabledPlugins). 마켓플레이스는 공식 `anthropics/claude-plugins-official` 하나. ⚠ postman 플러그인에도 skills 폴더(api-discovery·api-documentation·api-mocking 등)가 있지만 2026-11-17 세션의 스킬 목록에는 나오지 않는다(원인 미확인).

## 2. 직접 만든 스킬 (오픈소스 경량판)

공통 방침 📄: 원본은 MIT 라이선스. 원본 전용 도구(텔레메트리·자동 업데이트·전용 브라우저·캐시)는 걷어내고, 질문·규칙·양식만 한국어로 옮겼다. 위치는 `~/.claude/skills/<이름>/SKILL.md`.
🧠 gstack을 통째로 설치하지 않은 이유(2026-11-09 결정): 크롬 연동 금지 문구, superpowers와 겹치는 기능, 텔레메트리·자동 업데이트 부담.

### 2-1. qa-only — 개발 후 검증 (2026-11-09)

- 📄 **원본**: [garrytan/gstack](https://github.com/garrytan/gstack) `qa-only/SKILL.md` v1.0.0 + `qa/sections`(scope·qa-patterns·system-functional)·`qa-only/sections`(exploratory·reporting).
- 📄 **바꾼 점**: gstack의 Aside 브라우저 → **claude-in-chrome**(새 탭, alert 등 대화상자·삭제 버튼 회피). deadline/evidence 헬퍼·텔레메트리·learnings·`~/.gstack` 사본 제거.
- 📄 **핵심 규칙**
  - **HARD GATE**: 코드·테스트·설정·의존성·git 상태를 절대 바꾸지 않는다. 쓰는 건 보고서·증거·임시 데이터뿐.
  - 점검 전에 **차터(점검 계획)를 먼저** 보고서에 쓴다. 나중에 계획을 지어내지 않는다.
  - 실패는 **같은 초기 상태에서 다시 실행해 재현 확인**. 한 번만 본 건 "1회 관찰"로 적는다.
  - 표면 2종: **브라우저**(화면, 블랙박스 점검) / **기능**(API·CLI·작업·웹훅, 계약표 10종 — 정상·잘못된 입력·인증·CLI·상태 전이·타임아웃·재시도·멱등성·동시성·부분 실패).
  - **모바일 375×812 점검 필수**(사용자 지시, `빠르게` 모드에서도). `resize_window`가 안 먹으면 iframe으로 대체하고 한계를 적는다(2026-11-09 실측 후 추가).
  - 운영 데이터를 바꾸는 점검은 대상·동작·영향을 밝히고 **사전 승인**. 스킬 호출 자체는 허락이 아니다.
  - 보고서: `<저장소>/.qa-reports/run-<UTC시각>/`(`.git/info/exclude`로 커밋 제외), 발견마다 관찰·기대·증거·확인·심각도, 브라우저 건강 점수, 회귀 테스트는 **제안만**(가치 카드 통과 시).
- 📄 **실사용**: 2026-11-09 [[delivery-smarthub|SmartHub]] 보안 레벨 화면 첫 실행(읽기 전용) → 같은 날 운영 쓰기 허용 전체 점검(Low 4건) → 11-11 배포 후 `회귀` 모드(회귀 0).

### 2-2. office-hours — 만들 가치 검증 (2026-11-09)

- 📄 **원본**: gstack `office-hours/SKILL.md` v2.0.0. brain 캐시·텔레메트리·빌더 프로필·Aside·교차 모델 리뷰 제거.
- 📄 **흐름**: 맥락 파악 → **진단 모드**(사내·사업) 또는 **빌더 모드**(개인·학습) → 전제 도전 → 대안 2~3개(최소안·이상안 필수) → 설계 문서(`docs/designs/<주제>.md`).
- 📄 **진단 모드 6가지 강제 질문**: 수요 현실 / 현상 유지 방식과 비용 / 가장 필요한 실제 사람 / 이번 주에 쓸 최소 버전 / 도와주지 않고 쓰는 걸 관찰했나 / 3년 뒤에도 필요한가. 사내 프로젝트는 "결정권자가 승인할 최소 데모", "챔피언이 떠나도 살아남나"로 바꿔 묻는다.
- 📄 **규칙**: 구현·스캐폴딩 금지, 질문은 한 번에 하나, 아첨 표현 금지(모든 답에 입장 + 그 입장을 바꿀 근거).
- 📄 **brainstorming과 경계**: 가치·방향 검증 = office-hours, 만들기로 정한 것의 설계 = superpowers:brainstorming.

### 2-3. humanizer — AI 티 빼기 (2026-11-12)

- 📄 **원본**: [blader/humanizer](https://github.com/blader/humanizer) v4.0.0(위키백과 "Signs of AI writing" 기반). LICENSE 동봉.
- 📄 **바꾼 점**: 26개 패턴 → 15개. 영어 전용 패턴(하이픈 복합어·둥근 따옴표·is/are 회피) 제외, 한국어 번역투·명사 나열·"~할 수 있습니다"류 추가.
- 📄 **강한 패턴(한 번만 보여도 고침)**: "X가 아니라 Y" 대비, 한 줄 마무리, 깊어 보이는 경구, 본론 앞 예열, 없는 상대와 논쟁.
- 📄 **보고서 규칙**: 번호·셀 구조 등 형식은 그대로 두고 **문장만** 고친다. 주간보고는 항상 이 스킬로 다듬은 뒤 보여준다(사용자 지시).

## 3. 검증 스킬 사이의 경계

📄 qa-only 스킬 본문의 경계표 + 작업 후 검증 규칙(2026-11-09 사용자 지시).

| 상황 | 스킬 |
|---|---|
| 내가 방금 끝낸 작업이 됐는지 확인 후 완료 선언 | superpowers:verification-before-completion (**기본**) |
| 만들어진 걸 직접 써 보며 버그·동작 확인 | **qa-only** |
| 변경 diff를 읽어서 버그 찾기 | /code-review |
| 보안 취약점 | /security-review |
| 원인 파고들어 고치기 | superpowers:systematic-debugging |

**qa-only로 승격하는 조건**(하나라도 해당하면, 묻지 않고 sonnet 서브에이전트에 맡김):
1. 화면 흐름 변경
2. 권한·입력 검증이 있는 API·엣지 함수 변경
3. 운영 배포·머지 직전
4. 고객·외부 전달물
5. 이전 qa-only 보고서가 있는 영역 재수정 → `회귀` 모드

제외: 문구·문서, DB 규칙/데이터만, 스크립트·cron·메일 양식.
🧠 승격 시 새 서브에이전트에 맡기는 이유는 만든 사람의 편향을 피하기 위해서다. 기존 검증이 정상 경로 위주라 화면 상태·API 계약·배포 전 근거가 비어 있던 점을 메운다.

## 4. superpowers 작업 흐름

📄 플러그인 v7.0.2(2026-03-26 설치, 2026-11-13 갱신).
🧠 실제로 거의 매번 쓰는 순서:

```
brainstorming → writing-plans → subagent-driven-development (또는 executing-plans)
   → test-driven-development / systematic-debugging
   → verification-before-completion (+ 조건 해당 시 qa-only)
   → requesting-code-review → finishing-a-development-branch
```

- 병렬로 쪼갤 수 있는 작업은 dispatching-parallel-agents, 격리가 필요하면 using-git-worktrees.
- 세션이 꼬였을 때 원인 분석은 diagnosing-superpowers, 새 스킬 만들 땐 writing-skills(또는 anthropic-skills:skill-creator).

## 5. 그 밖의 스킬 묶음

- 📄 **Orca**(`~/.agents/skills/` → `~/.claude/skills/`에 심볼릭 링크, 2026-11-06): `orca-cli`(워크트리·터미널·Orca 내장 브라우저), `orca-computer-use`(앱 창 GUI를 백그라운드로 조작), `orchestration`(Codex 같은 다른 에이전트를 Orca 워커로 돌리고 결과 받기). 🧠 내 서브에이전트로 되는 일이면 orchestration을 쓰지 않는다.
- 📄 **claude.ai 동기화 스킬**(`~/.claude/skills/synced/`): 문서 파일(docx·pdf·pptx·xlsx), Google 문서, 딥 리서치, 브라우저(Chrome 확장·내장 브라우저), 데스크톱 조작, 스킬 제작기, **mww-ci-design-apply**(회사 CI를 PPT에 적용), 모닝 브리프, 메모리 가져오기.
- 📄 **Claude Code 기본 제공**: code-review(`--fix`·`--comment`), security-review, simplify, run, loop·schedule(반복·예약 실행), update-config(훅·권한), claude-api, artifact 계열, dataviz, workflow-authoring 등.

## 6. 앞으로

- 📄 qa-only·office-hours·humanizer 모두 "실제로 써 보며 조정"이 남은 후속 과제다(질문 강도·트리거·낱말 목록).
- 🧠 같은 방식(MIT 오픈소스 → 한국어 경량판)으로 더 가져올 후보가 생기면 이 페이지 §2에 추가한다.
- 🧠 postman 플러그인 스킬이 목록에 안 뜨는 원인은 확인해 볼 만하다(실제로 필요할 때).

## 관련 문서
- [[에이전트-자동화-도구]] — 스킬 위에서 돌아가는 자동화 기능(workflows·/goal·routines)
- [[Claude-Code-업데이트-동향]] — 스킬·플러그인 기능의 업데이트 출처
- [[내-MCP-커넥터-환경]] — 스킬과 함께 쓰는 MCP 커넥터 환경
- [[delivery-smarthub]] — qa-only를 처음 실전에 쓴 대상(보안 레벨 화면, 2026-11-09~11)
