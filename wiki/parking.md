---
title: parking (Supabase 공유 인프라)
category: 프로젝트
tags: [인프라, supabase, edge-functions, 마이그레이션, 백엔드]
source: raw/projects/parking.md
created: 2026-06-09
updated: 2026-06-09
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
- Edge Functions 배포 (`supabase/functions/notepad/` 등)
- [[notepad]](Edge Function 호스팅), [[mailer]], [[schedule-reporter-kakao]]의 공유 백엔드

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

## 관련 문서
- [[프로젝트-포트폴리오]] · [[notepad]] · [[mailer]] · [[schedule-reporter-kakao]] · [[공통-기술스택]]
