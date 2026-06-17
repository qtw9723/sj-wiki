---
title: 헤르메스 — Hostinger 기반 개인비서 호스팅
category: 프로젝트
tags: [헤르메스, 개인비서, hostinger, vps, n8n, docker, 자동화, 인프라, 구상, 멀티에이전트]
source: 웹 리서치(2026-06-16) — Hostinger 공식/리뷰 다수(본문 출처 참조)
created: 2026-06-16
updated: 2026-06-16
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

- **헤파이스토스(Hephaestus)** — 생성자: 스펙→코드.
- **모모스(Momus)** — 비평가: 실행 결과 + diff 기반으로 결함 지적·수정안(칭찬 금지, 증거 요구).
- **헤르메스** — 루프 제어: 합격(green)·예산 소진 판단, 사람에게 에스컬레이션.

```
스펙 → [헤파이스토스] 생성 → 검증 하네스(VPS: vitest·tsc·eslint·build)
        ↑ 실패 시 에러+diff → [모모스] 분석·수정안 → 재생성
        └ 통과 → 사람(나) 최종 리뷰 → 머지
```

**원칙(🧠)**: 그라운드 트루스 = 테스트/타입/린트/빌드(LLM 의견 아님). 비평가는 생성자와 **다른 모델·다른 프롬프트**, 반복 상한·비용 예산, 테스트 없으면 모모스가 회귀 테스트 먼저 추가.

**적용 후보(🧠/📄)**: 검증용으로 문서화 잘 된 [[notepad]]부터 테스트 보강 루프 → 더 나아가 "dynamic workflows로 전 프로젝트 일괄 마이그레이션"([[Claude-Code-업데이트-동향]]·[[프로젝트-포트폴리오]])에 생성+검증 루프 적용.

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
