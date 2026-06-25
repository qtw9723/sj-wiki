---
title: 모닝 브리핑 — Google Apps Script (데일리/위클리 자동 발송)
category: 도구/스킬
tags: [자동화, apps-script, gemini, gmail, google-calendar, 브리핑, 리포팅]
source: raw/모닝-브리핑-AppsScript.md (사용자 전달 2026-06-24)
created: 2026-06-24
updated: 2026-06-24
---

> [!tip] 핵심 takeaway
> 🧠 매일 아침 받는 **"DAILY BRIEFING" 메일의 정체** = 개인 구글 계정에서 도는 **Google Apps Script**. 시간 기반 트리거로 스케줄 → 기본 캘린더(오늘 일정) + Gmail 받은편지함을 읽어 → **개인 Gemini(무료분) `gemini-2.5-flash`** 로 메일을 요약·일정 추천 → HTML 메일 발송 + 구글 드라이브 저장.
> 🧠 [[Teams-Gmail-캘린더-Gemini-연동]]이 "회사 메일·일정을 구글로 모으는 **수집층**"이라면, 이건 그 위에서 도는 **소비·푸시층** — 두 개가 합쳐져 "회사 일정/메일이 매일 아침 요약돼 온다"가 완성된다.
> 🧠 [[내-프로필]]의 "크론탭+메일 보고서" 자동화 DNA가 SaaS(Apps Script+Gemini)로 재현된 형태. [[schedule-reporter-kakao]]와 같은 패턴, 채널만 다름(여긴 메일+드라이브).

> [!warning] 보안 — API 키
> ⚠️ 실제 Gemini API 키는 **이 위키에 두지 않는다**. Apps Script **스크립트 속성(`GEMINI_API_KEY`)** 에만 저장하고, 코드에는 `PropertiesService`로 로드만 한다.
> 📄 2026-06-24 채팅으로 키 평문이 노출된 적 있음 → **해당 키 폐기·재발급 권고**(아래 할 일).

## 어떻게 받고 있나 (동작 흐름) 📄

```
시간 트리거(Apps Script)
  ├─ [데일리] sendDailySummaryReport()  — 평일만(주말·한국 공휴일 제외)
  │     ├─ 오늘 일정 수집  (CalendarApp 기본 캘린더, 00:00~23:59)
  │     ├─ 메일 수집      (GmailApp, in:inbox / 월요일은 직전 3일·그 외 1일)
  │     ├─ Gemini 요약    (gemini-2.5-flash, 재시도 2→4→8s)
  │     │     → ✉️ 주요 메일 요약  +  💡 일정 등록 추천
  │     ├─ 메일 발송      (MailApp → sjpark@mindwareworks.com)
  │     └─ 드라이브 저장  (MWW/데일리 브리핑 보고서/[Daily Briefing] yyyy-MM-dd.html)
  └─ [위클리] sendWeeklyScheduleReport() — 이번 주 월~일 일정만 (Gemini 미사용)
        ├─ 메일 발송      (WEEKLY BRIEFING)
        └─ 드라이브 저장  (MWW/주간 일정 보고서/...)
```

## 구성 요소 📄

| 요소 | 내용 |
|------|------|
| 실행 환경 | **Google Apps Script** (개인 구글 계정), 시간 기반 트리거로 스케줄 |
| 일정 소스 | `CalendarApp.getDefaultCalendar()` — 개인 구글 캘린더(=회사 일정 구독본 포함, [[Teams-Gmail-캘린더-Gemini-연동]] B1) |
| 메일 소스 | `GmailApp.search("after:... in:inbox")` — 받은편지함(=회사 메일 자동전달분 포함, A2) |
| AI 요약 | **개인 Gemini API, 무료분만** 사용 · 모델 `gemini-2.5-flash` |
| 수신처 | `sjpark@mindwareworks.com` (회사 메일) |
| 산출물 | ① HTML 메일 발송 ② 구글 드라이브 `MWW/<하위폴더>` 에 HTML 저장 |
| 키 보관 | 스크립트 속성 `GEMINI_API_KEY` (`PropertiesService`) |

## 데일리 브리핑 메일 구성 📄
- 헤더: `DAILY BRIEFING` + 날짜 (다크 배경 #1a1a1a, 포인트 #deff9a)
- `📅 오늘 해야 할 일정` — 시작시각 + 제목
- `✉️ 주요 메일 요약` — Gemini가 **광고·뉴스레터·스팸·시스템 알림 제외**, 실제 업무 메일만 선별 요약
- `💡 일정 등록 추천` — 메일에서 일정화할 만한 건 + 제안 일시
- 푸터: "AI 비서가 자동 생성"

## 설계 포인트 (눈여겨볼 점) 🧠
- 📄 **발송 안 하는 조건이 명확**: 주말·공휴일 skip, 키 없으면 중단, **Gemini 요약 실패 시 메일·드라이브 저장 자체를 건너뜀**(빈/오류 브리핑 방지). 메일 0건은 실패가 아니라 "새 메일 없음"으로 정상 발송.
- 📄 **재시도/백오프**: 429·500·503·네트워크 오류(`-1`) 시 `2000 * 2^(attempt-1)` = 2s→4s→8s, 최대 4회(`muteHttpExceptions:true`로 예외 대신 코드 분기). → 무료 분량 rate limit 대응.
- 📄 **월요일 보정**: 주말 메일을 놓치지 않게 월요일엔 직전 3일치 메일 수집(`diffDays = dayOfWeek===1 ? 3 : 1`).
- 📄 **메일 수집 단위 = 토큰 절약형**: 스레드별 **마지막 메시지**만(`getMessages().pop()`) 추려, 제목·발신자·날짜 + 본문 **앞 300자 snippet**(개행 제거)만 JSON으로 Gemini에 전달. 전문이 아니라 요약 입력만 보냄 → 무료분 절약.
- 📄 **구조화 출력 파싱**: 프롬프트에서 `---1---`/`---2---` 구분자를 강제해 응답을 메일요약/일정추천 두 덩어리로 split. 프롬프트 역할은 "전문 경영 컨설턴트 비서", 광고·뉴스레터·스팸·시스템 알림은 무시하라고 지시.
- 📄 **위클리는 요일별 그룹핑**(Gemini 미사용): 이번 주 월~일 이벤트를 날짜별로 묶어 `MM/dd (요일)` 라벨 + 시간순 정렬, 종일 일정은 `종일`로 표기.
- 📄 **드라이브 저장은 폴더 자동 생성**: `MWW`(없으면 생성) → 하위 `데일리 브리핑 보고서`/`주간 일정 보고서`(없으면 생성)에 HTML 파일로 적재. 저장 실패는 try/catch로 로그만 남기고 메일 발송은 막지 않음.
- 🧠 ⚠️ 코드에 `diagnoseGemini()`가 `gemini-3.5-flash`(존재하지 않는 모델명)를 참조 — 진단 함수라 실발송엔 무관하나, 진단 시 404날 수 있음. 실제 발송은 `gemini-2.5-flash`로 정상.
- 📄 진단/유틸 함수 별도 존재: `setGeminiKey()`(키 1회 주입), `checkKey()`(키 길이·앞 4자 로그), `diagnoseGemini()`(사용 가능 모델 목록 조회 + 최소 요청 테스트) — 운영 발송엔 무관한 보조 도구.

## 할 일 / 개선 후보 🧠
- 🔴 **(보안) 노출된 Gemini 키 폐기·재발급** 후 스크립트 속성만 갱신 (2026-06-24 채팅 노출분).
- 🧠 무료 분량 한계로 요약 실패가 잦으면: 모델 다운시프트/배치 축소 또는 유료 키 검토.
- 🧠 `diagnoseGemini()`의 모델명을 `gemini-2.5-flash`로 교정.
- 🧠 같은 결과를 카카오로도 밀어주고 싶으면 [[카카오-Play-MCP]]·[[schedule-reporter-kakao]] 패턴과 결합 가능.

## 의외의 연결점 🧠
- 🧠 [[Teams-Gmail-캘린더-Gemini-연동]]은 **온디맨드**(내가 Gemini에게 물어봄), 이 Apps Script는 **푸시**(매일 아침 자동으로 옴) — 같은 데이터(Gmail+캘린더) 위의 두 소비 방식. 둘이 같이 굴러간다.
- 🧠 [[schedule-reporter-kakao]]·[[mailer]]의 "스케줄→요약→발송" 자동화와 동일 골격. 코드 없이가 아니라 **Apps Script로 가볍게** 구현한 점이 다름.
- 🧠 [[에이전트-자동화-도구]]의 routines/스케줄 발상과 정확히 같은 문제(정기 리포팅).

## 관련 문서
- [[Teams-Gmail-캘린더-Gemini-연동]] — 이 브리핑이 읽는 Gmail·구글 캘린더를 채우는 수집층
- [[schedule-reporter-kakao]] · [[mailer]] — 같은 리포팅 자동화 패턴(다른 채널)
- [[에이전트-자동화-도구]] — 정기 리포팅/스케줄 발상
- [[내-프로필]] — 크론+메일 보고서 자동화 DNA
