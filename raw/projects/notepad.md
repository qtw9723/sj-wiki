# notepad

## 프로젝트 개요
- **설명**: 마크다운 지원 메모장 애플리케이션 - Supabase 백엔드
- **유형**: 프론트엔드 애플리케이션
- **버전**: 0.0.0
- **마지막 수정**: 2026-05-04 16:36:13
- **경로**: `/Users/sangjun/IdeaProjects/notepad`

## 기술 스택
- **프레임워크**: React 19
- **빌드 도구**: Vite 8
- **스타일링**: Tailwind CSS 4
- **백엔드**: Supabase (PostgreSQL + Auth + Edge Functions)
- **마크다운**: react-markdown + remark-gfm
- **레이아웃**: react-resizable-panels (split view)
- **UI**: lucide-react (아이콘)
- **상호작용**: @dnd-kit (드래그 앤 드롭)

## 주요 의존성
```json
{
  "@supabase/supabase-js": "^2.99.2",
  "react": "^19.2.4",
  "react-dom": "^19.2.4",
  "react-markdown": "^10.1.0",
  "react-resizable-panels": "^4.7.6",
  "react-router-dom": "^7.14.0",
  "remark-gfm": "^4.0.1",
  "@dnd-kit/core": "^6.3.1",
  "@dnd-kit/sortable": "^10.0.0",
  "lucide-react": "^0.577.0"
}
```

## 개발 명령어
```bash
npm run dev      # Vite 개발 서버
npm run build    # 프로덕션 빌드
npm run lint     # ESLint 실행
npm run preview  # 빌드 결과 미리보기
```

## 문서
- ✅ README.md 있음
- ✅ CLAUDE.md 있음 (상세한 기술 문서)
- ❌ 추가 배포 문서 없음

## 주요 기능
- 📝 마크다운 지원 메모장
- 🎨 다크 테마
- 🏷️ 태그 기반 필터링
- 💾 자동 저장 (800ms debounce)
- 🔗 공유 링크 기능
- 🖼️ 이미지 업로드 (Supabase Storage)
- 📱 모바일 반응형 UI
- 🔐 인증 (Supabase Auth)

## 데이터 모델
**notes 테이블:**
- id (UUID PK)
- user_id (UUID FK, nullable)
- title (TEXT)
- content (TEXT)
- content_type ('markdown' | 'html' | 'text')
- tags (TEXT[])
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)

## 백엔드 연동
- **Edge Function**: `/Users/sangjun/IdeaProjects/parking/supabase/functions/notepad/`
- **배포**: `supabase functions deploy notepad --no-verify-jwt`
- **마이그레이션**: `parking/supabase/migrations/`에서 관리

## 스타일링
- **배경색**: #0d1117 (앱), #0d0d14 (사이드바)
- **강조색**: #7c6af5 (보라)
- **텍스트**: #e6edf3 (강함), #cdd9e5 (기본)
- **타이포그래피**: Pretendard, Noto Sans KR, SF Mono

## 배포
- **프론트엔드**: Vercel (main 브랜치 자동 배포)
- **Edge Function**: 수동 배포
- **환경변수**: 
  - VITE_SUPABASE_URL
  - VITE_SUPABASE_ANON_KEY
  - VITE_NOTEPAD_URL (Edge Function URL)

## 상태
안정적인 프로덕션 상태. 상세한 기술 문서(CLAUDE.md)가 구비되어 있음.
