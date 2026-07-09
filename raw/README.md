# IdeaProjects Raw Data

옵시디언 위키화를 위한 `/Users/sangjun/IdeaProjects` 프로젝트들의 raw 데이터입니다.

생성일: 2026-06-09

## 📊 프로젝트 목록

### Node.js/JavaScript 프로젝트 (4개)

#### 🟢 활발한 프로젝트

| 프로젝트 | 유형 | 마지막 수정 | 상태 |
|---------|------|---------|------|
| **notepad** | 프론트엔드 | 2026-05-04 | ✅ 프로덕션 안정 |
| **mailer** | 풀스택 | 2026-06-08 | 🔄 개발 중 |
| **schedule-reporter-kakao** | 풀스택 | 2026-06-08 | 🔄 개발 중 |
| **CogInsight-Generator** | 프론트엔드 | 2026-05-27 | ✅ 배포 준비 |

### 기타 프로젝트 (3개)

| 프로젝트 | 유형 | 마지막 수정 | 상태 |
|---------|------|---------|------|
| **parking** | 백엔드/인프라 | 2026-03-19 | 📦 공유 인프라 |
| **MonsterCollector** | 미정 | 2026-05-28 | ❓ 정보 부족 |
| **MonsterRank** | 미정 | 2026-03-18 | ❓ 정보 부족 |

## 🗂️ 파일 구조

```
raw/
├── README.md              # 이 파일
├── projects.json          # 전체 프로젝트 메타데이터 (JSON)
└── projects/
    ├── coginsight-generator.md
    ├── mailer.md
    ├── notepad.md
    ├── schedule-reporter-kakao.md
    ├── monster-collector.md
    ├── monster-rank.md
    └── parking.md
```

## 📋 공통 기술 스택

### 프론트엔드 스택
- **React** 19 (모든 프로젝트)
- **Vite** 8 (빌드 도구)
- **Tailwind CSS** 4 (스타일링)
- **lucide-react** (아이콘)

### 백엔드/데이터
- **Supabase** (PostgreSQL, Auth, Edge Functions)
- **Express.js** (mailer, schedule-reporter-kakao)
- **Nodemailer** (메일링)

### 추가 라이브러리
- **react-router-dom** (라우팅)
- **@dnd-kit** (드래그 앤 드롭)
- **zod** (데이터 검증)

## 🔗 프로젝트 간 연동

```
┌─────────────────────────────────────┐
│        parking (Supabase)           │
│  ├── Database Migrations            │
│  ├── Edge Functions (notepad)       │
│  └── Shared Infrastructure          │
└─────────────────────────────────────┘
         ↑      ↑      ↑
         │      │      │
    ┌────┘      │      └────┐
    │           │           │
┌───┴──┐   ┌───┴──┐   ┌────┴──┐
│notepad│   │mailer│   │ schedule-│
│       │   │      │   │ reporter │
└───────┘   └──────┘   └─────────┘
```

- **notepad**: 독립 실행형 앱 (parking의 Edge Function 사용)
- **mailer**: 메일링 기능 (parking의 Supabase 사용)
- **schedule-reporter-kakao**: 일정 리포팅 (parking의 Supabase 사용)

## 📚 문서 현황

### 상세 문서 있음
- ✅ **notepad**: CLAUDE.md (매우 상세)
- ✅ **CogInsight-Generator**: 배포 문서 완비
- ✅ **mailer/schedule-reporter-kakao**: CLAUDE.md (Vercel 모범 사례)

### 부분 문서
- ⚠️ **MonsterCollector**: CLAUDE.md만 있음
- ⚠️ **parking**: CLAUDE.md만 있음

### 문서 부족
- ❌ **MonsterRank**: 문서 없음

## 🚀 배포 현황

### Vercel 배포
- notepad (자동 배포)
- 기타 프로젝트 (Vercel 모범 사례 문서화)

### Supabase 배포
- Edge Function: `supabase functions deploy notepad --no-verify-jwt`
- 마이그레이션: `parking` 프로젝트에서 관리

## 🔍 데이터 출처

**작성 기준**: 2026-06-09

각 프로젝트별 정보는 다음에서 추출:
- `package.json` - 메타데이터, 스크립트, 의존성
- `CLAUDE.md` - 기술 상세 내용
- `README.md` - 프로젝트 설명
- 배포 관련 파일 - 배포 절차

## 💡 사용 방법

### Obsidian에서 임포트
1. 이 폴더를 Obsidian 볼트에 복사
2. `projects.json`을 활용해 각 프로젝트 노트 자동 생성 가능
3. 각 프로젝트별 `.md` 파일을 마크다운으로 변환

### JSON 활용
`projects.json`에는 모든 프로젝트의 메타데이터가 구조화되어 있어 다른 도구에서도 파싱 가능.

## 📝 업데이트 가이드

새로운 프로젝트 추가 시:
1. `projects.json`에 항목 추가
2. `projects/{projectName}.md` 파일 생성
3. README.md의 표 업데이트

각 프로젝트별 정보 업데이트:
- 정기적으로 `package.json` 확인
- 주요 기술 변경사항 `projects/{projectName}.md`에 반영

---

**위키 링크**: `[[projects/notepad]]`, `[[projects/mailer]]` 등으로 프로젝트 상호 링크 가능
