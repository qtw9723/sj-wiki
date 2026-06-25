---
title: schedule-reporter-kakao
category: 프로젝트
tags: [프로젝트, 풀스택, 리포팅, 자동화, grafana]
source: raw/projects/schedule-reporter-kakao.md
created: 2026-06-09
updated: 2026-06-25
---

> [!tip] 핵심 takeaway
> **"크론탭+메일 보고서" 자동화의 정통 후계자** — [[내-프로필]]의 그 경험을 리포트 스케줄링으로 발전시킨 프로젝트.
> ⚠️ **이름과 달리 현재 카카오 연동은 코드에서 제거된 상태**(📄 2026-06-09 `simplify to schedule settings page only` 리팩터, grep 0건). 지금은 **[[mailer]]의 Grafana 리포트 기능을 떼어낸 단일 스케줄-설정 페이지**에 가깝다. 원래 목표(카카오 Play MCP 스케줄을 자체 서버로 이전)는 README에 남아 있으나 미완.
> → 이 "리포팅 자동화" 패턴은 [[에이전트-자동화-도구]]의 Claude Code **routines/스케줄·dynamic workflows**와 같은 문제를 푼다.

## 개요 📄
- 일정/리포트 스케줄러. 풀스택. 버전 0.1.0. 최근 커밋 2026-06-09, 🔄 개발 중.
- **현재 라우팅은 단 2개**(`App.jsx`): `/login`(LoginPage) + `/`(GrafanaPage). 사실상 **Grafana 리포트 스케줄 설정 단일 페이지**.
- `src/pages/`엔 Grafana·Hub·Mailer·Chatbot·Login 페이지가 있으나(=[[mailer]]와 동일 계열 구조) **Grafana만 라우팅**됨.
- 🧠 카카오(grep 0건) 코드 제거 → 이름의 `kakao`는 원래 목표의 흔적일 뿐.

## 기술 스택 📄
[[mailer]]와 **동일 스택**: React19/Vite8/Tailwind4([[공통-기술스택]]) + Express + Nodemailer + Supabase([[parking]]) + @dnd-kit(deps 잔존). `npm run dev`로 vite+Express 동시 실행, vitest 테스트.

## [[mailer]]와의 관계
- 🧠 스택·페이지 구조가 [[mailer]]와 거의 동일 → **mailer의 Grafana 리포트 부분을 분리한 형제 앱**으로 보인다. 현재 기능이 mailer와 상당 부분 겹침.
- → 두 프로젝트의 메일/스케줄/Grafana/Supabase 레이어는 공통 라이브러리로 묶거나 통합을 검토할 여지.

## 진행사항 업데이트 로그
- **2026-06-25** 📄: 라이브 저장소 재확인. 2026-06-09 단순화 리팩터 반영 — 카카오 연동 코드 제거, GrafanaPage 단일 페이지로 축소, [[mailer]] 계열 구조로 정렬. takeaway·개요를 현행화(기존 "카카오 연동·드래그앤드롭·일정 리포팅" 서술은 구버전이라 정정).

## 의외의 연결점 (🧠 판단 영역)
- 📅 **정기 발송 자동화 직관**: 정해진 시각에 리포트를 자동 생성·발송하는 패턴은 본업의 리마인드/리포팅 자동화 감각과 통한다.
- **MCP로 코드 없이**: (원래 목표였던) 카카오 푸시는 [[카카오-Play-MCP]](KakaotalkChat·Cal)로 코드 없이 즉시 구현 가능 → [[내-MCP-커넥터-환경]]. 자동화의 마지막 단계는 늘 "어디로 알릴 것인가"다.

## 관련 문서
- [[프로젝트-포트폴리오]] · [[mailer]] · [[parking]] · [[공통-기술스택]] · [[에이전트-자동화-도구]] · [[카카오-Play-MCP]] · [[Teams-Gmail-캘린더-Gemini-연동]] · [[모닝-브리핑-AppsScript]] · [[내-프로필]]
