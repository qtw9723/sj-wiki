# parking

## 프로젝트 개요
- **설명**: 공용 프로젝트 - Supabase 설정 관리
- **유형**: 백엔드/인프라스트럭처
- **마지막 수정**: 2026-03-19 13:26:31
- **경로**: `/Users/sangjun/IdeaProjects/parking`

## 용도
- Supabase 마이그레이션 관리
- Edge Functions 배포 및 관리
- 공유 데이터베이스 스키마
- notepad, mailer, schedule-reporter-kakao 프로젝트의 백엔드

## 주요 디렉토리
```
parking/
├── supabase/
│   ├── migrations/        # DB 마이그레이션 파일
│   └── functions/
│       ├── notepad/       # Notepad Edge Function
│       └── ...
```

## Supabase CLI 명령어
```bash
# 마이그레이션 적용
supabase db push

# Edge Function 배포
supabase functions deploy notepad --project-ref enawzdqroidrhtjqhpka --no-verify-jwt

# Supabase 환경 동기화
supabase db pull
```

## 연동 프로젝트
- 📝 **notepad** - Edge Function(notepad) 호스팅
- 📧 **mailer** - Supabase 데이터 관리
- 📅 **schedule-reporter-kakao** - Supabase 데이터 관리

## 문서
- ✅ CLAUDE.md 있음
- ❌ README 없음

## parking API (Edge Function) — 2026-06-25 확인
- 프로젝트 ref: `enawzdqroidrhtjqhpka` → Base `https://enawzdqroidrhtjqhpka.supabase.co/functions/v1/parking`
- 데이터: data.go.kr `B553881/Parking` (PrkRealtimeInfo / PrkSttusInfo). 정적정보=`parking_lot` 테이블, 실시간=조회 시 fetch 병합(이중 모델).
- 엔드포인트:
  - `POST /init` — 주차장 ID 적재(최초 1회 먼저)
  - `POST /initInfo` — 상세(이름/주소/좌표) 적재
  - `GET /parking` — 전체 + realtime
  - `GET /parking?id={id}` — 단일 + realtime(정제 응답: prk_center_id,name,sido,sigungu,address,latitude,longitude,total_spaces,available_spaces,last_updated)
- 인증: verify_jwt ON(config.toml 오버라이드 없음) → `Authorization: Bearer <ANON_KEY>` + `apikey` 헤더 필요. anon key는 parking/.env엔 없고 mailer/notepad/schedule-reporter/CogInsight의 .env(VITE_SUPABASE_ANON_KEY)에 있음(같은 프로젝트라 공유 가능, anon은 공개용 키).
- CORS 미처리(notepad과 달리) → 브라우저 직접 호출 불가, 서버사이드 전용.
- env(.env): SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, PUBLIC_DATA_SERVICE_KEY (anon key 없음).
- 주의: parking_lot 생성 마이그레이션 repo에 없음(수동 생성), numOfRows=100 고정(페이지네이션 없음), initInfo는 created_at↔API index 순서 매핑(data.ts:92), 실시간 매칭 data.ts:158(0으로만 나오면 점검).
- 현재 호스팅 함수: parking·notepad·todos·mailer·results·questions·admin·coginsight-generator 등.

## 상태
인프라 관리용 프로젝트로, 다른 프로젝트들의 백엔드 역할을 수행.
