---
title: 올림푸스 GLM 백엔드 연동 (구현 역할 오프로드)
category: 프로젝트
tags: [올림푸스, glm, z-ai, claude-code, 비용절감, 구현가이드]
source: "올림푸스 repo(~/IdeaProjects/olympus) config.sh·run.sh·resilience.sh 직접 확인, docs.z.ai/devpack/tool/claude (2026-07-07)"
created: 2026-07-07
updated: 2026-07-07
---

> [!tip] 핵심 takeaway
> **목표**: 예산 월 ~$20(=Claude Pro) 유지하면서 [[올림푸스-Olympus]]의 토큰·캡 문제 해결.
> **전략**: 토큰 잡아먹는 **빌더(구현) 역할만 GLM(z.ai)으로**, **설계(메티스)·비평(모모스=critic)은 Claude Pro 그대로**. **verify.sh 심판 게이트**가 있어 구현 모델이 싸도 최종 품질이 방어된다.
> **변경 규모**: `config.sh` 3줄 + `run.sh` `worker()` 몇 줄 + `.env.local` 1줄. 되돌리기 쉬움.

## 0. 왜 이렇게 되나 (📄 repo 확인)
📄 올림푸스는 역할을 **순차 실행**하고, 각 역할은 **별도 `claude -p` 서브프로세스**다(`run.sh`):
- 설계 = `metis()` → 항상 `$PLANNER_MODEL`(Claude Opus)
- 구현 = `worker(builder.md, $BUILDER_MODEL)` ← **여기만 GLM으로 교체**
- 비평 = `worker(critic.md, $CRITIC_MODEL)` → Claude Opus 유지
- 루프: `metis M0 → {builder → verify.sh → critic} ×MAX_ROUNDS → metis M2`

📄 Claude Code는 **프로세스 단위로 env(`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`)를 읽는다**. 각 역할이 독립 프로세스이므로, **빌더 서브셸에만 z.ai env를 주입**하면 그 호출만 GLM으로 가고 나머지는 Claude Pro 로그인(OAuth)을 그대로 쓴다. 🧠 → 역할별 백엔드 분리가 깨끗하게 됨.

## 1. 사전 준비
1. **z.ai 계정 + API 키 발급**: https://z.ai (또는 bigmodel.cn). API Key 하나 생성.
2. **모델 결정**:
   - 무료 노림: `glm-4.5-flash` / `glm-4.7-flash` (⚠ 아래 §4에서 **무료가 이 엔드포인트로 되는지 반드시 테스트**)
   - 확실한 초저가: `glm-4.6` (입력 $0.6 / 출력 $2.2, run당 ≈$9.5 — [[GLM-Zhipu-Z-ai]] §4.6)
   - 품질 우선: `glm-5.2`(플래그십, $1.4/$4.4)
   - 🧠 **권장 시작점: `glm-4.6`** (무료 여부 불확실성 없이 바로 저비용). 안정화 후 flash 테스트로 무료화 시도.

## 2. `.env.local` 에 키 추가 (gitignore됨)
📄 `config.sh`가 `.env.local`을 `set -a`로 로드하므로 여기 넣으면 자동으로 env에 뜬다.
```bash
# ~/IdeaProjects/olympus/.env.local  (커밋 금지 — 이미 gitignore)
ZAI_API_KEY=여기에_z.ai_API키
```

## 3. `config.sh` 수정 (3줄)
```bash
# (기존) BUILDER_MODEL="${BUILDER_MODEL:-claude-sonnet-4-6}"
BUILDER_MODEL="${BUILDER_MODEL:-glm-4.6}"          # ← 구현 역할을 GLM으로

# z.ai Anthropic-호환 엔드포인트 (추가)
ZAI_BASE_URL="${ZAI_BASE_URL:-https://api.z.ai/api/anthropic}"
# ZAI_API_KEY 는 .env.local 에서 로드됨 (여기 하드코딩 금지)
```
> 🧠 `PLANNER_MODEL`·`CRITIC_MODEL`은 **건드리지 않는다**(Claude Opus 유지 = 설계/심판 품질 보존).

## 4. `run.sh` `worker()` 수정 — 모델명으로 자동 라우팅
📄 현재:
```bash
worker () {
  ( cd "$TARGET_REPO" && claude_guarded -p "$(worker_prompt "$1")" \
      --add-dir "$PIPELINE_DIR" --model "$2" $PERMISSION_FLAG )
}
```
🧠 변경 — 모델명이 `glm-`으로 시작하면 그 서브셸에만 z.ai env 주입:
```bash
worker () {
  ( cd "$TARGET_REPO"
    case "$2" in
      glm-*)
        export ANTHROPIC_BASE_URL="$ZAI_BASE_URL"
        export ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY"
        export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1   # z.ai키로 Anthropic 배경호출 실패 방지
        export API_TIMEOUT_MS="${API_TIMEOUT_MS:-3000000}"  # 긴 작업 타임아웃 여유
        ;;
    esac
    claude_guarded -p "$(worker_prompt "$1")" \
      --add-dir "$PIPELINE_DIR" --model "$2" $PERMISSION_FLAG )
}
```
- `export`가 **서브셸 `( … )` 안**이라 이 호출에만 적용 → `metis()`·critic(claude-opus) 무영향. ✅
- `critic`도 `worker()`를 쓰지만 `$CRITIC_MODEL=claude-opus-4-8`이라 `glm-*` 케이스에 안 걸림 → Claude 유지.

## 5. 무료 Flash 검증 (⚠ 미확인 — 개발 전 필수 확인)
🧠 docs.z.ai의 Claude Code 연동은 **Coding Plan(유료) 기준**으로 쓰여 있고, **무료 Flash가 이 Anthropic-호환 엔드포인트로 $0에 되는지는 공식 확인 안 됨**. 개발 착수 전 1회 테스트:
```bash
source ~/IdeaProjects/olympus/.env.local
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic \
ANTHROPIC_AUTH_TOKEN="$ZAI_API_KEY" \
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 \
claude -p "1+1은?" --model glm-4.5-flash
```
→ 응답 오면 z.ai 대시보드에서 **청구 발생 여부 확인**.
- 무료 확인되면 → `BUILDER_MODEL=glm-4.5-flash`(또는 `glm-4.7-flash`)로 바꿔 **완전 무료 구현**.
- 무료 안 되거나 품질 부족 → `glm-4.6` 유지(초저가). 이게 안전한 기본값.

## 6. 검증 & 롤백
- **1 실행 돌려보기**: `bash run.sh` — 라운드 로그에 `BUILDER (glm-4.6)` 뜨는지, 빌더가 실제로 코드 쓰고 `verify.sh` 통과하는지 확인.
- **품질 급락 시**: `MAX_ROUNDS`가 흡수(빌더가 못 하면 라운드 소모↑) → 심판이 계속 reject하면 빌더만 `glm-5.2`로 승급하거나 롤백.
- **롤백**: `config.sh`에서 `BUILDER_MODEL=claude-sonnet-4-6`로 되돌리면 끝(`glm-*` 아니면 라우팅 자동 해제).

## 7. 기대 효과 (🧠)
- **비용**: 구현 역할(가장 토큰 많음)이 Claude Pro 한도에서 빠짐 → Pro는 설계/심판 경부하만 담당 → **월 $20 유지하며 캡 벽 완화**. GLM은 glm-4.6이라도 run당 ≈$9.5, flash면 ≈$0.
- **캡**: Claude Pro의 주당 Opus시간 소비가 크게 줄어 무인 장시간 실행이 벽에 덜 부딪힘. (`TOKEN_WAIT` 자동 대기는 그대로 안전망)
- **품질**: verify.sh 게이트가 최종 판정 → 싼 구현 모델도 "통과할 때까지" 돌아 결과 품질 보장.
- ⚠ **회사 코드**가 대상이면 중국 모델 데이터 반출 이슈 → [[GLM-Zhipu-Z-ai]] §6 거버넌스 확인 먼저. 개인 프로젝트는 바로 적용 가능.

## 관련 문서
- [[올림푸스-Olympus]] — 파이프라인 전체 구조(4역할·verify.sh 심판)
- [[올림푸스-실행-런북]] — 실행 시 세팅 체크리스트(이 연동도 여기 env와 함께 관리)
- [[GLM-Zhipu-Z-ai]] — 모델·요금·예산해법(§4.5~4.7)의 근거
