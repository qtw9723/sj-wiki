---
title: parking (Supabase 공유 인프라)
category: 프로젝트
tags: [인프라, supabase, edge-functions, 마이그레이션, 백엔드]
source: raw/projects/parking.md
created: 2026-06-09
updated: 2026-06-25
---

> [!tip] 핵심 takeaway
> 네 개인 프로젝트들의 **공용 백엔드 허브**. [[notepad]]·[[mailer]]·[[schedule-reporter-kakao]]가 전부 여기 Supabase에 의존한다.
> → parking을 잘 관리하면 여러 앱이 동시에 안정되고, 잘못 건드리면 동시에 깨진다. **단일 장애점이자 단일 레버리지점.**
> ⚠️ 주의: parking raw는 `supabase db push`를 표준 절차로 안내하지만, [[mailer]]에는 이 명령을 쓰면 안 된다(아래 충돌 참고).

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
| POST | `/init` | 주차장 ID 초기 적재(`PrkRealtimeInfo`) — **최초 1회 먼저** |
| POST | `/initInfo` | 상세정보(이름/주소/좌표) 적재(`PrkSttusInfo`) — init 다음 |
| GET | `/parking` | 전체 목록 + 실시간 병합(`realtime` 필드 부착) |
| GET | `/parking?id={id}` | 단일 조회 + 실시간 병합(정제 응답), 없으면 404 |

- **사용 순서** 📄: 조회 전 반드시 `POST /init` → `POST /initInfo`로 DB를 채워야 데이터가 나온다.
- **인증** 🧠: `config.toml`에 `verify_jwt=false` 오버라이드가 없어 **JWT 검증 ON** → 호출 시 `Authorization: Bearer <ANON_KEY>` + `apikey: <ANON_KEY>` 헤더 필요. anon key는 parking/.env엔 없지만 **같은 프로젝트를 쓰는 [[mailer]]/[[notepad]]/[[schedule-reporter-kakao]]/[[CogInsight-Generator]]의 `.env`(`VITE_SUPABASE_ANON_KEY`)에 저장**돼 있어 그대로 재사용 가능(anon은 공개용 키라 안전, 진짜 비밀은 `SERVICE_ROLE_KEY`).
- ⚠️ **CORS 미처리** 🧠: parking 함수엔 [[notepad]]과 달리 CORS 헤더가 없어 **브라우저 직접 호출 불가 → 서버사이드/프록시 전용**.
- 단일 조회 응답: `prk_center_id, name, sido, sigungu, address, latitude, longitude, total_spaces, available_spaces, last_updated`.
- ⚠️ 주의 🧠: ① `parking_lot` 생성 마이그레이션이 repo에 없음(수동 생성) ② data.go.kr 호출 `numOfRows=100` 고정(페이지네이션 없음) ③ `initInfo`가 DB `created_at` 순서 ↔ API index 순서로 매핑(`data.ts:92`)해 정렬 어긋나면 이름/주소 오결합 가능 — 실시간 수치가 항상 0이면 id 매칭(`data.ts:158`) 점검.

## 관련 문서
- [[프로젝트-포트폴리오]] · [[notepad]] · [[mailer]] · [[schedule-reporter-kakao]] · [[CogInsight-Generator]] · [[공통-기술스택]]
