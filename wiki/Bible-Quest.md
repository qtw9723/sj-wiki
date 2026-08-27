---
title: Bible Quest (신앙 성장 RPG)
category: 프로젝트
tags: [프로젝트, 게임, 교회-개발, react, supabase, bible-quest]
source: IdeaProjects/MonsterCollector/Bible-Quest 저장소(README.md·ROADMAP.md·CLAUDE.md), GitHub qtw9723/Bible-Quest, 대화 확인(2026-08-27)
created: 2026-08-27
updated: 2026-08-27
---

> [!tip] 핵심 takeaway
> 📄 **신약 성경 스토리 기반 텍스트 RPG(솔로 개발)** — [[내-프로필]] 관점에서는 [[팀숲-bible-forest]](협업)와 대비되는 **1인 풀사이클 프로젝트** 포트폴리오 근거. 12챕터 중 3챕터 완료(진행률 ~17%), 로컬·GitHub 모두 최신 상태로 동기화되어 있음(2026-08-27 확인).
> 🧠 발표 준비 요청(2026-08-27)의 대상 프로젝트. 다음 우선순위는 로드맵상 **화면 프롬프트·이미지 에셋 제작**이므로, 발표에서도 "완료된 3챕터 데모 + 다음 단계 이미지 작업 계획" 구도로 짜는 게 자연스러움.

## 프로젝트 개요 📄

| 항목 | 내용 |
|------|------|
| 이름 | Bible Quest — 신앙 성장 RPG |
| 컨셉 | 신약 성경 스토리를 텍스트 기반 RPG로 각색, 선택지 기반 분기 스토리 |
| 대상 | 교회 대학부, 성경에 익숙하지 않은 사람들 |
| 구조 | 12개 챕터 |
| 개발 방식 | 솔로 개발(Claude Code 활용) |
| 배포 URL | https://bible-quest-nine.vercel.app |
| 소스 위치 | 로컬 `IdeaProjects/MonsterCollector/Bible-Quest`, GitHub `github.com/qtw9723/Bible-Quest` |
| 저장소 상태 | 2026-08-27 확인 — `working tree clean`, `origin/main`과 동기화됨(로컬-깃허브 간 누락 없음) |

## 기술 스택 📄

| 영역 | 기술 |
|------|------|
| 프론트 | Vite + React 19 + Tailwind CSS + Framer Motion |
| 백엔드 | Supabase (PostgreSQL + Edge Functions) |
| 배포 | Vercel |
| 인증 | Supabase Auth (예정, 미구현) |

## 화면 구성 📄

1. 타이틀 화면 — 게임 시작/이어하기
2. 챕터 선택 — 전체 챕터 목록 + 진행도
3. 스토리 화면 — 메인 게임(텍스트 + 선택지)
4. 챕터 완료 — 완료 메시지 + 성경 구절
5. 어드민 패널(`/admin`, 비밀번호 인증) — 장/장면/선택지 CRUD(StoryBuilder)

## 스토리 데이터 구조 📄

```json
{
  "chapter": 1,
  "title": "갈릴리의 부름",
  "scenes": [
    {
      "background": "galilee.jpg",
      "character": "peter.png",
      "text": "예수께서 갈릴리 해변을 지나가시다가...",
      "choices": [
        { "label": "따라간다", "next": 2 }
      ]
    }
  ]
}
```
DB 테이블: `chapters` · `scenes` · `choices`(스토리 데이터), `players` · `player_progress`(진행도).

## 진행 현황 📄 (ROADMAP.md 기준, 마지막 업데이트 2026-05-28)

| Phase | 상태 | 진행률 |
|-------|------|--------|
| 1. 기초 구조(Vite/React/Supabase/Tailwind/Framer Motion) | ✅ 완료 | 100% |
| 2. 어드민 대시보드(StoryBuilder, `/admin` 접근·비밀번호 인증) | ✅ 완료 | 100% |
| 3. 배포(Vercel, SPA 라우팅, 환경변수, GitHub) | ✅ 완료 | 100% |
| 4. 버그 수정(어드민 scene 로딩, choice 필드명, 모바일 반응형 등) | ✅ 완료 | 100% |
| 5. 콘텐츠 작성(챕터 1~3 완료: 갈릴리의 부름·광야의 시험·산상수훈, 4~12 미작성) | 🔄 진행 중 | 25% (3/12) |
| 6. 화면 프롬프트·이미지 에셋(Figma 설계 + AI 이미지 프롬프트 + Supabase Storage 업로드) | ⏳ 예정(우선순위 1위) | 0% |
| 7. 선택지 분기 처리(next_scene_id, 분기별 엔딩 2개 이상) | ⏳ 예정 | 0% |
| 8~13. 진행도 관리·사용자 인증·고급 기능(멀티엔딩·리더보드)·성능 최적화·QA·배포 준비 | ⏳ 예정 | 0% |

**전체 진행률: 약 17%**

> 🧠 로드맵의 "단기 목표(다음 1주)"는 **화면 프롬프트 제작(Figma + 배경 12개·캐릭터 5개 AI 이미지 프롬프트)** 이 1순위로 명시되어 있고, 챕터 4~6 콘텐츠 작성과 이미지 최소 3개 업로드가 뒤따른다.

## 어드민 접근 📄
- 경로: `localhost:5173/admin`
- 비밀번호: 환경변수 `VITE_ADMIN_PASSWORD`로 관리(ROADMAP 예시상 `admin123` — 로컬 개발용 표기, 프로덕션 값은 `.env` 확인 필요 🧠)

## 의외의 연결점 🧠
- 로컬 경로가 `IdeaProjects/MonsterCollector/Bible-Quest`로, [[게임-프로젝트-MonsterCollector-MonsterRank]]에서 다루는 **MonsterCollector(숫자 맞추기·카드 수집 게임, Unity+Supabase)와는 별개 프로젝트**가 그 폴더 안에 중첩 배치되어 있는 것으로 확인됨(2026-08-27). 같은 리포지토리가 아니라 폴더만 같이 쓰고 있는 형태.
- [[팀숲-bible-forest]]와 같은 "신약 성경 + 웹앱 + React/Supabase/Vercel" 계열이지만, 팀숲은 협업(4인)·게이미피케이션(나무 수집)인 반면 Bible Quest는 **솔로 개발·스토리텔링 RPG** 축이라 같은 주제를 다른 방식으로 실험하는 포트폴리오 페어로 보임.

## 관련 문서
- [[팀숲-bible-forest]] — 같은 "신약 성경" 소재의 다른 프로젝트(협업)
- [[게임-프로젝트-MonsterCollector-MonsterRank]] — 같은 상위 폴더(MonsterCollector)의 게임 프로젝트 묶음 문서
- [[프로젝트-포트폴리오]] · [[내-프로필]]
