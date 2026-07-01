---
title: 헤르메스 — Hostinger 기반 개인비서 호스팅
category: 프로젝트
tags: [헤르메스, 개인비서, hostinger, vps, n8n, docker, 자동화, 인프라, 구상, 멀티에이전트]
source: 웹 리서치(2026-06-16) — Hostinger 공식/리뷰 다수(본문 출처 참조); §7-2 구현현황 = IdeaProjects/dev-pipeline 저장소(2026-06-29~30)
created: 2026-06-16
updated: 2026-07-01
---

> [!tip] 핵심 takeaway
> **헤르메스 = 네 "전반 업무를 다 받는 개인비서" → 핵심 요건은 항상 켜진(always-on) 백엔드 + 스케줄러 + 외부 연동.** 🧠
> 이건 정적 호스팅(공유 호스팅)으로는 안 되고 **Hostinger KVM VPS**가 정답이다(영구 프로세스·cron·custom port·root·Docker). 🧠
> 추천: **KVM2(2 vCPU / 8GB / 100GB NVMe), 24개월** — Docker로 n8n + LLM 에이전트 + 기존 [[mailer]]·[[schedule-reporter-kakao]] 서비스를 한 서버에 올릴 여유. 🧠
> **구조는 하이브리드가 ROI 최고**: 데이터·Auth는 기존 [[parking]](Supabase) 그대로, **Hostinger는 "항상 도는 자동화/에이전트 평면"으로만** 쓴다. 🧠
> ⚠️ 함정 2개: ① **갱신가 폭등**(VPS 약 140~232%↑) → 약정 만료 전 알림 필수, ② **VPS는 셀프 관리**(보안·패치·백업 내 책임) — 다만 네 SM/네트워크 경력([[내-프로필]])이 그대로 강점이 된다. 🧠

---

## 1. 헤르메스가 뭐가 되어야 하나 (요건)

🧠 사용자 확정(2026-06-16): **개인비서로서 "나의 전반적인 업무를 모두 포함"**. 즉 단발 스크립트가 아니라 **상시 가동되는 허브**다. [[내-프로필]]·[[프로젝트-포트폴리오]] 관점에서 필요한 것:

- **Always-on 프로세스**: 알림·감시·에이전트 루프가 24시간 떠 있어야 함 → 영구 실행 필요.
- **스케줄러(cron)**: 일정 리포트·메일 보고서([[mailer]]·[[schedule-reporter-kakao]] 계열)를 시간대별로 실행.
- **외부 연동 다수**: 메일(Gmail/Teams — [[Teams-Gmail-캘린더-Gemini-연동]]), 카카오(캘린더/메모/검색 — [[카카오-Play-MCP]]), 캘린더, TodoMate.
- **LLM 호출 + 메모리**: Claude/Gemini API로 판단·요약, 상태 보존(예정 [[claude-api]]).
- **단일 도메인 게이트웨이**: 여러 사이드 프로젝트를 한 도메인 아래 묶기.

➡️ 🧠 이 요건은 **VPS(루트 + Docker + cron + custom port)**를 요구한다. 공유 호스팅(PHP/정적 위주)으로는 영구 에이전트 프로세스를 못 돌린다.

## 2. Hostinger 가격 (📄 2026-06 기준)

> 📄 모든 가격은 **장기 약정 선결제 기준의 프로모션가**이며, 약정 만료 후 갱신가가 크게 오른다(아래 §4).

| 상품 | 시작가(프로모) | 사양/비고 |
|---|---|---|
| 공유 호스팅(Shared) | $2.69~$2.99/월 | 무료 도메인 1년·SSL·빌더 포함. 📄 **헤르메스 용도엔 부적합**(영구 프로세스 불가) |
| **KVM VPS** | **약 $5~6.49/월~** | 12·24개월 약정. 루트·NVMe·Docker·다중 Node 버전 📄 |
| 클라우드 호스팅 | $7.99/월~ | 관리형 |
| 이메일 호스팅 | $0.39/월/메일박스 (갱신 $1.59) | 📄 |

**KVM VPS 라인업** 📄 ($6.49–$25.99/월 범위, 24개월):

| 플랜 | vCPU | RAM | NVMe | 적합도(🧠) |
|---|---|---|---|---|
| KVM1 | 1 | 4GB | ~50GB | 최소 시작용. n8n 단독은 OK, 여유 적음 |
| **KVM2** ⭐ | **2** | **8GB** | **100GB** | 🧠 **헤르메스 권장** — Docker+n8n+에이전트+여러 Node 서비스 |
| KVM4 | 4 | 16GB | 200GB | 서비스 늘거나 트래픽 생기면 |
| KVM8 | 8 | 32GB | 400GB (32TB BW) | 과사양(현 단계 불필요) |

**공통 포함** 📄: 루트 액세스, NVMe, unmetered 대역폭, 일일 백업, DDoS 방어, Cloudflare CDN, 24/7 라이브챗, **30일 환불보장**(단 VPS 라이선스·도메인·암호화폐 결제는 환불 불가).

**자동화 친화 기능** 📄: **n8n 원클릭 설치 VPS 템플릿**(가격 동일, n8n pre-installed), **hPanel에서 Docker 원클릭 활성화**(컨테이너 네트워킹 사전구성), Node 다중 버전 전환.

## 3. 장점 (📄)

- **가성비**: 동급 VPS 중 공격적 가격(루트 VPS를 월 5~7달러대 시작).
- **성능**: NVMe + unmetered 대역폭, KVM 가상화로 자원 격리.
- **운영 편의**: hPanel + 원클릭 Docker/n8n → 셀프호스팅 진입장벽 낮음.
- **유연성**: 루트·custom port·영구 프로세스·다중 Node 버전 → 에이전트/자동화에 딱.
- **안전망**: 일일 백업·DDoS·Cloudflare CDN·30일 환불보장.

## 4. 단점·함정 (📄 + 🧠 리스크)

- ⚠️ **갱신가 폭등** 📄: VPS 갱신 시 약 **140~232%↑**(공유는 더 심함). 🧠 → 24개월로 길게 잡고, **만료 1개월 전 알림**을 헤르메스 자신에게 등록.
- ⚠️ **셀프 관리(unmanaged)** 📄: 보안 하드닝·패치·업타임·백업이 전부 내 책임. 🧠 단, [[내-프로필]]의 **SM·네트워크·레거시 운영 경력**이 그대로 강점 → 오히려 학습 기회.
- 📄 VPS 약정은 **12·24개월만**(공유의 48개월 같은 장기 락 없음), **갱신 시 쿠폰 적용 불가**.
- 📄 고급 기능(시간당 과금·오토스케일·엔터프라이즈 SLA·고급 네트워킹)은 약함 → 필요하면 DigitalOcean/Vultr가 나음(🧠 현 단계엔 불필요).
- 🧠 VPS 라이선스 환불 불가 → 30일 안에 실제로 헤르메스 PoC를 올려 검증할 것.

## 5. 헤르메스 활용방안 (🧠 — 내 스택에 맞춤)

> 전제: 기존 자산 = [[공통-기술스택]](React19/Vite/Tailwind/Supabase), [[parking]](Supabase 공유 백엔드), 자동화 라인([[mailer]]·[[schedule-reporter-kakao]]), 챗봇 라인([[Cogi-POC-Generator]]).

1. **n8n을 헤르메스의 오케스트레이션 척추로** — Hostinger 원클릭 n8n VPS에 설치. 메일·카카오·캘린더·TodoMate를 노드로 연결해 "수신 → 판단(LLM) → 행동(알림/등록/리포트)" 워크플로를 GUI로 구성. 🧠 [[에이전트-자동화-도구]]의 routine/goal 개념을 실제 상시 서비스로 구현하는 자리.
2. **기존 자동화 라인을 영구 서비스로 승격** — [[mailer]]·[[schedule-reporter-kakao]]의 cron/리포트를 Supabase Edge Function의 시간 제약 없이 VPS의 진짜 cron + 장수명 프로세스로 운영. 🧠 Edge는 단발/경량, VPS는 상시/무거운 작업으로 역할 분담.
3. **LLM 에이전트 컨테이너** — Python/Node 개인비서 에이전트를 Docker로 띄우고 Claude/Gemini API 연동 + 상태(메모리) 영속화. 🧠 [[Cogi-POC-Generator]]에서 익힌 zod 스키마 검증을 LLM 출력 검증에 재사용. (참조 예정 [[claude-api]])
4. **단일 도메인 게이트웨이(Nginx + 무료 SSL)** — [[notepad]]·[[mailer]]·[[Cogi-POC-Generator]]를 한 도메인 서브패스/서브도메인으로 묶어 "표준화된 개인 플랫폼"([[프로젝트-포트폴리오]])을 실제 포트폴리오 URL로 노출. 🧠
5. **하이브리드 아키텍처 고정** — 🧠 **데이터·Auth는 [[parking]](Supabase) 유지(이전 금지)**, Hostinger는 컴퓨트/오케스트레이션 평면만. 정적 프론트(React/Vite)는 Vercel 유지 or Nginx 정적 서빙 중 택1(정적은 VPS 필수 아님).

### 권장 아키텍처 (🧠)

```
            [헤르메스 = Hostinger KVM2 VPS]
            ├─ Docker: n8n (오케스트레이션)
            ├─ Docker: LLM 에이전트 (Claude/Gemini API + 메모리)
            ├─ cron: mailer / schedule-reporter 리포트
            └─ Nginx + SSL: 개인 프로젝트 게이트웨이
                         │  (데이터/Auth)
                         ▼
              [parking = Supabase]  ← 그대로 유지
```

## 6. 실행 체크리스트 (🧠)

- [ ] KVM2 / 24개월 결제 → **약정 만료일을 헤르메스 cron 알림으로 등록**(갱신가 폭등 대비).
- [ ] 30일 환불기간 내 PoC(n8n + 에이전트 1개 워크플로) 올려 검증.
- [ ] 초기 보안: ufw 방화벽 · SSH 키 인증 · fail2ban · 자동 보안 업데이트.
- [ ] 🔒 **회사 기밀 분리**: 헤르메스가 업무 전반을 다뤄도, 사내 AI 챗봇 기밀 설정·자격증명은 이 클라우드 동기화 vault가 아니라 **PC 전용 [[내-프로필]] §회사 / `sj-wiki-work`**에만. (헤르메스 서버의 회사 연동 상세도 work vault로)

## 7. 구상 — 하고 싶은 것 (⚠️ 미구축 / 아이디어 단계)

> [!note] 상태: 구상(want), 아직 안 만듦
> 아래는 **구축한 게 아니라 하고 싶은 방향**이다. 전부 🧠 판단·희망사항이며, 실제 구현·검증된 것은 없다.

### 7-1. 멀티 페르소나 (역할·도구·권한 분리)

헤르메스를 단일 비서가 아니라, **헤르메스가 전문 페르소나들에게 일을 분배하는 오케스트레이터**로 만들고 싶다. 핵심은 말투가 아니라 **역할·도구·권한의 분리**.

- **헤르메스(Hermes)** — 라우터+전령. 입력(카카오/텔레그램) 수신 → 의도 분류 → 적임 페르소나 호출 → 결과 통합·전달(supervisor).
- **이리스(Iris)** — 인박스 트리아지(메일 분류/요약 → 알림·[[mailer]]·TodoMate 분배).
- **므네모시네(Mnemosyne)** — 위키 아키비스트(위키화 + 기밀 자동 판별·라우팅 sj-wiki↔work).
- **클레이오(Clio)** — 동향 큐레이터(크롤링→요약→주간소식 초안, [[웹-크롤링-기초]]).
- **아르고스(Argus)** — 워치독([[parking]]·프로젝트 헬스체크→이상 알림).
- **아테나(Athena)** — 회사 개발 보조(HealthCare). ⚠️ **기밀 경계 안에서 분리 운영**(클라우드 VPS·개인 채널 접근 차단).

**이 설계를 원하는 이유(🧠)**: **페르소나 경계 = 보안 경계**. 아테나만 비동기화·로컬 환경에 가두면 "헤르메스 본체는 회사 기밀에 못 닿는다"가 구조로 강제됨(§1 기밀분리 원칙을 코드로). 부수효과로 각자 최소 권한 자격증명만 보유.

**전제 조건(🧠)**: ① 공유 메모리 = [[parking]](Supabase)로 컨텍스트 파편화 방지, ② 헤르메스→페르소나 핸드오프를 **zod 스키마로 고정**([[Cogi-POC-Generator]] 재사용), ③ 라우팅은 싼 모델·실작업만 좋은 모델.

**리스크(🧠)**: 1인 운영 과설계 위험 → **2명부터**(헤르메스 라우터 + 이리스), 검증되면 증설. 아테나는 맨 마지막에 분리 환경.

### 7-2. 코드 자가개선 루프 (생성자 ↔ 비평가)

코드 작업 시 에이전트가 서로 검증·개선하게 하고 싶다. 단, **"LLM 둘이 토론"이 아니라 "실행되는 테스트 위에서 싸우게"** 하는 게 핵심(LLM끼리는 서로 동의하며 버그를 함께 놓치는 경향).

> [!success] 구현 현황 — 로컬 버전 완성됨 (📄 2026-06-29~30, `IdeaProjects/dev-pipeline`)
> 이 §7-2는 더 이상 순수 구상이 아니다. 헤르메스(VPS)로 올리기 전 단계로, **로컬에서 Claude Code 세션들이 협업하는 범용 오케스트레이터 `dev-pipeline`** 가 실제로 만들어졌다. 아래 "구현 현황" 참조. (멀티 페르소나 §7-1은 여전히 구상 단계)

#### 구현 현황 — `dev-pipeline` (📄 저장소에서 확인)

📄 **정체**: `~/IdeaProjects/dev-pipeline` — "로컬 다세션 개발 루프 (기획자 + Builder↔Critic)". **기획서(`spec/` 폴더 문서들)만 넣으면 알아서 분석·분해·개발**하는 범용 도구. **대상 repo와 분리**돼 있어(`config.sh`의 `TARGET_REPO`) 어떤 repo·언어에도 붙는다. 그라운드 트루스는 LLM 의견이 아니라 **실행 게이트**(`verify.sh` → 대상의 `VERIFY_CMD`).

📄 **역할 매핑** (§7-2 구상 → 실제 구현):
| 구상(위 §7-2) | dev-pipeline 실제 | 소유 상태파일 |
|---|---|---|
| (신규) 기획자/PO | **메티스(Metis)** — 상시 세션, 요구사항 분석·질문응답·**변경 수용·결정** | `requirements.md`(의도=기억)·`decisions.md`·`backlog.md` |
| 헤파이스토스(생성자) | **헤파이스토스(Builder)** — 스펙→코드+테스트, 의도 모르면 질문 | `ask-planner.md` |
| 모모스(비평가) | **모모스(Critic)** — 결함검사·칭찬금지·증거요구, verify 직접 재실행 | `critic-feedback.md`·`findings.md` |
| 헤르메스(루프 제어) | **`run.sh`** — 차례·라운드·예산·질문 라우팅 | `handoff.json` |

🧠 **원래 구상과의 차이**: 3역할(생성/비평/제어) 구상에 **기획자(메티스)를 추가한 4역할**로 진화. 메티스가 "의도의 기억"을 상시 들고 질문에 답하고 **원안과 달라도 합리적이면 변경을 수용**(→ `decisions.md`)하는 게 핵심 보강점.

📄 **5단계 파이프라인** (§7-2 Phase 0~4 구상과 일치): `spec/` → [기획자] 요구사항 분석(`requirements.md`) → 분해(`backlog.md`) → 작업별 [Builder]↔[Critic] 루프(심판=`verify.sh`, green까지) → 다음 작업 → 전부 done → **사람 최종 승인 1회(머지)**. `status`: `pending/needs_clarification/ready/reviewing/needs_intent/green/all_done`.

📄 **모호함 처리 = 자율성**: 진짜 블로커일 때만 `questions.md`로 멈추고, 그 외 모호함은 **합리적 가정으로 진행** + `open-questions.md`에 모아 **끝에 한 번에** 사람에게 물음. Critic이 범위밖 결함을 찾으면 `findings.md`로 자율 트리아지.

📄 **실행 2모드**: (A) `bash run.sh` — 헤드리스 자동실행(6/30 커밋 `e95cbe4`·`a0483c0`: 헤드리스 자동실행 + 자율 결함 트리아지 + 심판 무결성). (B) 수동 다터미널 — 상시 기획자 창을 진짜로 켜둠. 모델: 기획자/비평가 opus-4-8, 생성자 sonnet-4-6(비평가≠생성자 원칙 준수), `MAX_ROUNDS=6`.

📄 **지속 사용 설계**: `state/`는 런타임(git 미추적), **도구(roles·스크립트)만 추적**. `reset.sh`로 초기화 후 새 `spec/`. 대상은 `TARGET_REPO`/`VERIFY_CMD` 환경변수로 그때그때 교체(어댑터). 헤르메스 승격 시 `state/` → Supabase 등 외부 영속 상태로.

📄 **미구현/다음 후보**: **Phase 3**(요구사항 완료 후 추가기능 제안·교차검증)는 아직 미구현 — 다음 확장 후보. 🧠 config.sh 기본 `TARGET_REPO`가 `mindboard`로 지정돼 있어 신규 프로젝트(mindboard) 스캐폴딩에 물려둔 상태로 보인다.

- **헤파이스토스(Hephaestus)** — 생성자: 스펙→코드.
- **모모스(Momus)** — 비평가: 실행 결과 + diff 기반으로 결함 지적·수정안(칭찬 금지, 증거 요구).
- **헤르메스** — 루프 제어: 합격(green)·예산 소진 판단, 사람에게 에스컬레이션.

#### 두 세션 역할 — 비대칭(생성자/비평가) 권장 🧠 (2026-06-29 확정 방향)

"두 세션을 대등하게 둘까, 생성자/비평가로 나눌까"의 답: **비대칭이 낫다.**
- 대등 페어의 약점: 둘 다 "만드는 입장"이라 같은 사각지대에서 같은 버그를 놓침(위 실패 모드).
- 비대칭의 강점: 비평가를 **다른 모델·다른 프롬프트**로 두고 "칭찬 금지·증거(실행결과/diff) 요구" 역할에 고정 → 결함 검출률↑.
- 대등 페어의 유일한 장점(아이디어 다양성)은 아래 **Phase 3(기능 추천)에서만** 부분 채택.

#### 스펙 주도 전체 수명주기 (5단계) 🧠

사용자 요구 = "기획서 넣으면 LLM이 자체 확인하며 개발 → 두 세션이 교차검증·수정 → 요구사항 전부 끝나면 추가 기능 추천 → 서로 검증 후 좋으면 추가 개발". 이를 5단계로 고정:

- **Phase 0 — 스펙 인테이크**: 비평가가 *스펙 자체*를 먼저 리뷰(모호·누락·모순 지적) → 작업 목록 + 각 작업의 **수용 기준(acceptance criteria)**으로 분해. 이 기준이 나중에 "다 됐는지" 판정하는 체크리스트가 됨.
- **Phase 1 — 빌드 루프(작업 단위 반복)**:

```
작업 → [헤파이스토스] 코드 생성 → 검증 하네스(test·type·lint·build 자동 실행)
        ↑ 실패: 에러+diff → [모모스] 결함 분석·수정안 → 재생성
        └ 통과(green) → 다음 작업
```

  테스트가 없으면 모모스가 **회귀 테스트부터** 추가. 통과/탈락은 LLM 의견이 아니라 실행 결과가 결정.
- **Phase 2 — 수용 검증**: Phase 0 체크리스트로 "스펙 ↔ 구현" 갭 대조. 비평가가 빠진 요구사항을 잡아 Phase 1로 환류. 전부 충족 시 진행.
- **Phase 3 — 기능 추천(여기서만 대등 모드)**: 두 세션이 각자 자유롭게 추가 기능 후보 제안 → 서로 교차평가(가치·리스크·구현비용) → 합의된 것만 추림. **반드시 사람(나) 승인 게이트**(자동 무한 증식 = scope creep 방지).
- **Phase 4 — 승인분 재투입**: 내가 승인한 항목만 Phase 1 루프로 재개발·재검증.

#### 반드시 넣을 통제장치 🧠

- **사람 승인 게이트 2곳**: (a) 머지 직전, (b) Phase 3 기능 추가 직전.
- **예산·반복 상한**: 작업당 재시도 N회·토큰/비용 한도. 초과 시 헤르메스가 사람에게 에스컬레이션.
- **다른 모델·다른 프롬프트**: 생성자/비평가 분리(동일 모델 금지).
- **외부 상태/메모리**: 진행상태를 [[parking]](Supabase) 등 외부에 영속화 → 세션이 죽어도 이어감.
- **핸드오프 스키마 고정**: 세션 간 메시지를 zod 스키마로 검증([[Cogi-POC-Generator]] 재사용).

#### 언어 무관(범용) 만들기 🧠

파이프라인 골격(생성↔비평↔검증)은 고정하고 **검증 하네스만 프로젝트 언어로 교체(어댑터)**:
- JS/TS: `vitest + tsc + eslint + build`
- Python: `pytest + mypy + ruff`
- 그 외: 각 언어의 test/lint/build

즉 "어댑터만 갈아끼우는" 구조로 추상화하면 언어 무관 범용 파이프라인이 된다.

**원칙(🧠)**: 그라운드 트루스 = 테스트/타입/린트/빌드(LLM 의견 아님). 비평가는 생성자와 **다른 모델·다른 프롬프트**, 반복 상한·비용 예산, 테스트 없으면 모모스가 회귀 테스트 먼저 추가.

**적용 후보(🧠/📄)**: 검증용으로 문서화 잘 된 [[notepad]]부터 테스트 보강 루프 → 📄 실제로 notepad에 **vitest + `verify`(lint&&test&&build) 게이트가 추가됨**(2026-06-29) = dev-pipeline의 `VERIFY_CMD` 대상으로 준비 완료. 🧠 더 나아가 "dynamic workflows로 전 프로젝트 일괄 마이그레이션"([[Claude-Code-업데이트-동향]]·[[프로젝트-포트폴리오]])에 생성+검증 루프 적용.

**현실 경고(🧠)**: 이건 에이전틱 코딩(예: Claude Code) + 강한 CI가 이미 하는 일. 먼저 **기존 도구 + 강한 테스트/타입/린트**로 같은 효과를 보고, 그래도 부족한 "상시 자동 개선"만 헤르메스 루프로 떼어내는 게 ROI 우선.

## 의외의 연결점 (🧠)

- 헤르메스 VPS는 [[내-프로필]]의 두 경력선을 합류시킨다: **SM/인프라(서버 운영)** + **NLP/LLM(에이전트)**. 즉 "비개발 → 개발 전환"의 가장 강한 포트폴리오 한 방이 될 수 있다.
- [[mailer]]·[[schedule-reporter-kakao]]가 이미 "메신저(전령)" 성격 → 헤르메스(Hermes=전령신)는 이들을 **하나의 비서로 통합**하는 상위 레이어로 자연스럽게 자리한다.

## 관련 문서

- [[index]] · [[내-프로필]] · [[프로젝트-포트폴리오]] · [[공통-기술스택]]
- [[parking]] · [[mailer]] · [[schedule-reporter-kakao]] · [[Cogi-POC-Generator]]
- [[에이전트-자동화-도구]] · [[내-MCP-커넥터-환경]] · [[카카오-Play-MCP]] · [[Teams-Gmail-캘린더-Gemini-연동]]
- 작성 예정: [[claude-api]]

## 출처 (📄 웹, 2026-06-16)

- Hostinger Pricing 2026 (websitebuilderexpert): https://www.websitebuilderexpert.com/web-hosting/hostinger-pricing/
- Hostinger Pricing 2026 (cybernews): https://cybernews.com/best-web-hosting/hostinger-review/pricing/
- Hostinger Node.js Hosting Review (hostadvice): https://hostadvice.com/hosting-company/hostinger-reviews/hostinger-nodejs-hosting-review/
- Node.js on Hostinger VPS — Practical Guide (brandrums): https://www.brandrums.com/blog/host-nodejs-app-hostinger-vps-2026/
- Hostinger n8n Hosting Review (hostadvice): https://hostadvice.com/hosting-company/hostinger-reviews/hostinger-n8n-hosting-review/
- Hostinger VPS Pricing & Real Renewal Costs (hostadvice): https://hostadvice.com/hosting-company/hostinger-reviews/vps-pricing/
- Hostinger Pricing Plans 2026 (googiehost): https://googiehost.com/blog/hostinger-pricing-plans/
