---
title: parking (Supabase 공유 인프라)
category: 프로젝트
tags: [인프라, supabase, edge-functions, 마이그레이션, 백엔드]
source: raw/projects/parking.md
created: 2026-06-09
updated: 2026-08-24
---

> [!tip] 핵심 takeaway
> 네 개인 프로젝트들의 **공용 백엔드 허브**. [[notepad]]·[[mailer]]·[[schedule-reporter-kakao]]가 전부 여기 Supabase에 의존한다.
> → parking을 잘 관리하면 여러 앱이 동시에 안정되고, 잘못 건드리면 동시에 깨진다. **단일 장애점이자 단일 레버리지점.**
> ⚠️ 주의: parking raw는 `supabase db push`를 표준 절차로 안내하지만, [[mailer]]에는 이 명령을 쓰면 안 된다(아래 충돌 참고).
> 🆕 2026-08-06: parking 서비스 자체가 **사내 교육용으로 실서비스 전환**됐다(50면 이상 197건). 이제 인프라 허브인 동시에 대외 시연 대상이라, 데이터 재적재는 `/reload`로만 한다.
> 🚨 2026-08-24: **업스트림 data.go.kr이 전면 장애**(`result_code -999`)라 실시간 병합이 197/197 전건 실패했다. 교육용이라 실데이터일 필요가 없어 **결정적 목 데이터 폴백**을 넣었다(아래 참고).

## 개요
- 설명: 공용 프로젝트 — Supabase 설정 관리(마이그레이션 + Edge Functions + 공유 스키마). 백엔드/인프라.
- 최근 2026-03-19. CLAUDE.md 있음, README 없음.

## 역할
- DB 마이그레이션 관리 (`supabase/migrations/`)
- Edge Functions 배포 — 📄 현재 호스팅: `parking`·`notepad`·`todos`·`mailer`·`results`·`questions`·`admin`·`coginsight-generator` 등. 한 프로젝트(ref `enawzdqroidrhtjqhpka`)에 여러 서비스가 공존.
- [[notepad]]·[[mailer]]·[[schedule-reporter-kakao]]·[[CogInsight-Generator]]의 공유 백엔드 + DB

## 주요 명령어
```bash
supabase db push                                  # 마이그레이션 적용 (⚠️ mailer 예외 주의)
supabase functions deploy notepad --no-verify-jwt # Edge Function 배포
supabase db pull                                  # 원격 스키마 동기화
```

## ⚠️ 마이그레이션 절차 충돌 (건강검진 항목)
- parking raw 문서: 마이그레이션 = `supabase db push`.
- [[mailer]] 규칙: `supabase db push` **금지**, SQL Editor에서 멱등 SQL로 적용.
- → 프로젝트마다 마이그레이션 정책이 다르다. **공유 DB를 건드리는 작업 전에는 해당 앱의 정책을 먼저 확인**할 것. 통일된 정책 문서화가 필요(개선 과제).

## 개선 아이디어
- README 부재 + 정책 불일치 → "마이그레이션 운영 규칙" 한 장으로 통일하면 [[mailer]]/[[notepad]]/[[schedule-reporter-kakao]] 전체의 사고 위험이 줄어든다.

## parking API 연동 (Edge Function) 📄
> 한국 공공데이터포털(data.go.kr) 실시간 주차장 데이터 서비스. 정적정보(이름·주소·좌표)는 `parking_lot` 테이블, 실시간 점유는 조회 시 data.go.kr에서 즉시 fetch해 병합하는 **이중 데이터 모델**. (`supabase/functions/parking/index.ts`·`data.ts`)

**Base URL**: `https://enawzdqroidrhtjqhpka.supabase.co/functions/v1/parking`

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/reload?min={면수}&limit={건수}` | **(권장, 2026-08-06 추가)** 최소 주차면수 조건으로 전량 교체 적재 |
| POST | `/init` | (레거시) 주차장 ID 초기 적재(`PrkRealtimeInfo`) |
| POST | `/initInfo` | (레거시) 상세정보(이름/주소/좌표) 적재(`PrkSttusInfo`) — init 다음 |
| GET | `/parking` | 전체 목록 + 실시간 병합(`realtime` 필드 부착) |
| GET | `/parking?id={id}` | 단일 조회 + 실시간 병합(정제 응답), 없으면 404 |

- **사용 순서** 📄: `POST /reload` 한 번이면 된다. 레거시 경로를 쓸 경우에만 `POST /init` → `POST /initInfo` 순서가 필요하다.
- **인증** 🧠: `config.toml`에 `verify_jwt=false` 오버라이드가 없어 **JWT 검증 ON** → 호출 시 `Authorization: Bearer <ANON_KEY>` + `apikey: <ANON_KEY>` 헤더 필요. anon key는 parking/.env엔 없지만 **같은 프로젝트를 쓰는 [[mailer]]/[[notepad]]/[[schedule-reporter-kakao]]/[[CogInsight-Generator]]의 `.env`(`VITE_SUPABASE_ANON_KEY`)에 저장**돼 있어 그대로 재사용 가능(anon은 공개용 키라 안전, 진짜 비밀은 `SERVICE_ROLE_KEY`).
- ⚠️ **CORS 미처리** 🧠: parking 함수엔 [[notepad]]과 달리 CORS 헤더가 없어 **브라우저 직접 호출 불가 → 서버사이드/프록시 전용**.
- 단일 조회 응답: `prk_center_id, name, sido, sigungu, address, latitude, longitude, total_spaces, available_spaces, last_updated`.
- ⚠️ 주의 🧠: ① `parking_lot` 생성 마이그레이션이 repo에 없음(수동 생성) ② 레거시 `/init`·`/initInfo`는 `numOfRows=100` 고정(페이지네이션 없음) ③ `initInfo`가 DB `created_at` 순서 ↔ API index 순서로 매핑(`data.ts`)해 이름/주소가 오결합됨 → **원인 규명 완료, 아래 참고**.

### 🔑 두 외부 API의 ID 체계가 다르다 (2026-08-06 규명) 📄

`initInfo`가 인덱스 순서로 매칭했던 건 실수가 아니라 **ID로는 매칭이 불가능해서**였다.

```
실시간 PrkRealtimeInfo : 00000-19199-00003-00-1
상세   PrkSttusInfo    : 01016-11291-00001-00-1
```

실측 📄: 실시간 5만건 ∩ 상세 2만건 = **351건**만 겹침. 전체 건수는 실시간 787,232 / 상세 1,767,934.
→ 인덱스 매칭 방식으로는 이름·주소가 **구조적으로** 엉뚱한 주차장에 붙을 수밖에 없다.

**해결책 = `/reload` (교집합 방식)** 🧠: 두 API 모두에 존재하는 ID만 골라 적재하면
이름·주소·좌표(상세)와 실시간 점유 현황(실시간)이 **모두 정확히** 맞물린다.

- 상세 API의 `prk_cmprt_co`(주차구획수) 필드로도 면수 필터가 가능하나, 그 경우 실시간 병합이 거의 안 붙는다.
- 조회 시 실시간 병합 범위를 5,000건으로 확대(교집합 대상이 인덱스 2779~4804에 분포) — 응답 형태는 불변.
- 성능 실측 📄: 실시간 5천건 0.6초 / 상세 5만건 25초 → `/reload` 총 **약 30초**.

### 사내 교육용 서비스 운영 (2026-08-06) 📄

8기 인턴교육([[intern-education-2026-h2]] 관련)용 시연 데이터로 `min=50` 적용해 배포·서비스 중.

| 항목 | 값 |
|---|---|
| 적재 건수 | **197건** (총 주차면수 50면 이상) |
| 실시간 병합 | 197 / 197 전건 성공 |
| 지역 분포 | 남양주시 42 · 평택시 22 · 중구 20 · 의정부시 18 · 강남구 13 |
| 커밋 | `78d8948` (main 머지, `feat/parking-reload-min-capacity`) |

- ⚠️ 197건 중 **104건은 좌표(위경도)가 비어 있음** 📄 — 공공 API 원본이 빈 문자열로 내려주는 **데이터 결손**이며 코드 문제가 아니다. 지도 시연이 필요하면 좌표 보유 93건만 쓰는 옵션 추가 필요(미구현).
- 회귀 확인 📄: `/init`·`/initInfo`·`GET` 응답이 변경 전과 완전히 동일함을 실제 호출로 검증(기존 사용법 불변 요구사항).

### 🚨 업스트림 전면 장애와 목 데이터 폴백 (2026-08-24) 📄

`GET /parking`이 197건 **전부 `realtime: null`**, 단일 조회는 `total_spaces: 0, available_spaces: 0`을
반환하는 상태로 발견됐다. 2026-08-06 적재 이후 DB는 그대로였고, 깨진 건 실시간 병합이다.

**근본 원인 ① 업스트림 장애 (외부)** 📄 — data.go.kr `B553881/Parking`(한국교통안전공단)이 모든 요청에
`{ result_desc:'fail', result_code:'-999', http_status:'200' }`를 반환한다. `PrkRealtimeInfo`·`PrkSttusInfo`
양쪽, `numOfRows` 1~1000 전부, HTTP·HTTPS 전부 동일. 간헐적으로 `SERVICETIMEOUT_ERROR`로 **60초 매달림**.

대조실험으로 우리 키·코드 문제가 아님을 확정 📄:

| 요청 | 응답 |
|---|---|
| 잘못된 키 | `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` (30) |
| 키 없음 | `SERVICE_KEY_IS_NULL` (20) |
| 없는 오퍼레이션명 | `NO_OPENAPI_SERVICE_ERROR` |
| **우리 키** | **게이트웨이 통과** + `X-RateLimit-Remaining: 9988/10000` 정상 차감 → 백엔드에서 `-999` |

→ 키는 유효하고 쿼터도 살아 있다. `-999`는 포털 공식 에러코드 목록에 **없는** undocumented 제공기관
내부 오류다. 포털에 중단·점검·폐기 공지도 없다(최종수정 2026-06-01).

**근본 원인 ② 실패를 삼키는 코드 (우리 쪽)** 📄 — 장애 본문이 유효한 JSON이 아니어서(키에 따옴표 없음,
싱글쿼트, `Content-Type: text/html`) `await res.json()`이 예외를 던지고 `catch`가 `return []`로 삼켰다.
그래서 **전면 장애가 "데이터 없음"과 구별되지 않았다.** HTTP 200이 나가고 로그도 안 남고,
`getParkingById`는 `last_updated`에 현재 시각까지 찍어 없는 데이터를 방금 갱신된 것처럼 보이게 만들었다.
→ 🧠 언제부터 깨졌는지 알 수 없는 이유가 이것이다. 관측성 부재가 진짜 결함이었다.

**대응: 실데이터 우선 + 장애 시 결정적 목 폴백** 🧠 (브랜치 `feat/parking-mock-realtime-fallback`)

- `mock.ts` — FNV-1a 해시 기반 순수 함수. **총면수는 id로 영구 고정**(50~500, 10단위 = `min=50` 조건과 일관),
  **잔여면수는 1분 버킷**으로 변동. 같은 분 안에서는 몇 번 불러도 동일해서 목록 조회와 단일 조회 값이 일치한다.
- `upstream.ts` — 응답을 `text()`로 먼저 받아 판정(`{ok, rows} | {ok:false, reason}`). 테스트 픽스처로
  실측한 `-999` 본문을 그대로 쓴다(회귀 테스트).
- **응답 계약은 불변** — 목 필드명이 실 API와 같아(`pkfc_ParkingLots_total` 등) 소비자는 분기할 필요가 없고,
  목/실데이터 구분은 **서버 로그에만** 남긴다. 소비자에게 노출하지 않는다(교육용 샌드박스이므로).
  ⚠️ 실사용자 대상으로 돌릴 일이 생기면 합성 데이터 라벨링을 다시 검토해야 한다.
- **타임아웃 추가** — 실시간 5초 / 상세 40초. 60초 매달림을 제거해 최악 5초에 목으로 넘어간다.
- `/reload`는 **손대지 않았다** 🧠 — 이름·주소·좌표를 발명하는 건 잘못된 데이터다. 장애 중엔 그대로 실패한다.

검증 📄: 유닛 16/16, `deno check` 통과, 로컬 구동으로 실 DB·장애 API 상대 확인 —
197건 `realtime` null **0건**, 불변식(`0 ≤ available ≤ total`) 위반 0건, 같은 분 내 값 동일, 최악 5.1초.

### ⏱️ 응답시간: 60초 매달림 → 0.3초 (2026-08-24 배포) 📄

"찔러보면 응답시간이 너무 긴 경우가 있다"는 증상의 정체. 업스트림 게이트웨이가 간헐적으로
응답을 안 주고 매달리는데 **옛 코드에 타임아웃이 없어** 끝까지 기다렸다.

프로덕션 실측 (전체 목록 조회):

| | 옛 코드 | 타임아웃+캐시 | **목 전용 (현재)** |
|---|---|---|---|
| 최악 | **60.3초** | 6.9초 | 1.72초 (콜드스타트만) |
| 일반 | 0.32~0.59초 | 0.31~0.33초 | **0.24~0.35초** |
| 느린 호출 | 6회 중 1회 | 10회 중 6회 | 0 |

**중간에 한 번 틀렸다** 🧠 — 인메모리 TTL 캐시를 넣었더니 로컬(단일 프로세스)에서는
12회 중 업스트림 1회로 완벽했는데, 프로덕션에서는 오히려 10회 중 6회가 5.3초였다.
캐시가 **아이솔레이트 메모리**에 있고 Edge Function은 아이솔레이트를 재활용하기 때문.
warm으로 가면 0.3초, cold로 가면 타임아웃 5초를 그대로 문다.
→ **교훈: 프로세스 수명을 가정한 상태는 서버리스에서 전제가 깨진다. 배포 환경에서 반드시 재측정.**

**최종: 조회 경로에서 업스트림 호출을 기본 차단** (`PARKING_TRY_UPSTREAM`)

- 미설정이 기본 → 조회는 목 데이터로만 응답, 항상 ~0.3초
- **업스트림 복구되면 `supabase secrets set PARKING_TRY_UPSTREAM=1`로 실데이터 우선 복귀**
- 오타로 켜지는 걸 막기 위해 `1`·`true`만 허용
- `/reload`·`/init`은 플래그 무관하게 항상 업스트림 시도 → **복구 확인은 `/reload`로** (사유가 그대로 나옴)
- 캐시(성공 15초 / 실패 60초)는 플래그를 켰을 때 적용. 성공은 신선도 때문에 짧게,
  실패는 재시도마다 5초를 물기 때문에 길게 — **한 숫자로 뭉개면 안 되는 지점**

배포 완료 📄: `supabase functions deploy parking` (커밋 `ed32015`·`0415174`, main 머지 `cd1406f`).
프로덕션 검증 — 197건 `realtime` null 0건, 불변식 위반 0건, 단일 조회 같은 분 3회 `200/13` 동일.

## 관련 문서
- [[프로젝트-포트폴리오]] · [[notepad]] · [[mailer]] · [[schedule-reporter-kakao]] · [[CogInsight-Generator]] · [[공통-기술스택]]
