---
title: notepad
category: 프로젝트
tags: [프로젝트, 프론트엔드, supabase, 마크다운]
source: raw/projects/notepad.md
created: 2026-06-09
updated: 2026-06-09
---

> [!tip] 핵심 takeaway
> 네 포트폴리오 중 **가장 완성도 높고 문서화가 잘 된 레퍼런스 프로젝트**(✅ 프로덕션 안정, 상세 CLAUDE.md 보유).
> 새 프로젝트를 시작할 때 **구조·스타일·배포의 기준점**으로 삼으면 된다. 특히 자동저장(800ms debounce)·태그 필터·공유 링크 패턴은 [[mailer]]·[[Cogi-POC-Generator]]에 그대로 재사용 가능.

## 개요
- 마크다운 지원 메모장. 유형: 프론트엔드 SPA + [[parking]]의 Supabase 백엔드.
- 상태: 안정적 프로덕션. 마지막 수정 2026-05-04.

## 기술 스택
[[공통-기술스택]] 기반 + 특화 라이브러리:
- react-markdown + remark-gfm (마크다운 렌더링)
- react-resizable-panels (split view)
- @dnd-kit (드래그앤드롭), lucide-react

## 주요 기능
마크다운 메모 · 다크 테마 · 태그 필터 · **자동 저장(800ms debounce)** · 공유 링크 · 이미지 업로드(Supabase Storage) · 모바일 반응형 · Supabase Auth.

## 데이터 모델 (notes)
`id, user_id(nullable), title, content, content_type('markdown'|'html'|'text'), tags[], created_at, updated_at`

## 백엔드 / 배포
- Edge Function: [[parking]] `supabase/functions/notepad/`
- 배포: `supabase functions deploy notepad --no-verify-jwt`
- 프론트: Vercel main 자동 배포. 환경변수 `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_NOTEPAD_URL`.

## 스타일 토큰 (재사용 가치)
배경 #0d1117 / 사이드바 #0d0d14 / 강조 #7c6af5(보라) / 텍스트 #e6edf3. 폰트 Pretendard·Noto Sans KR·SF Mono.

## 관련 문서
- [[프로젝트-포트폴리오]] · [[parking]] · [[공통-기술스택]] · [[mailer]]
