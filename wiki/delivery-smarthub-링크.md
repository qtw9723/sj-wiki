---
title: Delivery SmartHub — 링크 모음 (현행)
category: 프로젝트
tags: [프로젝트, 링크, delivery-smarthub, 공유용]
source: 신규 구축 세션 2026-07-21
created: 2026-07-21
updated: 2026-07-21
---

> [!tip] 핵심 takeaway
> delivery-smarthub 관련 주소를 한 곳에 모아둔 페이지. 현재 **private 레포만 존재**하고 **배포는 아직 안 함**(Phase1) — 그래서 공개 URL은 없다. 배포하면 이 페이지에 Vercel 주소를 추가한다.

## 🔒 소유자 전용 (개인 계정 인증 필요)
- 📄 **GitHub 저장소** (private): https://github.com/qtw9723/delivery-smarthub
  - 초기 커밋: `1ecc864` (Phase1 — delivery 허브 챗봇 모니터링 + 중앙 백오피스, 2026-07-21)
- 📄 **로컬 경로**: `/Users/sangjun/IdeaProjects/delivery-smarthub`
- 📄 **Supabase 대시보드** (cs와 공유, 프로젝트명 "parking"): https://supabase.com/dashboard/project/enawzdqroidrhtjqhpka
  - ⚠️ delivery-smarthub는 **`hub_*` 테이블만** 사용. cs 테이블(`chatbots` 등)은 무접근.

## 📄 프로젝트 내부 문서 (레포 내)
- 설계 스펙: `docs/superpowers/specs/2026-07-21-delivery-smarthub-phase1-design.md`
- 구현 계획: `docs/superpowers/plans/2026-07-21-delivery-smarthub-phase1.md`
- 배포/크론 실등록 절차(미실행): `docs/deploy-notes.md`

## ⏳ 아직 없음 (Phase1 미배포)
- 🌐 공개/앱 Vercel 주소 — **배포 시 추가 예정** (신규 Vercel 프로젝트, cs와 별개).
- pg_cron 정시 트리거 잡 — cs jobid 8과 별개의 새 잡으로 등록 예정(사용자 확인 후).

## 관련 문서
- [[delivery-smarthub]] — 프로젝트 본문(설계·진행 현황) · [[mailer]](형제) · [[프로젝트-포트폴리오]] · [[parking]]
