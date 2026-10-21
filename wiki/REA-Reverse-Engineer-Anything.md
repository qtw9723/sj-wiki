---
title: REA (Reverse Engineer Anything) — AI 에이전트용 역공학 MCP
category: 도구/스킬
tags: [rea, mcp, 역공학, reverse-engineering, claude-code, 오픈소스, electron, 보안, 공급망, 로컬llm, vllm, 챗봇구조분석]
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

### 7-1. 데이터 흐름 오해 정리 (2026-10-21 대화)
- 🧠 결과가 에이전트로 돌아가는 건 **REA가 업로드해서가 아니라 MCP 구조 자체**: 에이전트가 REA 도구를 호출 → REA가 로컬 분석 → 결과를 호출자에게 반환. 외부 전송은 **에이전트의 두뇌가 클라우드 LLM이라서** 생김.
- 🧠 그래서 "REA에서 전송 부분만 제거"는 불가능/무의미(제거하면 빈 MCP). REA는 MIT 오픈소스라 역공학할 필요도 없음.
- 🧠 외부로 안 내보내는 대안:

| 방법 | 외부 전송 | 잃는 것 |
|---|---|---|
| CLI만 사용(`--json`) | 없음 | AI 해석(직접 읽기) |
| 로컬/사내 LLM을 에이전트로 | 없음 | 모델 품질·속도 |
| 넣는 대상 선별(내 소유·공개 웹만) | 있음(비민감) | 회사·고객 자산 분석 불가 |
| 기업 데이터 정책(보관·학습 안 함 계약) | 있음 | 회사 승인·계약 필요 |

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

## 9. 활용 패턴 — REA는 분석기, 해석은 로컬/사내 LLM (🧠 판단 영역)
**A. CLI 파이프라인 (추천, 단순·확실)**
```
rea CLI ──JSON──▶ 스크립트(요약·청크 분할) ──▶ 로컬/사내 LLM(vLLM 등 OpenAI 호환 API) ──▶ 해석·재구성
```
- 모델이 도구 호출을 못 해도 동작. 단점: 분석 1회 → 해석 1회 고정, 모델이 스스로 추가 조사 못 함.

**B. 에이전트 방식 (REA MCP + 로컬/사내 LLM을 두뇌로)**
- OpenAI 호환 엔드포인트를 모델로 지정 가능한 MCP 클라이언트(Cline·Continue·OpenCode·Goose 등)에 REA 등록. Claude Code는 LiteLLM 같은 게이트웨이 경유로 가능하나 번거로움.
- 조건: vLLM `--enable-auto-tool-choice --tool-call-parser <모델별>`, 그리고 다회 도구 호출을 버틸 모델 성능.

**공통 주의**
- 분석 JSON이 큼 → `--max-model-len`(컨텍스트)에 맞게 필요한 모듈·함수만 잘라 넣기.
- 같은 공개 샘플을 Claude와 로컬 모델에 넣어 **해석 품질 비교 기준**부터 잡기.
- 데이터가 밖에 안 나가도 **분석 권한은 별개**(사내 자산은 승인 필요).
- 진행 순서: A로 공개 샘플 1개 시험 → 쓸 만하면 B 검토.

## 10. 활용 아이디어 — 도메인 → 비슷한 구조의 챗봇 (🧠 판단 영역)
목표: 도메인만 주면 그 사이트 챗봇의 **구조**를 파악해 비슷한 시나리오 틀 생성. 구조만 보면 네이티브 도구가 필요 없어 빠름.

| 보임 (클라이언트) | 안 보임 (서버) |
|---|---|
| 📄 페이지 구조·스크립트·네트워크·스크린샷(REA 웹 분석 범위) | 시나리오 트리·인텐트·학습 데이터 |
| 위젯 벤더/SDK, 대화 API 엔드포인트, 요청·응답 JSON 형태 | LLM 프롬프트·RAG 문서·분기 로직 |
| 버튼·카드·빠른응답 등 UI 컴포넌트 | 상담원 연결 등 내부 연동 |

- 정적 분석만으론 반쪽 → **실제로 대화하며 네트워크 캡처**해야 대화 흐름(인사 → 메뉴 → 분기 → 종료)이 드러남.
- 파이프라인: ① 챗봇 열고 대표 메뉴 클릭하며 HAR·스크린샷 수집 → ② 메뉴 트리·응답 유형·상담 연결 지점·API 형태로 요약 → ③ 그 구조로 시나리오 틀 생성(해석은 §9 A안의 로컬/사내 LLM).
- 이 범위는 **REA 없이 브라우저 자동화(Playwright·Chrome 연동)+HAR로도 충분**. REA는 Electron·번들 JS 심층 분석이 필요할 때 이점 → 가벼운 쪽 먼저, 막히는 부분만 REA.
- 주의: 남의 사이트는 REA가 말하는 "권한 있는 대상"이 아님 → **구조·흐름 참고까지만**, 응답 문구·콘텐츠 복제 금지, 대화 API 반복 호출(크롤링) 금지, 이용약관 확인. 고객사 사이트는 동의 받으면 깔끔.

## 관련 문서
- [[내-MCP-커넥터-환경]] — 등록 시 추가될 MCP, 권한 최소화 원칙
- [[에이전트-자동화-도구]] — 에이전트 도구군 중 하나로 분류
- [[Claude-Code-업데이트-동향]] — Claude Code와의 연동
- [[공통-기술스택]] — 적용 대상 스택
- [[웹-크롤링-기초]] — 웹 동작 파악(Playwright 등)과의 비교 후보
