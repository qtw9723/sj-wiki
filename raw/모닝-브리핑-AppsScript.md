# 모닝 브리핑 — Google Apps Script 원본 (사용자 전달, 2026-06-24)

> ⚠️ **API 키 redact됨**: 사용자가 전달한 원본 `setGeminiKey()`에는 실제 Gemini API 키가 들어 있었으나, 동기화 저장소(클라우드) 보안을 위해 `<REDACTED>` 로 치환해 보관한다. 실제 키는 Apps Script **스크립트 속성(`GEMINI_API_KEY`)** 에만 둔다. (채팅 노출되어 폐기·재발급 권고함)

## 사용자 전달 사실 (2026-06-24)
1. **구글 Apps Script**로 스케줄(시간 기반 트리거) 돌려 자동 발송.
2. **개인 Gemini API 키, 무료 분량만** 사용.
3. 소스코드 = 아래(키 redact).

## 소스코드 (key redacted)

```javascript
function setGeminiKey() {
  PropertiesService.getScriptProperties().setProperty('GEMINI_API_KEY', '<REDACTED>');
}
/**
 * 데일리/위클리 업무 브리핑 자동 발송 + 드라이브 저장 v3.0
 * - Gemini 요약(재시도 포함), 실패 시 메일 미발송
 * - API 키는 스크립트 속성(GEMINI_API_KEY)에서 로드
 */
const RECIPIENT = "sjpark@mindwareworks.com";
const GEMINI_MODEL = "gemini-2.5-flash"; // models 목록에 존재하는 모델 사용

// ── 데일리 브리핑 ──
function sendDailySummaryReport() {
  const GEMINI_API_KEY = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  const today = new Date();
  const dayOfWeek = today.getDay();
  // 1. 주말 제외
  if (dayOfWeek === 0 || dayOfWeek === 6) return;
  // 2. 공휴일 제외 (한국 공휴일 캘린더 조회)
  const holidayCal = CalendarApp.getCalendarById("ko.south_korea#holiday@group.v.calendar.google.com");
  if (holidayCal && holidayCal.getEventsForDay(today).length > 0) return;
  // --- 오늘 일정 수집 (기본 캘린더) ---
  // events → scheduleHtml (시작시각 + 제목)
  // --- 메일 수집: 월요일은 직전 3일치, 그 외 1일치, in:inbox ---
  //   thread별 제목/발신/snippet(300자)/날짜 수집 → emailData[]
  // --- Gemini 분석 (callGeminiForHtml, 재시도 포함) ---
  //   키 없으면 중단(메일 미발송). 메일 0건이면 "새 메일 없음"으로 정상 발송.
  //   aiReport.ok=false면 메일/드라이브 저장 건너뜀.
  // --- HTML 메일 템플릿: DAILY BRIEFING (날짜) ---
  //   📅 오늘 해야 할 일정 / ✉️ 주요 메일 요약 / 💡 일정 등록 추천
  // [액션1] MailApp.sendEmail(RECIPIENT, "[Daily Briefing] 오늘 아침 업무 요약입니다", htmlBody)
  // [액션2] saveToDrive("데일리 브리핑 보고서", "[Daily Briefing] yyyy-MM-dd.html", htmlBody)
}

// ── Gemini 호출 (재시도 + 성공여부 반환) ──
function callGeminiForHtml(emailData, apiKey) {
  // POST https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key=...
  // 프롬프트: "전문 경영 컨설턴트 비서" — 광고/뉴스레터/스팸/시스템알림 제외, 실제 업무 메일만 선별.
  //   출력 양식: ---1--- (메일 요약 <li>) / ---2--- (일정 등록 추천 <li>) 구분자 포함 HTML.
  // 재시도: 429/500/503/네트워크 오류 시 백오프 2s→4s→8s, 최대 4회.
  // 응답 파싱: candidates[0].content.parts[0].text 를 /---[12]---/ 로 split → {summary, recommendation}
  // 반환: { ok, summary, recommendation } 또는 { ok:false, error }
}

// ── 위클리 브리핑 (Gemini 미사용, 일정만) ──
function sendWeeklyScheduleReport() {
  // 이번 주 월~일 기본 캘린더 일정 수집 → 요일별 그룹핑(종일/시간대)
  // HTML: WEEKLY BRIEFING (월~일 범위) / 🗓 이번 주 일정
  // MailApp.sendEmail(RECIPIENT, "[Weekly Briefing] 이번 주 일정 요약입니다 (MM/dd~MM/dd)", htmlBody)
  // saveToDrive("주간 일정 보고서", "[Weekly Briefing] yyyy-MM-dd.html", htmlBody)
}

// ── 공통: 구글 드라이브 MWW/<하위폴더>에 HTML 저장 ──
function saveToDrive(subName, fileName, htmlBody) {
  // DriveApp: "MWW" 부모 폴더(없으면 생성) > subName 하위폴더 > createFile(fileName, htmlBody, HTML)
}

// ── 진단용 ──
function diagnoseGemini() {
  // (1) GET /v1beta/models?key=... → 사용 가능 모델 목록 로깅
  // (2) {MODEL}:generateContent 에 "1+1은?" 최소 요청 → 응답코드/본문 로깅
}
function checkKey() {
  // 스크립트 속성 GEMINI_API_KEY 존재/길이/앞4자 로깅
}
```

> 전체 원본 코드(주석·HTML 템플릿 풀버전)는 채팅으로 전달받음. 위 요약은 핵심 흐름만 남기고 키·장문 HTML은 압축. 필요 시 사용자 보관본 참조.
