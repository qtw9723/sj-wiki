---
title: schedule-reporter-kakao
category: 프로젝트
tags: [프로젝트, 풀스택, 카카오, 리포팅, 자동화]
source: raw/projects/schedule-reporter-kakao.md
created: 2026-06-09
updated: 2026-06-09
---

> [!tip] 핵심 takeaway
> **"크론탭+메일 보고서" 자동화의 정통 후계자** — [[내-프로필]]의 그 경험을 일정 리포팅 + 카카오 알림으로 발전시킨 프로젝트.
> 알림 채널이 메일(과거)→카카오(현재)로 확장된 것이 핵심. 이 "리포팅 자동화" 패턴은 [[에이전트-자동화-도구]]의 Claude Code **routines/스케줄·dynamic workflows**와 정확히 같은 문제를 푼다 — 동향을 네 프로젝트에 역수입할 여지가 크다.

## 개요
- 설명: 일정 리포터 — 카카오톡 연동. 풀스택. 버전 0.1.0. 최근 2026-06-08, 🔄 개발 중.

## 기술 스택
[[mailer]]와 **동일 스택**: React19/Vite8/Tailwind4([[공통-기술스택]]) + Express + Nodemailer + Supabase([[parking]]) + @dnd-kit. `npm run dev`로 vite+Express 동시 실행, vitest 테스트.

## 특징
일정 리포팅 · 카카오톡 연동 · 메일 발송(Nodemailer) · 드래그앤드롭 UI · Supabase 데이터 · CORS.

## [[mailer]]와의 차이
- 스택 동일. **차이는 목적**: mailer=일반 메일링 / 이 프로젝트=일정 기반 리포팅 + 카카오 채널.
- → 두 프로젝트의 메일/스케줄/Supabase 레이어는 공통 라이브러리로 묶을 후보.

## 의외의 연결점
- 카카오톡 알림 = "사람이 있는 곳으로 결과를 밀어주기". [[에이전트-자동화-도구]]에서 본 Claude Code의 **mobile push notifications / terminalSequence 알림 훅**과 발상이 같다. 자동화의 마지막 단계는 늘 "어디로 알릴 것인가"다.
- ⭐ **정기 발송 자동화 직관**: 일정·알림을 정해진 시각에 자동 발송하는 패턴은 본업의 리마인드/리포팅 자동화 감각과도 통한다.
- **MCP로 코드 없이**: 같은 카카오 푸시를 [[카카오-Play-MCP]](KakaotalkChat·Cal)로 즉시 구현 가능 → [[내-MCP-커넥터-환경]].

## 관련 문서
- [[프로젝트-포트폴리오]] · [[mailer]] · [[parking]] · [[공통-기술스택]] · [[에이전트-자동화-도구]] · [[카카오-Play-MCP]] · [[내-프로필]]
