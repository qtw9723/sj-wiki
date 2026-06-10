# mailer (cs-smarthub)

## 프로젝트 개요
- **설명**: CS SmartHub - 메일러 애플리케이션
- **유형**: 풀스택 애플리케이션 (프론트엔드 + 백엔드)
- **버전**: 0.1.0
- **마지막 수정**: 2026-06-08 16:33:43
- **경로**: `/Users/sangjun/IdeaProjects/mailer`

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
- 메일 발송 기능 (Nodemailer)
- 드래그 앤 드롭 UI (@dnd-kit)
- Supabase 데이터 관리
- CORS 처리

## 상태
현재 활발히 개발 중 (최근 수정: 2026-06-08)
