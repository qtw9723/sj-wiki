# Teams 메일 → Gmail → Google Calendar Gemini 자동화 연동 조사

조사일: 2026-06-12
출처: 대화 + 웹 서칭 (Claude Code)

## 배경

팀즈에서 회의 초대·변경 시 이메일(+ .ics 첨부)이 옴.
이를 Gmail로 자동 전달해서 Gemini AI가 Google Calendar에 자동 등록하는 방법 조사.

## 전체 흐름

Teams 회의 초대 이메일 (+ .ics 첨부)
  → Outlook 수신
  → 자동 전달 규칙 (Outlook 규칙)
  → Gmail
  → Gemini AI 감지
  → Google Calendar 자동 등록

## Gemini + Gmail 캘린더 자동 등록 방식

### 방법 1: .ics 첨부 감지 (기존 기능)
- Teams 초대 이메일에는 항상 .ics 파일이 첨부됨
- Gmail이 이를 감지하면 이메일 상단에 "캘린더에 추가" 버튼 표시
- 클릭 한 번으로 Google Calendar 등록

### 방법 2: Gemini 텍스트 분석 (신기능)
- 첨부 없어도 Gemini가 본문에서 날짜·시간·장소·링크를 읽어 "Add to Calendar" 제안
- 정확도 약 92~95%

### 방법 3: Google Calendar 자동 초대 추가 설정
- Google Calendar → 설정 → 이벤트 설정 → "내 캘린더에 초대 추가" → "모든 사람"
- 클릭 없이 Gmail에 도착한 초대가 자동 등록됨

## Outlook 자동 전달 설정

### OWA(Outlook 웹)에서 규칙 만들기 (권장)
- 조건: 메시지 유형 = 회의 초대 또는 업데이트
- 작업: 전달 대상 → Gmail 주소
- 참고: 새 Outlook 데스크톱은 고급 규칙이 제거돼 OWA 권장

### 새 Outlook 데스크톱 우회법
- 조건: 제목에 "초대" OR "변경" 포함 + 첨부 파일 있음
- 작업: 전달 대상 → Gmail

## 제한사항

- 회사 IT 정책으로 외부 도메인 전달 차단 가능 → 먼저 확인 필수
- Gmail에서 수락/거절해도 Teams 쪽에 응답이 안 감 → 읽기 전용 참고용으로 사용
- Google Workspace 또는 Google One AI Premium 플랜이어야 Gemini 기능 풀 지원
- "대체 이메일 주소로 전달된 초대에 응답 허용" 설정도 함께 켜야 함

## 설정 순서 (요약)

1. Google Calendar → 설정 → "내 캘린더에 초대 추가" → 모든 사람
2. "대체 이메일 주소로 전달된 초대에 응답 허용" 체크
3. OWA에서 회의 초대/업데이트 → Gmail 자동 전달 규칙 생성 (IT 정책 확인 후)
4. Teams 테스트 초대로 Gmail → Calendar 자동 등록 확인

## 참고 링크

- https://sider.ai/blog/ai-tools/use-gemini-in-gmail-to-add-calendar-events-automatically-so-you-stop-missing-stuff
- https://blog.google/products-and-platforms/products/workspace/help-me-schedule-gmail-gemini/
- https://spin.atomicobject.com/set-up-rule-forward/
- https://support.google.com/calendar/answer/37135
