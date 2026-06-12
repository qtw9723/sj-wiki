---
title: Teams → Gmail → Google Calendar Gemini 자동화
category: 도구/스킬
tags: [gmail, teams, google-calendar, gemini, 자동화, 일정관리, outlook]
source: raw/Teams-Gmail-캘린더-Gemini-연동.md
created: 2026-06-12
updated: 2026-06-12
---

> [!tip] 핵심 takeaway
> 🧠 Teams 회의 초대 이메일(.ics 첨부)을 Outlook 규칙으로 Gmail에 자동 전달하면 → Gemini가 감지해 Google Calendar에 클릭 없이 자동 등록 가능. **추가 앱·구독 없이** 구글 생태계로 회사 일정 통합하는 가장 가벼운 방법.
> 🧠 **선결과제**: 회사 IT 정책이 외부 도메인 자동 전달을 허용하는지 먼저 확인. 허용되면 OWA 규칙 1개로 구현 가능.
> 🧠 **한계**: 전달된 Gmail에서 수락/거절해도 Teams 쪽에 응답이 전달되지 않음 → 참고·열람 전용으로 운용하는 게 현실적.

---

## 전체 흐름 📄

```
Teams 회의 초대/변경 이메일 (+ .ics 첨부)
        │
        ▼
  회사 Outlook 받은편지함
        │  자동 전달 규칙 (OWA)
        ▼
      Gmail
        │  Gemini AI 감지 (.ics 또는 텍스트 분석)
        ▼
  Google Calendar 자동 등록
```

---

## Gmail → Calendar 자동 등록 방식 3가지

### ① .ics 첨부 감지 (기존, 가장 안정적) 📄
Teams 초대 이메일에는 항상 `.ics` 캘린더 파일이 첨부됨. Gmail이 이를 감지하면 이메일 상단에 **"캘린더에 추가"** 버튼이 표시되고 클릭 한 번으로 등록.

### ② Gemini 텍스트 분석 (신기능) 📄
첨부 없이 본문만 있어도 Gemini가 날짜·시간·장소·링크를 읽어 **"Add to Calendar"** 액션을 자동 제안. 정확도 약 92~95%.

> 🧠 Gemini 기능은 Google Workspace 또는 **Google One AI Premium** 플랜이어야 풀 지원. 일반 Gmail은 제한적.

### ③ Google Calendar 자동 초대 추가 설정 📄
**Google Calendar → 설정 → 이벤트 설정 → "내 캘린더에 초대 추가" → 모든 사람**
으로 켜두면 Gmail에 도착한 초대가 버튼 클릭 없이 자동 등록됨.

---

## Outlook 자동 전달 규칙 설정

### OWA(Outlook 웹 버전) — 권장 📄
새 Outlook 데스크톱은 고급 규칙이 제거됐으므로 OWA에서 만드는 것이 안정적.

1. Outlook Web → 설정 → 메일 → 규칙 → **새 규칙**
2. 조건: **메시지 유형 = 회의 초대 또는 업데이트**
3. 작업: **전달 대상 → qyw9723@gmail.com**

### 새 Outlook 데스크톱 우회법 🧠
"회의 초대" 조건이 없는 경우:
- 조건: **제목에 "초대" 또는 "변경" 포함** + **첨부 파일 있음**
- 작업: Gmail로 전달

---

## 설정 체크리스트

- [ ] 회사 IT 정책 확인 (외부 도메인 자동 전달 허용 여부)
- [ ] Google Calendar → "내 캘린더에 초대 추가" → **모든 사람** 설정
- [ ] Google Calendar → "대체 이메일 주소로 전달된 초대에 응답 허용" 체크
- [ ] OWA에서 회의 초대/업데이트 → Gmail 자동 전달 규칙 생성
- [ ] Teams 테스트 초대 발송 → Gmail 수신 → Calendar 자동 등록 확인

---

## 제한사항 & 주의사항

| 항목 | 내용 |
|------|------|
| IT 정책 | 회사에서 외부 자동 전달 차단 시 구현 불가 |
| 응답 처리 | Gmail에서 수락/거절해도 Teams 초대자에게 응답 전달 안 됨 |
| Gemini 플랜 | 일반 Gmail은 AI 기능 제한적 (Workspace/AI Premium 권장) |
| 변경 감지 | 회의 시간 변경 이메일도 동일하게 전달되면 자동 업데이트 적용 |

---

## 의외의 연결점

> 🧠 [[에이전트-자동화-도구]]·[[schedule-reporter-kakao]] 흐름과 같은 패턴: **이메일 트리거 → 파싱 → 캘린더 반영**. Gmail 수신을 트리거로 n8n/Zapier를 연결하면 수락 응답 자동화까지 가능 (고급 확장).
> 🧠 [[내-프로필]] — 반복 업무(일정 옮기기)를 자동화로 제거하는 접근. 개발 역량 쌓기보다는 "쓸 수 있는 도구 연결"로 즉시 효율화.

## 관련 문서
- [[에이전트-자동화-도구]] · [[schedule-reporter-kakao]] · [[카카오-Play-MCP]] · [[내-프로필]]
