# schedule-reporter-kakao

## 프로젝트 개요
- **설명**: 일정 리포터 - 카카오톡 연동 기능
- **유형**: 풀스택 애플리케이션 (프론트엔드 + 백엔드)
- **버전**: 0.1.0
- **마지막 수정**: 2026-06-08 16:27:48
- **경로**: `/Users/sangjun/IdeaProjects/schedule-reporter-kakao`

## 기술 스택
- **프론트엔드**: React 19 + Vite 8 + Tailwind CSS 4
- **백엔드**: Express.js (Node.js)
- **데이터베이스**: Supabase
- **이메일**: Nodemailer
- **UI 상호작용**: @dnd-kit (드래그 앤 드롭)

## 주요 의존성
```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.101.1",
    "express": "^4.21.2",
    "nodemailer": "^6.9.16",
    "cors": "^2.8.5",
    "dotenv": "^16.4.7",
    "@dnd-kit/core": "^6.3.1",
    "@dnd-kit/sortable": "^10.0.0",
    "lucide-react": "^1.7.0",
    "react": "^19.2.4",
    "react-router-dom": "^6.30.1"
  }
}
```

## 개발 명령어
```bash
npm run dev           # 클라이언트 + 서버 동시 실행
npm run dev:client   # 클라이언트만 실행
npm run dev:server   # 서버만 실행
npm run build        # 프로덕션 빌드
npm run test         # 테스트 실행
npm run test:watch   # 테스트 워치 모드
npm run lint         # ESLint 실행
```

## 문서
- ✅ README.md 있음
- ✅ CLAUDE.md 있음 (Vercel 배포 모범 사례)
- ❌ 상세 기술 문서 없음

## 아키텍처
- **클라이언트**: React + Vite SPA
- **서버**: Express.js (포트별도 운영)
- **데이터베이스**: Supabase
- **통신**: REST API (Express 서버)

## 특징
- 📅 일정 리포팅 기능
- 🤖 카카오톡 연동
- 📧 메일 발송 기능 (Nodemailer)
- 🎨 드래그 앤 드롭 UI
- 📊 Supabase 데이터 관리
- 🔐 CORS 처리

## 주요 차이점 (mailer와의 비교)
- mailer는 일반적인 메일링, schedule-reporter-kakao는 일정 기반 리포팅 + 카카오톡 연동
- 동일한 기술 스택 (React + Express + Supabase)

## 2026-06-25 재확인 — 단순화/피벗 (위 정보는 2026-06-08 기준 구버전)
- 2026-06-09 커밋 `refactor: simplify to schedule settings page only`로 **대폭 단순화**됨.
- **카카오 연동 코드 제거됨**: src/server/api 어디에도 `kakao/카카오` 참조 없음(grep 0건). 프로젝트명에만 "kakao"가 잔존(원래 목표=카카오톡 Play MCP 스케줄 기능을 자체 서버로 마이그레이션 — README 기준).
- **현재 앱**: `App.jsx` 라우트는 `/login`(LoginPage) + `/`(GrafanaPage, ProtectedRoute) 뿐. 사실상 **Grafana 리포트 스케줄 설정 단일 페이지**.
- 구조가 [[mailer]]와 동일 계열로 정렬됨: `src/pages/`에 GrafanaPage·HubPage·MailerPage·ChatbotPage·LoginPage 존재(라우팅은 Grafana만), `src/components/grafana|mailer|shared`, `src/lib/api/grafana.js`.
- README 설명: "카카오톡 플레이 MCP의 스케줄 기능을 자체 서버로 마이그레이션". 마이그레이션 체크리스트는 전부 미완([ ]). 스케줄링=Grafana 리포트 자동화(일일/주간).
- 스택: React19/Vite8/Tailwind4 + Express + Supabase + Nodemailer(여전). 최근 커밋 2026-06-09.
- 🧠 해석: mailer의 Grafana 리포트 기능을 떼어내 별도 앱으로 두려던 형제 프로젝트로 보이며, 현재는 mailer와 기능이 상당 부분 겹침.

## 상태
현재 활발히 개발 중 (최근 수정: 2026-06-08)
