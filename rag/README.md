# sj-wiki RAG (MVP)

sj-wiki의 **게임 요소 라이브러리**(`게임요소-*`, `게임-*`)와 **AI 주간 소식**(`AI-주간-소식-*`)을 대상으로 한 하이브리드 검색 + 답변(RAG) API/웹.

- 코퍼스: 107개 페이지 → 3,808 청크 (게임 85p/493c, AI뉴스 22p/3,315c)
- 검색: BM25(한글 bigram) + 벡터(코사인) → RRF 융합
- 임베딩/답변: **무료 OpenAI 호환 API** (키는 환경변수로만, 저장소에 두지 않음)
- 스냅샷: 인덱스는 특정 위키 커밋에 고정(`index/meta.json`의 `wikiCommit`) — 위키가 매일 바뀌어도 평가가 재현됨

## 구조

```
rag/
├── scripts/build-index.mjs   # wiki → 헤딩 기반 청킹 → index/chunks.json (+ meta.json, 커밋 SHA)
├── scripts/embed.mjs         # 청크 임베딩 → index/vectors.bin (배포 빌드 시 실행, 키 없으면 생략)
├── lib/search.mjs            # BM25 + 벡터 + RRF
├── lib/llm.mjs               # OpenAI 호환 embeddings / chat 클라이언트
├── api/{search,ask,health}.mjs
├── public/index.html         # 모바일 대응 검색 UI
└── eval/                     # 질문셋 + hit@k / MRR 평가
```

## API

| 엔드포인트 | 설명 |
|---|---|
| `GET /api/search?q=&k=8&category=game\|ai-news&mode=hybrid\|lexical\|vector` | 청크 검색(CORS 허용). 결과에 BM25/벡터 순위, 원문 링크 포함 |
| `POST /api/ask` `{question, k?, category?}` | 검색 + LLM 답변 + 근거 번호. `RAG_API_TOKEN` 설정 시 `Authorization: Bearer` 필요 |
| `GET /api/health` | 스냅샷 커밋, 청크 수, 벡터/모델 설정 상태(키 값은 노출 안 함) |

```bash
curl "$BASE/api/search?q=자세 게이지 붕괴&k=3"
curl -X POST "$BASE/api/ask" -H "authorization: Bearer $RAG_API_TOKEN" \
  -H "content-type: application/json" -d '{"question":"독성 한도 시스템이란?"}'
```

## 환경변수 (Vercel Project Settings → Environment Variables)

| 이름 | 용도 |
|---|---|
| `WIKI_LLM_BASE_URL` `WIKI_LLM_API_KEY` `WIKI_LLM_MODEL` | 답변 모델 (sj-wiki `~/.wiki-llm.env`와 동일한 이름) |
| `WIKI_LLM_REASONING_EFFORT` | 선택(예: `low`) |
| `EMBED_MODEL` | 임베딩 모델명. 설정해야 벡터 검색이 켜짐 |
| `EMBED_BASE_URL` `EMBED_API_KEY` | 선택. 미지정 시 `WIKI_LLM_*`의 값을 재사용 |
| `EMBED_DIMENSIONS` | 선택 |
| `RAG_API_TOKEN` | 권장. `/api/ask` 보호(무료 키 남용 방지) |

임베딩 설정이 없으면 **BM25 전용**으로 정상 동작한다. 설정 후 재배포하면 빌드 단계에서 벡터가 생성된다.

## 로컬 실행

```bash
cd rag
npm run build:index      # 위키 → 청크 (위키 커밋 고정)
npm run dev              # http://localhost:3000
npm run eval             # 검색 평가 (벡터는 EMBED_* 설정 시)
EVAL_BASE_URL=https://배포주소 npm run eval   # 배포 API 대상 평가
```

## 평가 (eval/)

질문 47개(게임 26 + 영어·동의어 질의 10 + AI뉴스 11), 정답은 페이지 단위. AI뉴스는 고유 용어가 실제로 들어 있는 페이지를 정답으로 자동 산출.

BM25 기준선 (스냅샷 `22bc3cc`):

| 구간 | hit@1 | hit@5 | MRR |
|---|---|---|---|
| 전체 | 0.787 | 0.809 | 0.796 |
| 게임(한국어 질의) | 1.00 | 1.00 | 1.00 |
| AI뉴스 | 0.909 | 0.909 | 0.922 |
| **영어·동의어 질의** | **0.10** | **0.20** | **0.125** |

해석: 질문과 문서가 같은 단어를 공유하면 BM25만으로 충분하지만, 어휘가 달라지는 질의(영어로 묻기 등)는 거의 못 찾는다 → 벡터 검색이 개선해야 할 구간. 벡터/하이브리드 수치는 임베딩 설정 후 같은 스크립트로 측정해 이 표에 추가한다.

> 한계: 질문 일부를 페이지의 핵심 문장을 보고 작성해 한국어 질의 구간은 쉬운 편이다(포화). 변별력은 영어·동의어 구간에서 본다.

## 보안 메모

- 위키 청크는 **자료일 뿐 지시가 아니다**: `/api/ask`의 시스템 프롬프트가 근거 속 지시문을 따르지 않도록 명시(간접 프롬프트 인젝션 방어). 자동 테스트는 아직 없음.
- 키는 코드·저장소에 없고 환경변수로만 사용. `RAG_API_TOKEN`이 없으면 `/api/ask`는 IP당 분당 5회로 제한(인스턴스 단위 best-effort).
- 코퍼스는 공개 저장소의 게임·AI뉴스 페이지만 포함(회사/교회/프로필 페이지 제외).
