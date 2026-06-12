---
title: 작업 이력 (Log)
category: 시스템
tags: [log, 이력]
created: 2026-06-10
updated: 2026-06-10
---

> [!tip] 핵심 takeaway
> 위키에 무슨 일이 있었는지 시간순으로 쌓는 기록장. 최신 항목이 맨 위.
> 형식: `## [날짜] 운영유형 | 제목` (운영유형: 자료넣기 / 질문 / 건강검진 / 셋업)
> ⚠️ 이 vault는 **동기화 대상(개인/포트폴리오)**. 회사 기밀 이력은 PC 전용 `sj-wiki-work` vault의 log에 있다.

---

## [2026-06-12] 자료넣기 | Teams→Gmail→Calendar Gemini 연동 조사 위키화
- 대화+서칭 결과 → `raw/Teams-Gmail-캘린더-Gemini-연동.md` 저장.
- `wiki/Teams-Gmail-캘린더-Gemini-연동.md` 신규 작성 (.ics 감지·Gemini 분석·자동 초대 추가 3가지 방식, OWA 규칙 설정, 체크리스트).
- `wiki/index.md` 도구/스킬 카테고리에 등록.

## [2026-06-12] 자료넣기 | 교회 개발팀 백엔드 회의 위키화
- 대화 기반 회의 내용 → `raw/교회-개발-백엔드-회의-2026-06-12.md` 저장(회사 아닌 교회 사이드 프로젝트 → 개인 vault 적합, `raw/meetings/` gitignore 회피해 raw 루트에 플랫 저장).
- `wiki/교회-백엔드-회의-2026-06-12.md` 신규 작성 (현황·개인 브랜치 전략·app/docs 문서화·Vercel용 개인 Git 배포·액션아이템). 📄/🧠 구분 표기.
- `wiki/index.md` "회의록" 카테고리 첫 등록(기존 "없음" 대체).
- 투두메이트 "교회-개발"에 다음 회의(2026-06-17 수 21:00) 등록 완료.
- claude.ai 원격 에이전트 `trig_01N49aP6vcKKxFJpzCb1nbpX` 생성: 매일 10:00 KST.
- 동작: git pull → CLAUDE.md 규칙대로 위키화 → git push → KakaotalkChat MemoChat 리포트.
- `wiki/웹-크롤링-기초.md` 전체 파이프라인 다이어그램 갱신.

## [2026-06-12] 셋업 | 크롤러 멀티에이전트 소스 추가 + NaverSearch 재활성화
- `D:\Projects\ai-crawler\crawler.py`: RSS 소스 6→9개 추가 (LangChain Blog, Microsoft Research, arXiv cs.MA), 멀티에이전트 키워드 10개 추가.
- claude.ai 원격 에이전트(`trig_0135s5oX7Xm2gn3NTrgXXQXM`): "멀티에이전트", "에이전트 AI" 키워드 추가 + auto_disabled 상태 재활성화.
- `wiki/웹-크롤링-기초.md` 시스템 현황 갱신.

## [2026-06-12] 자료넣기 | AI 주간 소식 W24 보강 + 크롤링↔주간소식 교차참조
- 수동 보강(사용자 요청)과 18:06 자동 위키화가 같은 페이지를 보강 → rebase 충돌을 정보 보존 방향으로 병합 해결.
- `wiki/AI-주간-소식-2026-W24.md`: raw 23건 중 누락분 반영 — HF Spaces 체이닝 에이전트·Nemotron 3.5 Content Safety는 본문 추가(에이전트/안전 섹션), Gemini RCT(시에라리온)·MIT RAISE PATH는 본문 전체 서술, LSEG·MIT 윤리 심포지엄은 "그 외 수집 항목"으로 기록(Oracle Cloud는 본문에 기존재).
- 의외의 연결점 교차참조: W24 다이제스트가 [[웹-크롤링-기초]]의 ai-crawler 첫 산출물임을 양쪽 페이지에 상호 링크.
- `index.md`는 변경 없음(두 페이지 모두 기등록).

## [2026-06-12] 자료넣기 | AI 주간 소식 W24 위키화
- `raw/ai-digest/2026-06-12.md` (RSS 수집 23건) 기반으로 `wiki/AI-주간-소식-2026-W24.md` 작성.
- 주요 내용: OpenAI IPO S-1 · Codex+GPT-5.5 실사례(Nextdoor·Notion) · Gemma 4 12B · 멀티에이전트 안전 $10M.
- 앞으로 주간 단위로 `AI-주간-소식-YYYY-WXX.md` 형식으로 위키화 예정.
- `wiki/index.md` AI/업계 동향 카테고리에 등록.

## [2026-06-12] 자료넣기 | 웹 크롤링 기초 학습 + AI 뉴스 수집 시스템 구축
- 대화 기반 자료 → `raw/웹-크롤링-기초.md` 저장.
- `wiki/웹-크롤링-기초.md` 신규 작성 (RSS/API/BeautifulSoup/Playwright 4방식 + ai-crawler 시스템).
- Python RSS 크롤러(`D:\Projects\ai-crawler\crawler.py`) + Windows Task Scheduler(08:00 KST) 구축.
- Claude 원격 에이전트(NaverSearch MCP, 09:00 KST) 등록 — `trig_0135s5oX7Xm2gn3NTrgXXQXM`.
- `wiki/index.md` 도구/스킬 카테고리에 등록.

## [2026-06-12] 건강검진 | 위키 전체 점검 (15페이지)
- 고아 페이지·분류 누락 없음. 발견 문제 3건:
  - ⚠️ `Claude-Code-업데이트-동향` W23~W24(6/1~6/12) 2주치 stale — raw 자료 대기 중.
  - ⚠️ `내-MCP-커넥터-환경` macOS 환경 기재 → 현재 Windows 기기 사용 (확인 필요).
  - ✅ `schedule-reporter-kakao` 관련 문서에 `[[공통-기술스택]]` 교차참조 추가 (즉시 수정).

## [2026-06-10] 자료넣기 | 회사 전파사항 1건 → work vault로 라우팅 (이 vault 위키 변경 없음)
- `raw/meetings/2026-06-10_전파사항.md`(회사 프로젝트 전파사항)가 이 vault에 들어옴 → **기밀 분리 원칙(CLAUDE.md §1)에 따라 이 vault에는 위키화하지 않고** work vault(`sj-wiki-work`)로 복사 후 거기서 기존 페이지 4곳 보강(상세 이력은 work vault log).
- 이 vault 원본 파일은 읽기 전용 규칙대로 그대로 둠(`.gitignore`의 `raw/meetings/` 안전망으로 push 대상 아님). 🧠 권장: 원본은 work vault로 옮기고 이 vault에서는 삭제(사용자 작업).
- 클라우드 동기화를 위해 **회사 기밀을 PC 전용 `sj-wiki-work` vault로 분리**(A안).
- 이동: 회사 wiki 8p, 회사 raw(회의록·정의서·커넥터 원본 등), 기존 log 전체 → work vault.
- 정리(redaction): 개인 vault 잔존 페이지들의 회사 참조(회사 페이지 링크·사내 플랫폼 용어·로컬 경로)를 제거/일반화.
- 이 log는 개인 vault용으로 새로 시작. `.gitignore`·`CLAUDE.md`에 분리 원칙 반영.
- 결과: 이 vault에는 회사 기밀·동료 실명·내부 아키텍처·금액 정보 없음(검증 완료).
