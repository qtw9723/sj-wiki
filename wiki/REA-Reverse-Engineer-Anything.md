---
title: REA (Reverse Engineer Anything) — AI 에이전트용 역공학 MCP
category: 도구/스킬
tags: [rea, mcp, 역공학, reverse-engineering, claude-code, 오픈소스, electron, 보안, 공급망]
source: https://github.com/morluto/rea (README, 2026-10-21 확인), npm rea-agents, https://pasqualepillitteri.it/en/news/23845/rea-reverse-engineer-anything-github-true-false, https://www.inside.com.tw/article/42615-rea-reverse-engineer-anything-open-source-mcp-ai-agent-github
created: 2026-10-21
updated: 2026-10-21
---

> [!tip] 핵심 takeaway
> 🧠 REA는 **"소스 없는 앱의 동작을 에이전트가 증거와 함께 설명하고, 내 프로젝트에 비슷한 기능을 만들게"** 해주는 MCP 서버다. 내 프로젝트(웹·Electron·JS 위주)에서는 **네이티브 디컴파일러 없이도 쓸 수 있는 웹/JS/Electron 정적 분석 부분만** 먼저 붙여보는 게 비용 대비 효과가 크다.
> 🧠 도입 전 체크 3가지: **(1) 공식 출처만 설치**(가짜 트로이 목마 레포 유포 중) **(2) 분석 대상의 권리 확인**(내 소유·허가된 SW만) **(3) 분석 결과가 모델 제공자로 전송됨** — 회사 바이너리·고객 앱은 넣지 말 것.

## 1. 한 줄 정의
- 📄 **REA = Reverse Engineer Anything.** AI 에이전트가 소프트웨어를 역공학할 수 있게 해주는 **MCP 서버 + CLI**. 앱 동작 수준부터 네이티브 바이너리까지. (README)
- 📄 공식 용도: 소스가 없는 앱을 살펴보고 → 기능 동작을 **증거와 함께** 설명하고 → 내 프로젝트에 비슷한 기능을 만드는 데 도움. 합법적 연구·교육·상호운용성·SW 보존, **내 소유이거나 분석 권한이 있는 SW**만 대상. (README)
- 📄 라이선스: REA 코드는 **MIT**. 서드파티 구성요소는 각자의 라이선스(THIRD_PARTY_NOTICES.md). (README, npm)

## 2. 현황 (2026-10-21 기준)
| 항목 | 값 | 출처 |
|---|---|---|
| GitHub | `morluto/rea` | 📄 README |
| npm 패키지 | `rea-agents` **v6.7.0** (2026-10-18 갱신) | 📄 `npm view` |
| Stars / Forks | 약 351k / 88k | 📄 GitHub 페이지 |
| Open issues / PR | 839 / 663 | 📄 GitHub 페이지 |
| 공식 출처 | morluto/rea, rea.tools, npm `rea-agents` **3곳만** | 📄 README |

- ⚠ 📄 스타 수는 기사마다 다름(10/14 약 23만, 10/17 29만 돌파 보도, 오늘 35만). 🧠 10월 초 GitHub 트렌딩 이후 폭발적으로 증가 중이라 숫자 자체엔 의미 두지 말 것.
- 🧠 이슈·PR이 수백 건 열려 있고 릴리스 속도가 매우 빠름 → **버전 고정(pin) 후 도입**이 안전.

## 3. 구조 (어떻게 동작하나)
```
나 → 에이전트(Claude Code 등) ──MCP──▶ REA ──▶ 대상 분석(로컬)
                                      │
                                      └─ 외부 엔진: Hopper / Ghidra / IDA / JEB / objdump / Rizin
        ◀── 근거(evidence)가 붙은 결과 ──┘
에이전트가 결과로 답변·설명·구현·테스트
```
- 📄 분석은 **로컬에서 실행**. REA는 앱을 업로드하지 않음. 단 **툴 결과는 에이전트(=모델 제공자)로 전달**되고 제공자의 데이터 정책이 적용됨.
- 📄 CLI로도 같은 워크플로를 실행할 수 있음.
- 📄 네이티브 심층 분석은 **외부 엔진 필요**(Hopper/Ghidra/IDA 등, REA가 설치해주지 않음). Go·Rust·Unity IL2CPP·Godot PCK·GGUF/safetensors·PyInstaller·Flutter·EVM·SQLite 등은 **내장 정적 파서**로 외부 도구 없이 처리.

## 4. 분석 가능 대상
| 대상 | 무엇을 보나 | 추가 요구사항 |
|---|---|---|
| **웹** | 페이지 구조·스크립트·네트워크 관찰·스크린샷, HAR/Fiddler SAZ/mitmdump 캡처 | Chrome 계열 브라우저 |
| **Electron / JavaScript** | 모듈·import·소스맵·라우트·IPC·네이티브 애드온 관계 | **Node.js + npm만** (정적) |
| **.NET** | 메타데이터·CIL·네이티브 의존성·빌드 비교 | 정적 전용 |
| **네이티브 바이너리** | 의사코드·어셈블리·문자열·심볼·호출·참조, ELF·Go·Rust·WASM | Hopper/Ghidra/IDA, WASM은 WABT 1.0.42 |
| **Android APK** | 매니페스트·클래스·디컴파일 메서드·리소스·실기기(adb)·JEB | JADX + JDK, Apktool, adb |
| **네트워크** | 패킷 캡처, 엔드포인트·DNS·TLS SNI·HTTP 요약 | TShark 4.x(Linux), capinfos |
| **기타** | 데스크톱 설치본, 모델 파일, SQLite DB, 펌웨어, 크래시 기록, Apple 번들 등 | 대상별 도구(Binwalk 등) |

(📄 전부 README)

## 5. 설치 · 업데이트
📄 요구사항: **Node.js 22.x(≥22.19) / 24.x(≥24.11) / 26+** + npm. SQLite 분석은 Node ≥24.15.

```bash
# 가이드 설치 — 에이전트 선택 → 변경안 검토 → 승인. 기존 설정 백업됨. 이후 에이전트 재시작
npx rea-agents setup

# 전역 CLI
npm install --global rea-agents
rea --help

# 1회성 JS/Electron 분석 (JSON 출력)
npx -y rea-agents@latest analyze-javascript-application <path> --json

# 업데이트
rea update                       # 전역 설치
npx rea-agents@latest setup      # 에이전트 등록 갱신
```
- 📄 지원 에이전트: **Claude Code**, Codex, Cursor, Gemini CLI, Grok Build 등. 로컬 MCP를 지원하는 클라이언트는 수동 등록 가능.
- 📄 skills.sh로 **스킬만** 설치하는 방식도 있음.
- 📄 MCP 툴 목록은 README에 없고 `docs/mcp-contracts.md`(자동 생성 카탈로그)에 있음. 예: `inspect_wasm_artifact`.
- 📄 환경변수: `REA_GHIDRA_STARTUP_TIMEOUT_MS`, `REA_HOPPER_STARTUP_TIMEOUT_MS`(큰 바이너리), `REA_JEB_MCP_URL`.
- 📄 일부 기능은 main에만 있고 최신 npm 릴리스엔 없을 수 있음(README의 release-availability 절 참고). Windows Ghidra는 실험적.

## 6. 사용 예
- 📄 프롬프트 예: *"Notes 앱에서 검색이 어떻게 동작하는지 이해하고, 증거를 보여주고, 내 프로젝트에 비슷한 기능을 만들어줘."*
- 📄 쇼케이스: DX-Ball(사운드 팬 재구성, 테스트 3,205개), **Notion(Electron 클립보드 브리지)**, TH04(DOS 탄막 계산).

## 7. 보안 · 법적 주의
- ⚠ 📄 **가짜 레포 주의**: 트로이 목마가 든 사칭 사본이 유포 중(팩트체크 기사). README도 공식 3곳에서만 받으라고 명시.
- 📄 정적 JS/.NET 분석은 대상을 **실행하지 않음**. 런타임 캡처는 **내 사용자 권한으로 대상을 실행**함.
- 📄 IDA Pro·Hopper·JEB 같은 상용 도구는 합법 라이선스 필요. REA는 라이선스를 제공하지 않으며 크랙·우회는 허용 안 함.
- 🧠 `npx rea-agents setup`은 에이전트 MCP 설정을 바꾸므로, **변경안 diff를 꼭 읽고 승인**할 것. 공격면이 넓은 툴(대상 실행·네트워크 캡처·adb)이라 [[내-MCP-커넥터-환경]] §스킬 공격면·권한 최소화 원칙을 그대로 적용.
- 🧠 회사 소유 바이너리·고객사 앱·사내 SDK 결과물을 분석하면 그 내용이 모델 제공자로 넘어감 → 회사 자산은 사내 승인 전 **분석 금지**.

## 8. 내 프로젝트 도입 제안 (🧠 판단 영역)
| 우선순위 | 어디에 | 무엇을 | 필요 도구 |
|---|---|---|---|
| 1 | 웹 프로젝트 전반 ([[공통-기술스택]] React/Vite) | 참고하고 싶은 **내가 쓰는 웹 서비스**의 동작·네트워크 흐름 파악 → 비슷한 기능 설계 | Chrome만 |
| 2 | 웹 SDK 연동 데모류 | 내가 만든 빌드 결과물(번들)을 다시 분석해 **소스맵·모듈 경계·노출 API가 의도대로인지 점검** — 배포 전 셀프 감사 | Node만 |
| 3 | Electron/데스크톱 앱 | 내가 쓰는 Electron 앱 구조 학습(IPC·preload 패턴) | Node만 |
| 보류 | 네이티브·APK·펌웨어 | 현재 프로젝트와 거리 멀고 Ghidra/JDK 등 설치 부담 | 외부 엔진 |

도입 순서 제안:
1. Node 버전 확인(≥22.19) → **전역 설치 대신 `npx -y rea-agents@<고정버전>`으로 1회성 CLI 분석**부터 써보기 (MCP 등록 없이 맛보기).
2. 쓸 만하면 `npx rea-agents setup`으로 **Claude Code만** 선택 등록, 변경 diff 확인.
3. 첫 실험은 **내 소유 웹 앱 빌드 산출물**로 (권리 이슈 0, 결과 검증 쉬움).
4. 버전 고정 + 업데이트는 수동으로(빠른 릴리스·많은 오픈 이슈).

## 관련 문서
- [[내-MCP-커넥터-환경]] — 등록 시 추가될 MCP, 권한 최소화 원칙
- [[에이전트-자동화-도구]] — 에이전트 도구군 중 하나로 분류
- [[Claude-Code-업데이트-동향]] — Claude Code와의 연동
- [[공통-기술스택]] — 적용 대상 스택
- [[웹-크롤링-기초]] — 웹 동작 파악(Playwright 등)과의 비교 후보
