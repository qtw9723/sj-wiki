---
title: Jev (TypeSafe AI) 웹 크롤링 원본 메모
collected: 2026-10-29
method: Claude Code WebSearch + WebFetch (요약 추출본, 원문 전문 아님)
---

# 출처별 추출 사실

## 1. DataNorth — "Jev: What it is and why this new model matters"
URL: https://datanorth.ai/blog/jev-what-it-is-and-why-this-new-model-matters
- TypeSafe AI가 2026-09-15 출시, 당시 버전 1.13. "System One" 모델(카너먼 System 1/2 비유) — 소프트웨어 안의 결정을 위한 새 모델 클래스.
- 텍스트 생성 X, 사용자가 정의한 옵션 중 선택. "작지도 않고 LLM도 아니다"(TypeSafe). 신규 아키텍처 + parallel sampler + 학습법 RLCD(Reinforcement Learning for Calibrated Decisions).
- 호출 = state(문자열/JSON/텍스트 배열) + questions. 질문들은 같은 state에 대해 병렬·독립 평가.
- 질문 3종: Choice(최대 255개 옵션 중 1, option·probabilities·confidence) / Score(2~10단계 루브릭, level·legend·probabilities·confidence) / Noul(예/아니오, 0~1 단일값).
- confidence = 확률분포 모양에서 산출. 3지선다 예: (3×최대확률−1)/2.
- 한도: 요청당 64k 토큰(state 32k + 최장 질문), 250,000 tok/s, 1,200 req/min(동적 조정).
- 각 질문은 "직감 판단" 단위. 다단계 추론은 여러 질문으로 쪼개고 코드에서 결합.
- 공개 벤치마크 점수 없음, 자체 eval 권장. 지연 70~500ms(TypeSafe 노트북 측정). 40~200배 빠름 주장. 자사 워크플로 eval 193.6배 빠름·444.6배 저렴. 홈페이지 데모: Jev 0.114s/$0.000081 vs LLM 8.566s/$0.013880.
- 가격: 입력 $0.042 / 1M 토큰, 출력 무료.
- 한계: 텍스트 생성·설명·코드 불가 / 산술·카운팅은 코드로 / 날짜를 텍스트로 읽음(비교는 코드로) / state에 무관한 내용 섞이면 정확도 하락 / 멀티홉·이중부정 약함 / 기본적으로 데이터를 적대적으로 보지 않음 / 비결정적(일관성 우선) / "Zero Hallucinations"는 출력 형태 보증이지 정답 보증 아님(FAQ).
- 활용: 모델 라우팅, 툴 선택, 가드레일(탈옥 0.74로 차단 예), RAG 패시지 평가(인젝션 0.99 탐지 예), 티켓 분류(카테고리·심각도·재현성·불만도 한 번에), 사람 에스컬레이션(>0.85 자동, 0.6~0.85 사용자 확인, <0.6 사람, 파괴적 작업은 >0.9).
- 미해결: 독립 평가 없음. calibration(0.9 confidence가 실제 90% 맞는지) 검증 필요.

## 2. GIGAZINE (2026-09-16)
URL: https://gigazine.net/gsc_news/en/20260916-system-one-jev
- 2026-09-15 "System One Models" 패밀리와 첫 모델 Jev 발표. CEO Diogo Almeida = ChatGPT 개발 참여 연구자.
- 순차 토큰 생성 아님, 사전 정의 구조로 결과를 한 번에 출력. 약 2년 스텔스로 RLCD 개발.
- 속도 20~200배(또 다른 주장 40~400배). GPT-5.6 Terra 품질을 약 1/100 비용으로(그래프). 툴콜 오류율 0%. 모든 출력에 confidence.
- 데모: 위키피디아 링크 레이스, DOOM 플레이(초당 ~10콜, 시간당 ~$7).
- 출시 시 Early Access 신청. 문서 docs.typesafe.ai.
- 후속: Jev 1.14(이미지·롱컨텍스트), 경쟁 결정모델(Cloudflare Clef, Microsoft-Decision-1).

## 3. 공식 문서 docs.typesafe.ai (Introduction + Quick Start)
- POST https://api.typesafe.ai/v1/systemone, Authorization: Bearer <API_KEY>, env TYPESAFE_API_KEY.
- SDK: pip install typesafe-sdk (Py 3.10+) / npm install @typesafe-ai/sdk (Node 20+).
- 요청 예: {"state": "...", "model": "jev-latest", "questions": {"urgent": {"type": "noul", "instructions": "The message conveys urgency"}}}
- 응답 예: {"model": "jev-1.13.0", "answers": {"urgent": {"type": "noul", "noul": 0.99}}, "usage": {...}}
- jev-latest 별칭, 응답에 실제 버전 표기. 한 요청에 질문 타입 혼합 가능.
- 베스트 프랙티스: 질문 하나 = 하나의 구체적 판단. 다요인 판단은 쪼개서 코드에서 가중 결합.

## 4. arXiv 2609.30216 "Jev in the Wild" (Ling·Xue·Ye, 2026-09-24, cs.SE)
- 2026-09-22 기준 GitHub 공개 Jev 프로젝트 2,170개 분석. 출시 1주 만에 신규 1,865개 + 기존 305개 통합, 스타 43,750.
- 인터페이스 사용률: Choice 81.0%, Noul 72.2%, Score 45.4%. 셋 다 사용 36.8%.
- 결정 목적: 속성 판단 77%, 점수/순위 52%, 행동 선택 31%, 결과 판단 20%, 콘텐츠 필터링 15%, 모델/툴 선택 13%. 목적이 식별된 프로젝트의 69.7%가 2개 이상 목적.
- 도메인: 특정 도메인 지배 없음(최대 Content&Expert 17.8%, Search&Memory 17.6%). 스타는 Routing&Automation 41.4%(Model&Tool Routing 32.6%) 집중. Routing&Automation+Interface Agents가 프로젝트 19.6%로 스타 63.0%.
- 한계: 1주 스냅샷, 공개 레포만. 검증·라벨링은 GPT-6 Luna Max 에이전트가 수행.
- 인용된 파생 연구: Jev-mem(에이전트 메모리 제어, 2609.23986), Jev-as-a-judge(확신 시 수용·불확실 시 에스컬레이트, 2609.26550), 6G 엣지 서비스 오케스트레이션(2609.22753, 2609.23136), 과학 결정 평가(2609.24965), 텍스트 주석 평가(2609.24574), 경쟁 this-that-model-1.0(30ms, 2609.23886). 예시 레포: browser-use "Jev ultra-fast", jev-router, Typesafe mario.

## 5. 회사·투자 (WebSearch 요약, 2차 보도)
- 2024년 설립. CEO Diogo Almeida(전 OpenAI), 공동창업 Sasha Sheng(COO), Erik Gafni(CTO) — 직함은 출처마다 상이.
- 2026-09 스텔스 해제 시 시드 $40M(DCVC 리드, Business Wire 보도).
- 2026-10 Bloomberg: a16z 리드로 약 $870M, 기업가치 $7.5B. (한때 $1B+/$10B+ 협상 보도는 미성사.) 라운드 명칭(시드/시리즈A)은 출처 간 불일치.
- 출처: https://news.bgov.com/private-equity/andreessen-horowitz-backs-jev-maker-at-7-5-billion-value , https://www.vktr.com/ai-platforms/chatgpt-cocreator-launches-typesafe-ai-with-jev/ , https://app.dealroom.co/companies/typesafe_ai_jev

## 6. Jev 1.14 (2026-10-14) (WebSearch 요약)
- 실험 기능("danger zone"): 이미지 입력(헤더 TypeSafe-Danger-Zone-Images: true, 1.13에서도 사용 가능), 바운딩박스 질문 타입 Box(1.14 전용), 롱컨텍스트 262k(TypeSafe-Danger-Zone-Long-Context: true, 단가 동일·느려지고 정확도 하락).
- TypeSafe는 프로덕션 사용 비권장. 이미지도 입력 토큰 과금($0.042/M). 1.14 이미지·롱컨텍스트 공개 벤치마크 없음.
- 출처: https://alternativeto.net/news/2026/10/typesafe-ai-ships-jev-1-14-with-new-box-type-composable-images-and-longer-context-length/ , https://pasqualepillitteri.it/en/news/26048/jev-1-14-image-input-box-typesafe-warns , https://docs.litellm.ai/blog/typesafe_jev_images

## 7. 기타 확인
- Jevkit: Jev를 CLI·MCP 도구로 에이전트에 노출하는 개발 도구 (https://mcpmarket.com/server/jevkit).
- 개발자 우려: 선택 이유 설명이 없어 2차 모델 또는 설명 모드 필요하다는 의견 (levelup.gitconnected.com "The Risks of Using JEV AI in Enterprise Software").
- 한국 보도 표기: "Jev" = "제브". it.chosun 2026-09-24 기사는 영문을 "Zeb"로 오기(수치 70~500ms·$0.042가 Jev와 동일).
