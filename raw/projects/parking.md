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

## 상태
인프라 관리용 프로젝트로, 다른 프로젝트들의 백엔드 역할을 수행.
