---
title: SmartHub (구 Delivery SmartHub) — 링크 모음 (현행)
category: 프로젝트
tags: [프로젝트, 링크, delivery-smarthub, smarthub, 공유용]
source: 라이브 저장소 README.md·docs/deploy-notes.md 확인, 2026-10-28
created: 2026-07-21
updated: 2026-10-28
---

> [!tip] 핵심 takeaway
> SmartHub 관련 주소 모음. 2026-07-22 배포되어 **프로덕션 가동 중**이다(허브 cs·delivery, 모듈 5종). 저장소는 private이라 외부 공유는 앱 주소로만 한다.

## 🌐 앱 (배포됨)
- 📄 **프로덕션**: https://mww-smarthub.vercel.app — 허브 목록(`/`)·백오피스(`/admin`)는 플랫폼 비밀번호, 허브(`/hub/cs`·`/hub/delivery`)는 허브별 비밀번호(없으면 공개).
  - ⚠️ 팀 슬러그가 붙은 Vercel URL은 SSO 보호라 302. 외부 호출·크론은 반드시 위 깔끔한 도메인 사용. 구 `delivery-smarthub.vercel.app`은 죽음(2026-07-22 도메인 변경).

## 🔒 소유자 전용 (개인 계정 인증 필요)
- 📄 **GitHub 저장소** (private): https://github.com/qtw9723/smarthub (옛 이름 delivery-smarthub, 2026-07-22 리네임)
- 📄 **로컬 경로**: `/Users/sangjun/IdeaProjects/smarthub`
- 📄 **Supabase**: [[mailer|CS SmartHub]]와 공유 프로젝트(대시보드 "parking", [[parking]]). SmartHub는 `hub_*`·hub 스코프 공유 테이블만 사용.
- 📄 **Vercel**: main 머지 = 자동 배포. committer는 GitHub noreply여야 통과.

## 📄 저장소 내부 문서
- `README.md` — 구조·인증 경계·모듈 계약 / `ROADMAP.md` — 계획(현재 계획 섹션 없음, 백로그만) / `CHANGELOG.md` — 완료 이력
- `docs/deploy-notes.md` — 배포·pg_cron(jobid 9~12)·컷오버 기록 / `docs/legacy-inventory.md` — 구 mailer 잔재 목록 / `docs/backups/` — 구 테이블 폐기 백업
- `docs/superpowers/specs·plans/` — 설계 스펙·구현 계획(Phase1, 단계 A, mailer 마이그레이션 M1~M5, grafana 멀티소스, 문서 도구 이식 등)

## 관련 문서
- [[delivery-smarthub]] — 프로젝트 본문(현재 상태·이력) · [[mailer]](형제·기원) · [[프로젝트-포트폴리오]] · [[parking]]
