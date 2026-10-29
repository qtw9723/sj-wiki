---
title: Jev (TypeSafe AI) — System One 의사결정 모델
category: 개념 / 지식
tags: [jev, typesafe-ai, system-one, 의사결정모델, 분류, 라우팅, 가드레일, llm대안, 저비용모델, 제브]
source: raw/jev-typesafe-crawl-2026-10-29.md (datanorth.ai · gigazine · docs.typesafe.ai · arXiv 2609.30216 · Bloomberg 등 2026-10-29 크롤링), raw/ai-digest/naver-2026-09-21.md, raw/ai-digest/naver-2026-09-24.md, raw/ai-digest/naver-2026-10-05.md
created: 2026-10-29
updated: 2026-10-29
---

> [!tip] 핵심 takeaway
> 🧠 Jev는 **"글을 쓰는 AI"가 아니라 "고르는 AI"** 다. 질문과 선택지를 주면 텍스트 대신 **선택·점수·0~1 확률 + confidence**만 돌려준다. LLM 대체가 아니라 **LLM 앞단의 판단 레이어**(라우팅·분류·가드레일·에스컬레이션)용.
> 🧠 네 작업에 바로 대응되는 자리: 챗봇의 **인텐트/미응답 분류·긴급도 판정**, [[CogInsight-Generator]] Stage1(입력 분류·라우팅), RAG([[rag-compare]]) 검색결과의 관련성·인젝션 필터. 공부 순서는 **§3 API 3종 → §5 confidence 임계값 패턴 → §6 한계**면 충분.
> ⚠ 성능 수치는 거의 전부 **TypeSafe 자체 측정**이다. 독립 벤치마크 없음 → 쓰려면 내 데이터로 eval부터.

## 1. 한 줄 정의
📄 TypeSafe AI가 2026-09-15 공개한 **System One 모델** 패밀리의 첫 모델. 개발자가 *결정 질문 + 가능한 출력*을 정의하면, Jev가 **Choice(선택) / Noul(예·아니오) / Score(등급)** 결과를 반환한다. (datanorth, arXiv 2609.30216)

- 📄 이름 유래: 카너먼의 **System 1(빠른 직관) / System 2(느린 숙고)**. Jev = 빠른 직관 판단 담당, LLM = 추론·글쓰기 담당으로 짝지어 쓰는 구조를 의도.
- 📄 TypeSafe 표현: *"작은 모델도 아니고 LLM도 아니다"* — 차이는 크기가 아니라 **목적과 출력 형태**.
- 📄 한국 보도에선 **"제브"** 로 표기(AI타임스 2026-10-05, 조선 IT 2026-09-24).

## 2. 어떻게 동작하나 (LLM과의 차이)
| 구분 | LLM (+JSON 모드) | Jev |
|---|---|---|
| 출력 | 토큰을 순차 생성 → 파싱 | 사전 정의 구조로 **한 번에** 출력 📄 |
| 형식 보장 | JSON 모드는 형식만 맞춤 | 처음부터 구조화 결정용으로 학습 📄 |
| 확신도 | 별도 추정 필요 | 모든 출력에 확률·confidence 📄 |
| 설명 | 가능 | **불가** (이유를 글로 못 씀) 📄 |

- 📄 내부: 신규 아키텍처 + **parallel sampler** + 학습법 **RLCD**(Reinforcement Learning for Calibrated Decisions). 약 2년 스텔스로 개발(CEO 발언, GIGAZINE). 아키텍처 세부는 비공개.
- 🧠 기존 대안과 비교하면: 지도학습 분류기(라벨 데이터·재학습 필요)와 LLM(제로샷이지만 느리고 비쌈) 사이의 빈칸을 노린 것 — arXiv 논문도 같은 틀로 설명(📄).

## 3. API 구조 (공식 문서)
📄 `POST https://api.typesafe.ai/v1/systemone` · `Authorization: Bearer $TYPESAFE_API_KEY`
📄 SDK: `pip install typesafe-sdk`(Py 3.10+) / `npm install @typesafe-ai/sdk`(Node 20+)

요청 = **state**(판단 대상: 문자열·JSON·텍스트 배열) + **questions**(여러 개, 타입 혼합 가능). 📄 각 질문은 같은 state에 대해 **병렬·서로 독립**으로 평가된다.

```json
{
  "state": "결제했는데 3일째 배송이 안 와요. 오늘 안 오면 취소할게요",
  "model": "jev-latest",
  "questions": {
    "urgent":   { "type": "noul",   "instructions": "The message conveys urgency" },
    "category": { "type": "choice", "options": ["배송", "결제", "환불", "기타"] },
    "anger":    { "type": "score",  "levels": ["차분", "약간 불만", "불만", "격앙"] }
  }
}
```
*🧠 위 예시는 이해용으로 재구성(필드명 `options`·`levels`는 추정, 공식 스키마는 API Reference 확인). 📄 공식 예시는 `urgent` noul 하나.*

📄 응답 예(공식): `{"model":"jev-1.13.0","answers":{"urgent":{"type":"noul","noul":0.99}},"usage":{...}}` — `jev-latest` 별칭을 쓰면 실제 버전이 응답에 찍힌다.

| 타입 | 용도 | 반환 | 제약 |
|---|---|---|---|
| **Choice** | N개 중 하나 고르기 | choice, probabilities, confidence | 옵션 최대 255개 📄 |
| **Score** | 순서 있는 루브릭 등급 | score(level·legend), probabilities, confidence | 2~10단계 📄 |
| **Noul** | 예/아니오 | 0~1 단일 값 | — |
| **Box** (1.14 실험) | 이미지 바운딩박스 | — | danger-zone 헤더 필요 📄 |

📄 한도: 요청당 64k 토큰(state 32k + 최장 질문), 250,000 tok/s, 1,200 req/min(동적). 롱컨텍스트 실험 시 262k.

## 4. 가격·속도 (⚠ 대부분 벤더 주장)
- 📄 입력 **$0.042 / 1M 토큰**, 출력 **무료**. 이미지도 입력 토큰으로 과금.
- 📄 지연 70~500ms(TypeSafe 노트북 측정), "40~200배 빠름"(다른 발표 20~200 / 40~400배).
- 📄 자사 워크플로 eval: **193.6배 빠름 · 444.6배 저렴**. 홈페이지 데모: Jev 0.114s/$0.000081 vs LLM 8.566s/$0.013880.
- 📄 GIGAZINE: GPT-5.6 Terra 품질을 약 1/100 비용, 툴콜 오류율 0%. DOOM 플레이 데모 초당 ~10콜·시간당 ~$7.
- 📄 ZDNet(W39 수집): Claude Sonnet 5 67.8% · GPT-5.6 Sol 74.1% · Opus 5 73.1%와 비교, **건당 0.0004달러**. ⚠ 평가 항목·방법론 불명.
- ⚠ 📄 **"Zero Hallucinations"는 출력 *형태* 보증이지 정답 보증이 아니다**(TypeSafe FAQ: *"guarantees the shape of its answers, not that every decision is correct"*). 홍보 그래프의 환각 0%는 실측치 아님(datanorth).

## 5. 활용 패턴 (공식·리뷰 사례)
- 📄 **모델 라우팅**: 의도·난이도 분류 → 작은 모델 / 프론티어 모델로 분기.
- 📄 **툴 선택**: 고정된 툴 목록을 Choice로.
- 📄 **가드레일**: Noul·Score로 메시지 검사(탈옥 시도 0.74 → 차단 예).
- 📄 **RAG 패시지 평가**: 관련성·사용가능성·모순·인젝션을 프롬프트 투입 전 채점(심어둔 공격 인젝션 0.99 탐지 예).
- 📄 **티켓 분류**: 카테고리·심각도·재현성·불만도를 한 요청에.
- 📄 **사람 에스컬레이션 (confidence 임계값)**:
  - `> 0.85` 자동 처리 / `0.6 ~ 0.85` 사용자에게 확인 / `< 0.6` 사람에게 이관 / 파괴적 작업은 `> 0.9` 요구
- 📄 confidence 계산: 확률분포 모양에서 도출. 3지선다면 `(3 × 최대확률 − 1) / 2` → 균등분포 0, 확정 1.
- 📄 설계 원칙(공식): **질문 하나 = 구체적 판단 하나**. 다요인 판단(예: 시장성·기술 실현성·차별성)은 각각 따로 물어보고 **가중 합산은 코드에서**.

## 6. 한계 — 쓰기 전 체크리스트 (📄 datanorth·공식)
- 텍스트 생성·이유 설명·코드 작성 **불가** → 설명이 필요하면 LLM과 2단 구성.
- **산술·카운팅·날짜 비교는 코드로**(날짜를 순서값이 아닌 텍스트로 읽음).
- state에 **무관한 내용이 섞이면 정확도 하락** → 넣기 전에 필터링.
- 멀티홉 추론·**이중부정**에 약함.
- 입력을 기본적으로 적대적으로 보지 않음 → 인젝션 방어는 명시적 기준+테스트.
- **비결정적**(동일성 대신 "비슷한 의미 → 비슷한 결정" 일관성 우선).
- 공개 벤치마크 없음, 독립 평가 없음 → **calibration**(confidence 0.9가 실제 90% 맞나) 검증이 핵심.
- 📄 개발자 우려: 선택 이유를 안 알려줘서 엔터프라이즈 감사·디버깅이 어렵다(levelup 기고).

## 7. 생태계 (arXiv 2609.30216 "Jev in the Wild", 2026-09-22 스냅샷)
- 📄 출시 1주 만에 GitHub 공개 프로젝트 **2,170개**(신규 1,865 + 기존 레포 통합 305), 스타 43,750.
- 📄 인터페이스 사용률: **Choice 81.0% · Noul 72.2% · Score 45.4%**, 셋 다 쓰는 곳 36.8%.
- 📄 결정 목적: **속성 판단 77%** · 점수/순위 52% · 행동 선택 31% · 결과 판단 20% · 콘텐츠 필터링 15% · 모델/툴 선택 13%. 69.7%가 2개 이상 목적에 사용.
- 📄 관심(스타)은 **라우팅·자동화(41.4%)** 와 인터페이스 에이전트에 쏠림 — 프로젝트 수 19.6%로 스타 63.0%. 게임·시뮬레이션(DOOM, 마리오)도 프로젝트 수는 많음(10.5%).
- 📄 파생 연구: Jev-mem(에이전트 메모리 제어), **Jev-as-a-judge**(확신 시 수용·불확실 시 에스컬레이트), 6G 엣지 오케스트레이션의 LLM 대체, 텍스트 주석 평가.
- 📄 도구: **Jevkit**(Jev를 CLI·MCP로 에이전트에 노출), LiteLLM 지원, browser-use "Jev ultra-fast".
- ⚠ 논문 한계: 1주 스냅샷·공개 레포만, 라벨링을 GPT 에이전트가 수행.

## 8. 회사·버전 타임라인
| 날짜 | 사건 |
|---|---|
| 2024 | 📄 TypeSafe AI 설립 — CEO **Diogo Almeida**(전 OpenAI, ChatGPT 개발 참여), Sasha Sheng, Erik Gafni (직함은 출처마다 상이) |
| 2026-09-15 | 📄 System One Models + **Jev 1.13** 공개, Early Access, 시드 $40M(DCVC 리드) |
| 2026-09-20~24 | 📄 국내 보도: "역사상 가장 빠르게 사용량이 증가한 유료 모델" |
| 2026-10-14 | 📄 **Jev 1.14** — 실험 기능(danger zone): 이미지 입력·Box 타입·롱컨텍스트 262k. 프로덕션 비권장 |
| 2026-10 | 📄 Bloomberg: a16z 리드 약 **$870M, 기업가치 $7.5B** (라운드 명칭은 출처 간 불일치) |
| 이후 | 📄 경쟁 결정모델 등장: Cloudflare Clef, Microsoft-Decision-1, this-that-model-1.0(30ms) |

> ⚠ **표기 혼동 정정**: [[AI-주간-소식-2026-W39]] (KR-W39-102) *"제브(Zeb)"* 는 별개 모델이 아니라 **Jev와 같은 모델**이다. 🧠 근거: 수치(70~500ms·$0.042)가 Jev 공식 수치와 정확히 일치, 한국어 "제브" = Jev(AI타임스 표기). 원 기사가 영문을 Zeb로 오기한 것으로 판단.

## 9. 의외의 연결점 / 제안 (🧠 판단)
- 🧠 **챗봇 미응답 처리·인텐트 분류 같은 "판정" 업무는 Jev 모양 그대로**다: 인텐트 목록 = Choice 옵션, "미응답인가" = Noul, 심각도 = Score. 단, 업무 데이터는 외부 API 전송 이슈가 먼저.
- 🧠 [[CogInsight-Generator]] 기존 결론(*"모델 단가 추격보다 호출 설계가 먼저"*)과 충돌하지 않는다 — Jev는 **"작은 판단자를 앞에 세우고 확신 없을 때만 큰 모델"** 구조(카이스트 갈래)의 *판단자 후보*로 보는 게 맞다. §5의 confidence 3단 임계값이 그 구조의 구체적 레시피.
- 🧠 [[rag-compare]]에 "검색결과 패시지 관련성 Score" 칼럼을 붙이면 store 비교를 사람 눈 대신 수치로 할 수 있다(실험 소재).
- 🧠 학습용 첫 실습: Early Access 키 → 내 개인 데이터(예: AI 주간 소식 기사 제목)로 Choice 분류 50건 → 사람 라벨과 비교해 **confidence별 정답률(calibration)** 직접 그려보기.

## 출처
- 📄 [DataNorth — Jev: what it is and why it matters](https://datanorth.ai/blog/jev-what-it-is-and-why-this-new-model-matters)
- 📄 [GIGAZINE (2026-09-16)](https://gigazine.net/gsc_news/en/20260916-system-one-jev)
- 📄 [TypeSafe 공식 문서](https://docs.typesafe.ai) · [Quick Start](https://docs.typesafe.ai/introduction/quickstart.md)
- 📄 [arXiv 2609.30216 — Jev in the Wild](https://arxiv.org/pdf/2609.30216)
- 📄 [Bloomberg Gov — a16z backs Jev maker at $7.5B](https://news.bgov.com/private-equity/andreessen-horowitz-backs-jev-maker-at-7-5-billion-value) · [Dealroom](https://app.dealroom.co/companies/typesafe_ai_jev)
- 📄 [AlternativeTo — Jev 1.14](https://alternativeto.net/news/2026/10/typesafe-ai-ships-jev-1-14-with-new-box-type-composable-images-and-longer-context-length/) · [Pillitteri — 1.14 프로덕션 경고](https://pasqualepillitteri.it/en/news/26048/jev-1-14-image-input-box-typesafe-warns)
- 📄 [Jevkit (MCP)](https://mcpmarket.com/server/jevkit) · [The Risks of Using JEV AI in Enterprise Software](https://levelup.gitconnected.com/the-risks-of-using-jev-ai-in-enterprise-software-5d39ffc72842)

## 관련 문서
- [[AI-주간-소식-2026-W39]] — 최초 수집(KR-W39-15 Jev, KR-W39-102 "Zeb" = Jev)
- [[AI-주간-소식-2026-W41]] — "제브(Jev)" 재등장, 개발자명
- [[CogInsight-Generator]] — §비용 축: 단가 갈래 vs 호출 횟수 갈래
- [[공통-기술스택]] — 에이전트 운영 비용식
- [[rag-compare]] — 패시지 관련성 채점 실험 후보
- [[GLM-Zhipu-Z-ai]] — 다른 저비용 모델 축(생성형)
- [[내-MCP-커넥터-환경]] — Jevkit MCP 후보
