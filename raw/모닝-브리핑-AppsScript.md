# 모닝 브리핑 — Google Apps Script 원본 (사용자 전달, 2026-06-24)

> ⚠️ **API 키만 redact됨**: 아래는 사용자가 전달한 **원본 소스 전체**다. `setGeminiKey()`의 실제 Gemini API 키만 `<REDACTED>`로 가렸고(동기화 저장소 보안), 나머지는 원문 그대로 보존한다. 실제 키는 Apps Script **스크립트 속성(`GEMINI_API_KEY`)** 에만 둔다. (채팅 노출되어 폐기·재발급 권고함)

## 사용자 전달 사실 (2026-06-24)
1. **구글 Apps Script**로 스케줄(시간 기반 트리거) 돌려 자동 발송.
2. **개인 Gemini API 키, 무료 분량만** 사용.
3. 소스코드 = 아래(키만 redact, 그 외 원문 그대로).

## 소스코드 (원문 그대로 · 키만 redact)

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

  // 2. 공휴일 제외
  const holidayCal = CalendarApp.getCalendarById("ko.south_korea#holiday@group.v.calendar.google.com");
  if (holidayCal && holidayCal.getEventsForDay(today).length > 0) return;

  // --- 오늘 일정 수집 ---
  const startOfDay = new Date(today.setHours(0, 0, 0, 0));
  const endOfDay = new Date(today.setHours(23, 59, 59, 999));
  const events = CalendarApp.getDefaultCalendar().getEvents(startOfDay, endOfDay);

  let scheduleHtml = "";
  if (events.length === 0) {
    scheduleHtml = `<p style="color: #666; font-style: italic;">오늘 예정된 일정이 없습니다.</p>`;
  } else {
    events.forEach(event => {
      const start = Utilities.formatDate(event.getStartTime(), Session.getScriptTimeZone(), "HH:mm");
      scheduleHtml += `
        <div style="margin-bottom: 10px; padding: 10px; border-left: 4px solid #deff9a; background: #f9f9f9;">
          <strong style="color: #333;">[${start}]</strong> ${event.getTitle()}
        </div>`;
    });
  }

  // --- 메일 데이터 수집 (월요일은 직전 3일치) ---
  const diffDays = (dayOfWeek === 1) ? 3 : 1;
  const startTime = new Date(new Date().getTime() - (diffDays * 24 * 60 * 60 * 1000));
  const afterQuery = Utilities.formatDate(startTime, Session.getScriptTimeZone(), "yyyy/MM/dd");

  const threads = GmailApp.search(`after:${afterQuery} in:inbox`);
  let emailData = [];
  threads.forEach(thread => {
    const lastMsg = thread.getMessages().pop();
    emailData.push({
      subject: thread.getFirstMessageSubject(),
      from: lastMsg.getFrom(),
      snippet: lastMsg.getPlainBody().substring(0, 300).replace(/\n/g, " "),
      date: Utilities.formatDate(lastMsg.getDate(), Session.getScriptTimeZone(), "MM/dd HH:mm")
    });
  });
  Logger.log(`수집 메일 ${emailData.length}건`);

  // --- AI 분석 (Gemini, 재시도 포함) ---
  let aiReport;
  if (!GEMINI_API_KEY) {
    Logger.log("중단: GEMINI_API_KEY 미설정 — 메일 발송 안 함.");
    return;
  } else if (emailData.length === 0) {
    // 메일 없음은 실패가 아니므로 정상 발송
    aiReport = {
      ok: true,
      summary: "<li style='list-style:none;'>새로 온 메일이 없습니다.</li>",
      recommendation: "<li style='list-style:none;'>분석할 데이터가 없습니다.</li>"
    };
  } else {
    aiReport = callGeminiForHtml(emailData, GEMINI_API_KEY);
  }

  // ★ 재시도 끝에 AI 요약이 실패하면 메일/드라이브 저장 건너뜀
  if (!aiReport.ok) {
    Logger.log("Gemini 요약 실패 — 메일/드라이브 저장 건너뜀. 사유: " + aiReport.error);
    return;
  }

  // --- HTML 메일 템플릿 ---
  const dateString = Utilities.formatDate(new Date(), "GMT+9", "yyyy년 MM월 dd일");
  const htmlBody = `
  <div style="font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; color: #333;">
    <div style="background: #1a1a1a; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
      <h1 style="color: #deff9a; margin: 0; font-size: 24px;">DAILY BRIEFING</h1>
      <p style="color: #fff; margin: 10px 0 0; font-size: 14px;">${dateString}</p>
    </div>
    <div style="padding: 20px;">
      <h2 style="border-bottom: 2px solid #1a1a1a; padding-bottom: 5px; font-size: 18px;">📅 오늘 해야 할 일정</h2>
      ${scheduleHtml}
      <h2 style="border-bottom: 2px solid #1a1a1a; padding-bottom: 5px; font-size: 18px; margin-top: 30px;">✉️  주요 메일 요약</h2>
      <ul style="padding-left: 20px; line-height: 1.6;">
        ${aiReport.summary}
      </ul>
      <h2 style="border-bottom: 2px solid #1a1a1a; padding-bottom: 5px; font-size: 18px; margin-top: 30px; color: #2c3e50;">💡 일정 등록 추천</h2>
      <ul style="padding-left: 20px; line-height: 1.6; color: #2c3e50;">
        ${aiReport.recommendation}
      </ul>
    </div>
    <div style="text-align: center; font-size: 12px; color: #999; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
      본 메일은 상준 님의 업무 효율을 위해 AI 비서가 자동 생성했습니다.
    </div>
  </div>`;

  // [액션 1] 메일 발송
  MailApp.sendEmail({ to: RECIPIENT, subject: `[Daily Briefing] 오늘 아침 업무 요약입니다`, htmlBody });

  // [액션 2] 구글 드라이브 저장
  saveToDrive("데일리 브리핑 보고서", `[Daily Briefing] ${Utilities.formatDate(new Date(), "GMT+9", "yyyy-MM-dd")}.html`, htmlBody);
}

// ── Gemini 호출 (재시도 + 성공여부 반환) ──
function callGeminiForHtml(emailData, apiKey) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`;
  const prompt = `너는 전문 경영 컨설턴트 비서야. 이메일 데이터를 분석해서 아래 [출력 양식]에 맞춰 HTML 형태로만 답변해줘.

  [분석 지침]
  1. 광고, 뉴스레터, 스팸, 단순 시스템 알림 등 '업무와 무관한 메일'은 완전히 무시하고, '실제 업무와 관련된 메일'만 선별해서 요약해.
  2. 메일 제목과 요약 내용이 한눈에 구분되도록 굵기와 줄바꿈, 색상을 명확히 분리해서 적용해.

  [출력 양식] (반드시 아래 구분자 ---1--- 과 ---2--- 를 포함해서 출력)
  ---1---
  <li style="margin-bottom: 18px; list-style: none;">
    <div style="font-weight: bold; font-size: 15px; color: #1a1a1a; margin-bottom: 6px;">📩 [메일 제목]</div>
    <div style="font-size: 14px; color: #555; padding-left: 24px; line-height: 1.5;">- 요약 내용...</div>
  </li>
  (업무 메일이 없으면 <li style="list-style: none;"><div style="color:#666;">새로운 업무 메일이 없습니다.</div></li> 출력)
  ---2---
  <li style="margin-bottom: 18px; list-style: none;">
    <div style="font-weight: bold; font-size: 15px; color: #2c3e50; margin-bottom: 6px;">💡 [추천 일정 제목]</div>
    <div style="font-size: 14px; color: #555; padding-left: 24px; line-height: 1.5;">- 이유 및 제안 일시...</div>
  </li>
  (추천 일정이 없으면 <li style="list-style: none;"><div style="color:#666;">추천할 일정이 없습니다.</div></li> 출력)

  분석 데이터: ${JSON.stringify(emailData)}`;

  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    muteHttpExceptions: true
  };

  // 일시 오류(429/500/503/네트워크)면 백오프 후 재시도: 2s → 4s → 8s
  const MAX = 4;
  let responseCode = 0, responseText = "";
  for (let attempt = 1; attempt <= MAX; attempt++) {
    try {
      const response = UrlFetchApp.fetch(url, options);
      responseCode = response.getResponseCode();
      responseText = response.getContentText();
    } catch (e) {
      responseCode = -1;
      responseText = e.toString();
    }
    if (responseCode === 200) break;
    const transient = (responseCode === 429 || responseCode === 500 || responseCode === 503 || responseCode === -1);
    if (transient && attempt < MAX) {
      Logger.log(`Gemini ${responseCode} — 재시도 ${attempt}/${MAX - 1}`);
      Utilities.sleep(2000 * Math.pow(2, attempt - 1));
      continue;
    }
    break;
  }

  if (responseCode !== 200) {
    return { ok: false, error: `HTTP ${responseCode} — ${responseText}` };
  }

  try {
    const json = JSON.parse(responseText);
    if (!json.candidates || !json.candidates[0].content) {
      return { ok: false, error: "응답 차단/빈 응답 — " + responseText };
    }
    const resultText = json.candidates[0].content.parts[0].text;
    const parts = resultText.split(/---[12]---/);
    return {
      ok: true,
      summary: parts[1] ? parts[1].trim() : "<li style='list-style:none; color:#666;'>요약 내용이 없습니다.</li>",
      recommendation: parts[2] ? parts[2].trim() : "<li style='list-style:none; color:#666;'>추천할 일정이 없습니다.</li>"
    };
  } catch (e) {
    return { ok: false, error: "파싱 오류 — " + e.toString() };
  }
}

// ── 위클리 브리핑 (Gemini 미사용, 일정만) ──
function sendWeeklyScheduleReport() {
  const TZ = Session.getScriptTimeZone();
  const now = new Date();

  // 이번 주 월요일 00:00 ~ 일요일 23:59:59
  const dayOfWeek = now.getDay();
  const daysSinceMonday = (dayOfWeek === 0) ? 6 : dayOfWeek - 1;
  const monday = new Date(now);
  monday.setDate(now.getDate() - daysSinceMonday);
  monday.setHours(0, 0, 0, 0);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  sunday.setHours(23, 59, 59, 999);

  const events = CalendarApp.getDefaultCalendar().getEvents(monday, sunday);
  const dayNames = ["일", "월", "화", "수", "목", "금", "토"];
  let scheduleHtml = "";

  if (events.length === 0) {
    scheduleHtml = `<p style="color: #666; font-style: italic;">이번 주 등록된 일정이 없습니다.</p>`;
  } else {
    const byDay = {};
    events.forEach(event => {
      const key = Utilities.formatDate(event.getStartTime(), TZ, "yyyy-MM-dd");
      (byDay[key] = byDay[key] || []).push(event);
    });
    for (let i = 0; i < 7; i++) {
      const day = new Date(monday);
      day.setDate(monday.getDate() + i);
      const key = Utilities.formatDate(day, TZ, "yyyy-MM-dd");
      const dayItems = byDay[key];
      if (!dayItems || dayItems.length === 0) continue;

      const label = Utilities.formatDate(day, TZ, "MM/dd") + " (" + dayNames[day.getDay()] + ")";
      scheduleHtml += `<div style="margin: 18px 0 6px; font-weight: bold; font-size: 15px; color: #1a1a1a;">📌 ${label}</div>`;
      dayItems.sort((a, b) => a.getStartTime() - b.getStartTime());
      dayItems.forEach(event => {
        let timeLabel;
        if (event.isAllDayEvent()) {
          timeLabel = "종일";
        } else {
          const s = Utilities.formatDate(event.getStartTime(), TZ, "HH:mm");
          const e = Utilities.formatDate(event.getEndTime(), TZ, "HH:mm");
          timeLabel = `${s}~${e}`;
        }
        scheduleHtml += `
          <div style="margin-bottom: 8px; padding: 10px; border-left: 4px solid #deff9a; background: #f9f9f9;">
            <strong style="color: #333;">[${timeLabel}]</strong> ${event.getTitle()}
          </div>`;
      });
    }
  }

  const rangeString = Utilities.formatDate(monday, "GMT+9", "yyyy년 MM월 dd일") + " ~ " + Utilities.formatDate(sunday, "GMT+9", "MM월 dd일");
  const htmlBody = `
  <div style="font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; color: #333;">
    <div style="background: #1a1a1a; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
      <h1 style="color: #deff9a; margin: 0; font-size: 24px;">WEEKLY BRIEFING</h1>
      <p style="color: #fff; margin: 10px 0 0; font-size: 14px;">${rangeString}</p>
    </div>
    <div style="padding: 20px;">
      <h2 style="border-bottom: 2px solid #1a1a1a; padding-bottom: 5px; font-size: 18px;">🗓 이번 주 일정</h2>
      ${scheduleHtml}
    </div>
    <div style="text-align: center; font-size: 12px; color: #999; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
      본 메일은 상준 님의 업무 효율을 위해 AI 비서가 자동 생성했습니다.
    </div>
  </div>`;

  MailApp.sendEmail({
    to: RECIPIENT,
    subject: `[Weekly Briefing] 이번 주 일정 요약입니다 (${Utilities.formatDate(monday, "GMT+9", "MM/dd")}~${Utilities.formatDate(sunday, "GMT+9", "MM/dd")})`,
    htmlBody
  });

  saveToDrive("주간 일정 보고서", `[Weekly Briefing] ${Utilities.formatDate(monday, "GMT+9", "yyyy-MM-dd")}.html`, htmlBody);
}

// ── 공통: MWW/<하위폴더>에 HTML 저장 ──
function saveToDrive(subName, fileName, htmlBody) {
  try {
    const parentName = "MWW";
    let parentFolders = DriveApp.getFoldersByName(parentName);
    let parentFolder = parentFolders.hasNext() ? parentFolders.next() : DriveApp.createFolder(parentName);
    let subFolders = parentFolder.getFoldersByName(subName);
    let targetFolder = subFolders.hasNext() ? subFolders.next() : parentFolder.createFolder(subName);
    targetFolder.createFile(fileName, htmlBody, MimeType.HTML);
    Logger.log(`구글 드라이브 [${parentName} > ${subName}] 저장 성공: ${fileName}`);
  } catch (e) {
    Logger.log("구글 드라이브 저장 실패: " + e.toString());
  }
}

function diagnoseGemini() {
  const key = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');

  // (1) 내 키로 실제 사용 가능한 모델 목록
  const list = UrlFetchApp.fetch(
    `https://generativelanguage.googleapis.com/v1beta/models?key=${key}`,
    { muteHttpExceptions: true });
  Logger.log("=== 사용 가능 모델 ===\n" + list.getContentText());

  // (2) 현재 모델에 '최소' 요청(메일 데이터 없이)
  const MODEL = "gemini-3.5-flash";
  const r = UrlFetchApp.fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${key}`,
    { method: "post", contentType: "application/json", muteHttpExceptions: true,
      payload: JSON.stringify({ contents: [{ parts: [{ text: "1+1은?" }] }] }) });
  Logger.log(`=== 최소 요청 (${MODEL}) ===\n` + r.getResponseCode() + "\n" + r.getContentText());
}

function checkKey(){
  const k = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  Logger.log(k ? `길이=${k.length}, 앞4자="${k.substring(0,4)}"` : "NULL(미설정)");
}
```
