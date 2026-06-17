---
title: 팀숲 — Bible Forest (교회 대학부 신약 1독 챌린지)
category: 프로젝트
tags: [프로젝트, 교회-개발, bible-forest, next.js, supabase, 협업개발]
source: (대화 기반, D:\Projects\bible_forest\app\docs\)
created: 2026-06-17
updated: 2026-06-17
---

> [!tip] 핵심 takeaway
> 🧠 **교회 대학부 대학생들이 신약 성경을 함께 읽으며 팀 숲을 키우는 게이미피케이션 웹앱.** 개발 기여자로 참여(sangjun = 백엔드 설계·문서화·의사결정 리드). [[내-프로필]] 관점에서는 협업 개발 + Supabase/Next.js 실전 경험 + 기획→설계→문서화→배포 풀사이클. 6/23 교회 수련회용 시연이 목표.
> 🧠 이 프로젝트의 가장 큰 기술 포인트: **"나무 회수 시 배치된 나무도 삭제"** — DB의 is_planted 구분과 무관하게 획득 역순 삭제. z_index 시퀀스로 렌더링 순서까지 관리하는 것이 자연스러운 UX 설계.

## 프로젝트 개요 📄

| 항목 | 내용 |
|------|------|
| 목적 | 교회 대학부 신약 1독 챌린지 (6월~수련회) |
| 컨셉 | 장 체크 → 나무 획득 → 팀 숲에 배치 → 팀별 랭킹 |
| 대상 | 교회 대학부 (비개발자 포함, Zero-Friction 로그인) |
| 로그인 | 이름 + 팀 선택만으로 즉시 등록. 비밀번호 없음. 쿠키 60일 |
| 배포 | Vercel (소스: 유성진 개인 GitHub, public) |
| 소스 위치 | `D:\Projects\bible_forest\` (로컬 클론) |

---

## 기술 스택 📄

| 영역 | 기술 |
|------|------|
| 프레임워크 | Next.js 16 App Router + TypeScript |
| 백엔드 | Next.js Route Handlers (`/api/v1/*`) — 별도 서버 없음 |
| DB | Supabase(Postgres) — **테이블 저장소로만** 사용, 로직은 백엔드 |
| 스타일 | Tailwind CSS + shadcn/ui |
| 배포 | Vercel (Root Directory: `app/`) |

> ⚠️ `AGENTS.md` 경고: "This is NOT the Next.js you know — read node_modules/next/dist/docs/ before writing code"

---

## 핵심 기능 📄

```
장 체크 (신약 260장) → 10장마다 나무 1그루 지급
                    → 260장 완독 시 특별 나무
나무 배치 → 팀 숲 격자에 좌표(%) 저장
팀 숲 조회 → 팀별 나무 배치 현황 + 랭킹
```

---

## 핵심 설계 결정 📄

> 전체 결정: `app/docs/backend-decisions.md`

| 결정 | 내용 |
|------|------|
| 나무 회수 | **회수함** — 재계산 후 마지막 획득 나무부터 삭제(배치 나무 포함) |
| 체크 API | **권(book) 단위 bulk replace** — 완료 버튼 시 해당 권 전체 교체 |
| 좌표 | % 값(0~100), `numeric(5,2)` |
| 배치 | 1회성 (좌표 수정 불가). 단 회수 처리 시 삭제 가능 |
| z-index | DB 시퀀스로 획득 순서 = z 순서 |
| 챌린지 기간 | 쓰기(체크)만 기간 제약, 조회는 기간 이후에도 허용 |
| 닉네임 | 10자 이내 (프론트 maxLength 제어) |

---

## API 구조 📄

| 그룹 | 엔드포인트 | 상태 |
|------|-----------|------|
| 인증 | `POST /auth/register`, `POST /auth/logout`, `DELETE /auth/withdraw` | ✅ 구현 |
| 사용자/팀 | `GET /users/me`, `GET /teams` | ✅ 구현 |
| 어드민 | `POST /admin/login`, `GET /admin/dashboard` | ✅ 구현 |
| 성경 | `GET·PATCH /bible/progress`, `GET /bible/status` | ✅ 구현 (스펙 변경 예정) |
| 나무 | `GET /trees/inventory`, `POST /trees/place` | ✅ 구현 |
| 숲 | `GET /forests/:team_id` | ✅ 구현 |

---

## DB 스키마 요약 📄

```
teams ──< users ──< bible_progress
              └──< trees (z_index serial, is_planted, x, y, species)
challenges (is_active=true인 1건이 체크 기간 제약 기준)
```

**추가 마이그레이션 필요**: `trees.z_index serial` 컬럼 추가 (2026-06-17 결정)

---

## 개발 일정 📄

| 날짜 | 마일스톤 |
|------|---------|
| 6/19 (금) | 디자인 완성분 프론트 개발 완료 |
| 6/23 (화) | 전체 시연 가능 수준 완성 |
| 수련회 | 베스트 가드너 시상 + 대형 스크린 전시 |

---

## 팀 구성 📄

| 역할 | 담당 |
|------|------|
| 백엔드/설계 | sangjun (유성진) |
| DB | 백은률 |
| 프론트 | 유혁상 |
| 디자인 | 이다혜 |

---

## 의외의 연결점
- 🧠 **[[공통-기술스택]]과 다른 스택**: 이 프로젝트는 Next.js 16 App Router + Supabase. 개인 프로젝트(React+Vite)와 달리 Next.js SSR 방식 — 두 스택을 병행하는 경험.
- 🧠 **Zero-Friction 로그인**은 [[교회-일정공유-캘린더]]와 동일 철학 — 비밀번호 없이 이름+선택만으로 참여. 대학부 서비스 특성.
- 🧠 API-First 설계(FE는 API 결과만 표시) → 역할 분리가 명확해 협업 마찰 최소화. [[mailer]]나 [[schedule-reporter-kakao]] 혼자 개발할 때와 다른 협업 패턴 경험.

## 관련 문서
- [[교회-백엔드-회의-2026-06-12]] — 1차 회의 (백엔드 완료·브랜치 전략)
- [[교회-개발-회의-2026-06-17]] — 2차 회의 (설계 변경·일정 확정)
- [[교회-일정공유-캘린더]] — 같은 교회 개발팀의 별개 프로젝트
- [[프로젝트-포트폴리오]] — 전체 프로젝트 목록
