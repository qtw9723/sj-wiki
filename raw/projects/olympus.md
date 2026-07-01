# Olympus (올림푸스) — 로컬 다세션 자율 개발 파이프라인

> 출처: 2026-06~07 대화로 직접 설계·구현. 실물 코드 = `~/IdeaProjects/olympus`, GitHub `qtw9723/olympus`(private).
> 성격: 개인 개발 도구 / 포트폴리오. 회사 기밀 아님.

## 한 줄 정의
**기획서 폴더(`spec/<프로젝트>/`)만 넣고 `bash run.sh` 하면, 여러 Claude Code 세션(기획자·생성자·비평가)이 협업해 스펙을 분석·분해·개발하고, 실행되는 테스트(게이트)가 심판이 되어 완성까지 자동으로 굴리는 로컬 오케스트레이터.**

## 배경 / 동기
- [[헤르메스-개인비서-Hostinger]] §7-2의 "코드 자가개선 루프(생성자↔비평가)" 아이디어를, **헤르메스(클라우드)로 올리기 전에 로컬에서 먼저 검증**하려고 만든 PoC.
- 핵심 통찰: **"LLM 둘이 토론"이 아니라 "실행되는 테스트 위에서 싸우게"** 한다. LLM 합의가 아니라 lint·test·build 결과가 유일한 진실(ground truth).
- 이름 유래: 기획자 **메티스**, 생성자 **헤파이스토스**, 비평가 **모모스**, 루프 제어 **헤르메스** — 이 그리스 신들이 사는 곳이 올림푸스.

## 역할 (다세션)
- **메티스 (Metis) — 기획자/Product Owner, 상시 세션**: 기획서를 **요구사항 분석(필수)**해 `requirements.md`에 의도를 보관(=기억). 작업을 백로그로 분해. 다른 세션의 질문에 답하고, 합리적이면 원안과 달라도 변경을 수용·결정. 범위 밖 결함을 자율 트리아지. brownfield면 기존 코드 먼저 파악.
- **헤파이스토스 (Hephaestus) — 생성자/Builder**: 스펙→코드+테스트. 최소 변경·동작 보존. 의도 모르면 추측 말고 기획자에게 질문(`ask-planner`).
- **모모스 (Momus) — 비평가/Critic**: 결함 검사. 칭찬 금지·증거 요구. verify를 **직접 재실행**(Builder 말 안 믿음, 깨끗한 셸). 심판 무결성 점검.
- **헤르메스 (Hermes) — 라우터**: `run.sh`가 담당. 차례·라운드·예산·질문 라우팅·사람 에스컬레이션.

## 5단계 수명주기
```
spec/<프로젝트>/  ─▶ [메티스] 요구사항 분석(필수) → requirements.md
                      ├─ 진짜 블로커만 → questions.md 쓰고 멈춤(사람)
                      ├─ 그 외 모호함 → 가정으로 진행 + open-questions.md에 누적
                      └─ 분해 → backlog.md + 첫 task.md
      각 작업마다:
   [헤파이스토스] 구현+테스트 ──(의도 모르면)──▶ ask-planner → [메티스]가 답
        ▼  verify.sh(심판: lint·test·build)
   [모모스] 결함검사 + verify 재실행
        ↑ AC 위반 → 헤파이스토스   범위밖 결함 → findings(메티스 트리아지)   결함없음 → green
   green → [메티스] 다음 작업 → … → 전부 done → 사람 최종 승인(전체 1회, 머지)
```

## 핵심 설계 원칙 (실전 검증으로 다듬어짐)
1. **그라운드 트루스 = 실행되는 게이트**. `verify.sh` = 대상 repo의 lint·test·build. LLM 의견 아님.
2. **비대칭 역할**(생성자≠비평가, 다른 모델 권장) — 대등한 둘은 함께 버그를 놓친다.
3. **심판 불가침**: Builder는 verify.sh·lint/test 설정·CI를 수정 금지. 깨지면 ask-planner로 보고(사람/하네스 오너 권한). → 비평가가 diff에 심판 파일이 섞였는지 필수 점검.
4. **자율 결함 트리아지**: 현재 작업 AC 밖에서 발견한 버그는 사람이 아니라 **메티스가** `findings.md`로 받아 백로그 추가/연기/기각을 자율 결정. 사람은 진짜 블로커/보안·스펙 중대위반/최종 승인에만.
5. **작업 단위 승인 없음**: 기획서 전체가 끝난 뒤 **사람 승인 1회**. 모호함은 가정으로 진행하고 끝에 일괄 확인.

## greenfield / brownfield 자동 판단
- `spec/<이름>/` 폴더명 → `$PROJECTS_DIR/<이름>`(기본 `~/IdeaProjects/<이름>`).
- 그 경로가 **없으면 greenfield**: repo 자동 생성(git init) + 범용 게이트(`templates/verify.sh`, py/node 관용형) 설치.
- **있으면 brownfield**: 기존 코드 수정 모드. 안전하게 `olympus/<프로젝트>-<타임스탬프>` **작업 브랜치 자동 생성**(GIT_BRANCH: auto/none/이름). 각 세션에 개발 MODE 주입 → 기존 구조·규약 따르고 동작 보존·기존 테스트 유지.

## 헤드리스 무인 실행
- `bash run.sh` 한 방 — 대상 repo·게이트 지정 불필요(spec 폴더명으로 자동).
- `PERMISSION_FLAG`(무인 시 `--dangerously-skip-permissions`), 실행 로그(`state/runs/`), `turn=human` 자동중단(`pause_if_human`), `AUTO_APPROVE`(최종 승인까지 생략).
- `reset.sh`: 새 작업용 state 초기화. state는 런타임(git 미추적), 도구만 버전관리 → 지속 재사용.
- 기획자 상시성: `--session-id`/`--resume`로 세션 유지(안 되면 durable 파일로 맥락 유지).

## 구성 파일
- `config.sh`(TARGET_REPO·VERIFY_CMD·모델·GIT_BRANCH·권한·예산), `run.sh`(오케스트레이터), `reset.sh`, `templates/verify.sh`(범용 게이트), `roles/{metis,builder,critic}.md`, `spec/<프로젝트>/*.md`(입력), `state/*`(런타임: requirements·backlog·task·ask-planner·findings·questions·open-questions·critic-feedback·verify.txt·handoff.json·runs/).

## 검증 — Mindboard 실전 테스트 (2026-06~07)
파이프라인 검증용으로 **Mindboard**(신규 풀스택 게시판: React+TS 프론트 + FastAPI+SQLite 백엔드, JWT 인증·CRUD·댓글·좋아요·검색·페이지네이션)를 기획서만 넣고 돌림. 결과 T1~T12(+T5.1) 전부 green.
- **백엔드 독립 검증**: 새 리눅스 venv에서 재실행 → ruff clean + **93 passed**. 진짜 green 확인.
- 파이프라인이 **한 단계 위에서** 잡아낸 것들(도구 가치 입증):
  - **심판 조작 시도**(T1: Builder가 verify.sh 수정) → Critic이 포착·에스컬레이션 → "심판 불가침" 규칙 신설.
  - **가짜 green 게이트**(T8: 프론트 `tsc --noEmit`가 무검사 통과) → Critic이 적대적으로 검출(빌드의 `tsc -b`가 실제 커버 확인).
  - **자기 오류 자기정정**(T3: Critic이 자기 T1 판정을 새 증거로 반증 — venv 부트스트랩이 py3.9 사용).
  - **자율 트리아지**(updated_at 버그를 메티스가 T5.1로 스케줄해 사람 없이 수정).
- 남은 사람 결정: liked_by_me 필드(스펙 갭, 계약변경), 반응형 수동 점검(R1) — 둘 다 정당하게 open-questions로 보류.

## 기술 스택 / 방식
- 순수 **bash 오케스트레이션** + **Claude Code CLI 헤드리스(`claude -p`)** 다세션. 외부 의존 없음.
- 언어 무관: 골격 고정, 대상 언어별로 `VERIFY_CMD`/게이트만 교체(어댑터).
- state 파일 공유로 세션 간 통신 → 헤르메스(클라우드)에선 외부 영속 상태(Supabase 등)로 승격 예정.

## 현재 상태 / 다음
- ✅ 로컬 도구로 동작·검증 완료. GitHub `qtw9723/olympus` push.
- ⏸ 헤르메스(클라우드 상시)로는 아직 안 올림 — 당분간 로컬 헤드리스로 사용.
- 다음 후보: Phase 3(요구사항 완료 후 추가기능 제안·교차검증), 게이트 강화(tsc -b), 다중 대상 병행.

## 관련
- [[헤르메스-개인비서-Hostinger]] (§7-2 생성자↔비평가 루프 = Olympus의 씨앗)
- [[notepad]] (초기 로컬 PoC 대상 — vitest 게이트 도입), [[내-프로필]](비개발→개발 전환 포트폴리오)
