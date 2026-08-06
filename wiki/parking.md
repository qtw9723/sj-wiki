---
title: parking (Supabase 공유 인프라)
category: 프로젝트
tags: [인프라, supabase, edge-functions, 마이그레이션, 백엔드]
source: raw/projects/parking.md
created: 2026-06-09
updated: 2026-08-06
---

> [!tip] 핵심 takeaway
> 네 개인 프로젝트들의 **공용 백엔드 허브**. [[notepad]]·[[mailer]]·[[schedule-reporter-kakao]]가 전부 여기 Supabase에 의존한다.
> → parking을 잘 관리하면 여러 앱이 동시에 안정되고, 잘못 건드리면 동시에 깨진다. **단일 장애점이자 단일 레버리지점.**
> ⚠️ 주의: parking raw는 `supabase db push`를 표준 절차로 안내하지만, [[mailer]]에는 이 명령을 쓰면 안 된다(아래 충돌 참고).
> 🆕 2026-08-06: parking 서비스 자체가 **사내 교육용으로 실서비스 전환**됐다(50면 이상 197건). 이제 인프라 허브인 동시에 대외 시연 대상이라, 데이터 재적재는 `/reload`로만 한다.

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

## 관련 문서
- [[프로젝트-포트폴리오]] · [[notepad]] · [[mailer]] · [[schedule-reporter-kakao]] · [[CogInsight-Generator]] · [[공통-기술스택]]
