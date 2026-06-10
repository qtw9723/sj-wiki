---
title: 내 MCP 커넥터 & 도구 환경
category: 도구/스킬
tags: [mcp, 커넥터, cowork, 도구, 자동화, 본인정보]
source: raw/my-connectors-and-techstack.md (회사 섹션 포함 원본은 sj-wiki-work vault로 이동)
created: 2026-06-09
updated: 2026-06-09
---

> [!tip] 핵심 takeaway
> **네([[내-프로필]])가 지금 실제로 손에 쥔 자동화·에이전트 무기고.** macOS + Claude Cowork 데스크탑 환경에서 쓰는 MCP 커넥터·내장 도구·스킬의 단일 목록이다.
> 가장 큰 레버리지: ① **scheduled-tasks(cron)** = 크론탭 자동화의 GUI 후계자 ② **computer-use / Claude in Chrome** = 화면 제어 자동화(시연 리허설·반복 업무) ③ **카카오 Play MCP** = 일정·알림·검색을 카카오 생태계로 묶기.
> 의외의 포인트: 개인 [[카카오-Play-MCP]]·[[schedule-reporter-kakao]]의 알림/발송 자동화는 본업의 알림 업무 감각과도 통한다 — 같은 "결과를 사람에게 푸시" 전략.

## 환경
- **OS/앱**: macOS + Claude Cowork 데스크탑 앱.
- 정리일 2026-06-09.

## 1. MCP 커넥터
### 1-1. 카카오 Play MCP (카카오 공식)
KakaoMap(장소·길찾기) / KakaotalkCal(캘린더·할일) / KakaotalkChat(나에게 메모) / TodoMate(할일·목표) / NaverSearch(뉴스·블로그·쇼핑·데이터랩) / AptInfo(실거래가) / UsStockInfo(미국주식·재무제표) / YouTubeData(영상·자막).
→ **도구 단위 상세는 [[카카오-Play-MCP]]**.

### 1-2. Claude 내장 MCP (Cowork)
| 커넥터 | 역할 |
|---|---|
| `computer-use` | macOS 데스크탑 제어(스크린샷·마우스·키보드) |
| `Claude in Chrome` / `Control Chrome` | 크롬 자동화(DOM·JS)·탭 제어 |
| `workspace (bash)` | Linux 샌드박스 쉘 + web_fetch |
| `cowork` | 파일 관리·Artifact 생성·폴더 접근 |
| `scheduled-tasks` | 예약 작업(cron) 생성·관리 |
| `session-info` | 세션·대화 이력 조회 |
| `mcp-registry` / `plugins` | 커넥터·플러그인 검색·설치 제안 |
| `visualize` | 위젯(SVG/HTML) 인라인 렌더 |

### 1-3. Skills (Cowork)
`docx`·`pdf`·`pptx`·`xlsx`(오피스 문서) / `schedule`(예약 작업) / `skill-creator`·`setup-cowork`.

## 2. 개발/업무 도구 (요약)
- **IDE**: IntelliJ IDEA(주), VS Code(보조). **DB/API**: DBeaver, Postman.
- **브라우저**: Chrome(주, Claude in Chrome 연동), NAVER Whale.
- **협업**: MS Teams·Outlook·Office·OneNote, KakaoTalk(사내 메신저), Zoom.
- 개인 프로젝트 기술 스택 상세는 [[공통-기술스택]] (React19·Vite8·Tailwind4·Supabase).

## 3. 회사 업무 환경
- 회사(사내 AI 챗봇) 업무 환경·플랫폼·프로젝트 기밀 상세는 **PC 전용 `sj-wiki-work` vault**에 분리 보관.

## 의외의 연결점
- **scheduled-tasks(cron) ↔ 자동화 정체성**: [[내-프로필]]의 파이썬+크론탭 → [[schedule-reporter-kakao]] → 이 커넥터들로 진화. 같은 본능, 더 강한 도구 → 흐름은 [[에이전트-자동화-도구]].
- **computer-use / Claude in Chrome ↔ 데모 운영**: 화면 전환·반복 작업 리허설을 화면 제어 도구로 자동화/검증할 여지.
- **카카오 채널**: 개인 [[카카오-Play-MCP]](KakaotalkChat·Cal)로 "결과를 카카오로 푸시" — 알림 자동화 직관.
- **NaverSearch datalab(연령·성별 트렌드)**: 타게팅·캠페인 설계 시 트렌드 데이터 활용 발상.

## 관련 문서
- [[카카오-Play-MCP]] · [[공통-기술스택]] · [[에이전트-자동화-도구]] · [[schedule-reporter-kakao]] · [[내-프로필]]
