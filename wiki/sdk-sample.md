---
title: sdk-sample
category: 프로젝트
tags: [프로젝트, 웹sdk, 챗봇, nodejs, 샘플, 개인프로젝트]
source: ~/IdeaProjects/sdk-sample (README, package.json, git log)
created: 2026-10-27
updated: 2026-10-27
---

> [!tip] 핵심 takeaway
> 🧠 **[[websdk-test]]에서 검증한 연동 지식을 "그대로 실행해 보고 옮겨 적는" 최소 예제로 증류한 고객 전달용 샘플.** 설정은 `config.js` 하나, 설명은 주석+README에 담아 비개발자도 따라 하게 만든 점이 핵심.
> 📄 2026-10-15~23 약 9일, 53커밋의 집중 개발.

## 문제 📄
- 챗봇 웹 SDK를 고객 웹페이지에 붙이는 방법을 보여줄 **최소 예제**가 필요했다(README). V2 웹SDK(`Cogbot`)와 XI SDK(`CGSDK`) 두 종류, 각각 인증/비인증.

## 내 역할
- 📄 저장소에 명시 없음. 🧠 사용자 확정(개인 프로젝트)으로 설계·구현·문서화 전체. 첫 커밋이 websdk-test v0.19.0 기반 축소판.

## 기능 📄
- 화면 2장: `v2.html`, `xi.html`. 구성은 같음: 구동 시 영역(봇 정보 → 첫 메시지 → 인증 → 연결), 실행 중 영역(text/data 보내기, action으로 받은 data 표시), 주고받은 데이터 기록창.
- 설정은 `config.js` 하나(host, botId, userKey/secure, apiKey, input 등). 요청마다 다시 읽어 서버 재시작 불필요, 문법 오류 시 직전 정상 설정 유지. 비밀은 `config.local.js`(gitignore)로 분리 가능.
- 화면 입력값이 config 기본값보다 우선, "config 값으로 되돌리기".
- JSON 입력칸 도우미(실시간 검사·오류 위치·정리 버튼·Tab·괄호 자동), 연결 전 영역 비활성+툴팁 안내, action 수신 시 테두리 깜빡임.
- XI 특성 반영: SDK 미정의 postfront 버튼 액션을 `CHAT_ACTION`으로 수신, XI는 text 필수(V2는 data만 가능), secure는 정확한 키로만 접근.
- README: 실행법, 화면 위치 표기(탭 › 영역 › 묶음 › 칸), API Key 발급 안내, 토큰 유효시간(60초) 등.

## 기술 📄
- Node 18+, Express 4, 정적 HTML/JS(`public/`), 서버는 화면 제공 + 브라우저용 설정 전달 + 토큰 발급 프록시(`server.js`). 포트 8080(충돌 시 안내).

## 진행 현황
- 📄 2026-10-23 마지막 커밋. 고객 전달 합의된 상태로 마무리(커밋 메시지). 이후 변경은 [[websdk-test]]에 반영 쪽으로 이동.

## 진행사항 업데이트 로그 (git log 기반) 📄
- **2026-10-23** — config 정리, entryID 안내, XI text 필수 처리, API Key 발급 방법 README 추가.
- **2026-10-22** — 화면을 구동 시/실행 중 영역으로 재편, data 입력·action data 표시, 툴팁·JSON 도우미, XI secure/input 전달 방식 실험(여러 건 Revert), 기본값 변경, 문구 정리.
- **2026-10-21** — 포트 충돌·설치 전 실행 시 안내.
- **2026-10-20** — XI input/data/entryid 전달 방식 반복 검증(실측), V2 토큰 60초 문서화.
- **2026-10-15** — 초기 구성(websdk-test v0.19.0 축소판), config 일원화, 화면 값 우선 적용, 리뷰 반영.

## 임팩트
- 저장소에 정량 수치 **없음**. 🧠 고객 전달물로 쓰였다면 연동 문의 응대 시간 단축이 기대 효과(근거 없음).

## 회고 / 다음 단계
- 저장소에 **없음**. 🧠 XI 쪽 Revert가 잦아 SDK 동작이 문서와 달랐음을 시사 → 실측 기록이 [[websdk-test]]의 가이드에 쌓임.
- ⚠ 2026-10-23 커밋이 "API Key 실제 값 포함"(고객 전달용 합의)이라고 밝힘 → 저장소를 공유·공개할 때 키 값 점검 필요(값은 이 페이지에 미기재).

## 관련 문서
- [[websdk-test]] · [[CogInsight-Generator]] · [[프로젝트-포트폴리오]] · [[내-프로필]]
