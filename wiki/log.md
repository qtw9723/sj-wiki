---
title: 작업 이력 (Log)
category: 시스템
tags: [log, 이력]
created: 2026-06-10
updated: 2026-07-15
---

## [2026-07-15] 프로젝트 업데이트 | CogInsight v0.4.0 프로덕션 릴리스 + 공유 노트 최신화
- 📄 사용자 "릴리스하자 + 공유 노트 최신화". 4축: ①코드 PR #106→main `52a0f59`·tag v0.4.0·GitHub Release(게이트 build+deno 260/0) ②DB·③엣지함수 해당없음(프론트 전용) ④프론트 Vercel 자동배포(200).
- 공유 노트: 공개 개요(coginsight-overview) v0.4.0 예정→릴리스 전환·재배포·라이브 검증, [[CogInsight-Generator-링크]] 위키 노트 갱신. ⚠ 개요 아티팩트(1e30660a)는 v0.3.0 기준 드리프트(기록됨).
- [[CogInsight-Generator]] 진행 현황·스냅샷·버전표(v0.4.0 릴리스)·진행 로그 갱신. 잔여: OQ2(PNG 외관 수동확인), v0.5(편집 역반영 등).

## [2026-07-15] 자료넣기 | CogInsight v0.4.0 — 구조 다이어그램: 시나리오=단일 흐름(반복 구획화) (직접 구현)
- 📄 사용자 관찰(회사 솔루션은 시나리오=단일 플로우인데 다이어그램은 여러 인입처럼 보임) → 원인=반복 본문 노드가 엣지 없이 떠 있음. 해결: 반복을 loopGroup 박스로, 본문을 박스 안(parentId+extent) 담아 메인 흐름 단일 스트림화. refDiagram bodyEdges 파생 추가. verify green(build 2065·deno 256/0). CogInsight 커밋 3개 push.
- [[CogInsight-Generator]] 진행 로그 2026-07-15(단일 흐름·반복 구획) 추가. 설계 spec은 저장소 `docs/superpowers/specs/2026-07-15-single-flow-loop-grouping-design.md`.
- ⚠ 한계: 중첩 반복 평면 렌더(향후). 미확인(사용자 몫): dev 서버에서 단일 흐름·반복 박스 육안 확인.

## [2026-07-15] 자료넣기 | CogInsight v0.4.0 — 구조 다이어그램 가독성 개선 (직접 구현)
- 📄 사용자 요구: 구조 다이어그램의 라벨 잘림(→호버 툴팁)·시나리오 통째 이동(그룹 박스 내)·색 대신 플로우차트 도형/범례. FlowCanvas 구조 뷰만 수정, 표준 도형(SVG)+범례 패널+2줄 라벨/호버 툴팁+그룹 드래그(parentId·extent:'parent', 읽기 전용). 새 모듈 nodeShape.js+테스트. verify green(build 2065·deno 253/0). CogInsight 커밋 3개 push.
- [[CogInsight-Generator]] 진행 로그 2026-07-15(구조 다이어그램) 추가. 설계 spec은 저장소 `docs/superpowers/specs/2026-07-15-structure-diagram-improvements-design.md`.
- ⚠ 미확인(사용자 몫): 전 라우트 OTP 게이트라 자동 구동 불가 → dev 서버 육안 확인.

## [2026-07-15] 자료넣기 | CogInsight v0.4.0 확장 — 생성 결과에도 플로우 시각화 (직접 구현)
- 📄 사용자 요구("레퍼런스뿐 아니라 생성 결과에서도 시각화")로 v0.4.0 브랜치에 직접 구현. `generated_json`이 레퍼런스와 동일 `dialogs/main` 구조라 `FlowCanvas`/`refDiagram` 재사용, 결과 화면 2곳(ResultDetail·ResultDetailModal)에 `[JSON|다이어그램]` 토글 배선 + 모달 ESC 가드. verify green(build 2065·deno 250/0). CogInsight 커밋 3개 push(브랜치 미머지·무배포).
- [[CogInsight-Generator]] 보강: 진행 로그 2026-07-15 신규, 스냅샷·버전표 v0.4.0 행을 "진입점 4곳(레퍼런스 2 + 생성 결과 2)"으로 확장. 설계 spec은 CogInsight 저장소 `docs/superpowers/specs/2026-07-15-result-flow-visualization-design.md`.
- ⚠ 미확인(사용자 몫): dev 서버에서 결과 다이어그램 육안 확인.

## [2026-07-15] 프로젝트 업데이트 | CogInsight Generator — v0.3.1(gpt-5.2) + v0.4.0 dev 구현 완료 반영
- 📄 라이브 저장소·올림푸스 state 직접 확인: main = **v0.3.1**(gpt-4o→gpt-5.2 전환, PR #105), **v0.4.0 레퍼런스 플로우 시각화는 [[올림푸스-Olympus]] 자율 개발로 dev 완주**(브랜치 미머지·프로덕션 무배포, T1~T7 done, deno 250/0·build 2065 green).
- [[CogInsight-Generator]] 보강: 스냅샷·진행 현황에 v0.3.1/v0.4.0 상태 추가, 기술스택 LLM gpt-4o→gpt-5.2, 버전 히스토리 표에 v0.3.1·v0.4.0(dev) 행, 업데이트 로그 2건(7/14~15 v0.4.0 구현·경위·잔여 OQ / 7/9 v0.3.1). 진행 현황 헤더 버전중립화(앵커 정합).
- ⚠ 사용자 확인거리: 사용자 흐름도 PNG 외관(OQ2, 수동 판정) / CHANGELOG [0.4.0] Added 미기입(릴리스 전 저장소 보강 필요).

## [2026-07-14] 자료넣기 | AI 주간 소식 W28 (7/6~7/12) 위키화
- 📄 `raw/ai-digest/2026-07-11.md`(OpenAI·MIT·MS Research·arXiv 멀티에이전트·HuggingFace) 위키화 → 신규 [[AI-주간-소식-2026-W28]] 생성(W28 페이지 부재).
- 빅이슈: OpenAI 제품 대공세(GPT-5.6·ChatGPT Work 행동 에이전트·GPT-Live 음성·M365 Copilot 기본채택), SWE-Bench Pro 벤치마크 신뢰성 문제. arXiv 멀티에이전트 실무배치 3편을 내 프로젝트에 교차연결: 실패국소화→[[올림푸스-Olympus]], ASMR 스키마 자동생성→[[CogInsight-Generator]], 프라이버시 방화벽→[[GLM-Zhipu-Z-ai]] 거버넌스. Flint(MS 시각화 언어)→CogInsight v0.4.0 다이어그램. 🧠 의외의 연결점: W27→W28 "연구개념→안전배치" 이동, 음성 2주연속, 비개발→개발 시대적 정당화([[내-프로필]]).
- [[index]] AI/업계 동향에 등록, [[AI-주간-소식-2026-W27]]에 다음 주 역링크 추가.

## [2026-07-09] 자료넣기 | 올림푸스 run.env 도입 — 버전 폴더 실사고의 근본 수정 + 자동 재개
- 📄 실사고: 버전 폴더(spec/CogInsight-Generator-v0.4.0)를 UI 큐로 실행하자 TARGET_REPO를 폴더명으로 추측해 **빈 디렉토리를 greenfield 생성**, 파이프라인이 사람에게 "명령 복사 재기동"을 요구 — 사용자 지적("자동화 시스템이 재실행을 시키면 안 됨").
- 근본 수정(`d3bc670`): **spec/<프로젝트>/run.env 자동 로드**(우선순위: 명시적 env > run.env > config 기본값) — UI/큐 실행에서도 대상 repo·브랜치·게이트 자동. v0.4.0 spec에 run.env 동봉, 잘못 생성된 빈 스캐폴드 삭제, 블로커 답변을 human-answers.md에 기록 후 **큐 항목 queued 복귀 → 사람 개입 없이 자동 재개 검증**(brownfield·feat/v0.4.0 브랜치 확인). 테스트 전체 green. [[올림푸스-기획요청서-작성요령]] §4에 run.env 필수 규약 추가, 기획서 실행 가이드 단순화(PROJECT만).

## [2026-07-09] 자료넣기 | 올림푸스 메일에 응답 방법 명시 (사용자 요구)
- 📄 승인 요청 메일에 "어디서 어떻게 응답하는지" 안내가 없어 혼동 → 올림푸스 발신 메일 전 경로에 응답 방법 블록 추가(승인=이 메일 답장 첫 줄 y/n·제목 토큰 유지, 질문 대기=답장 무효·GitHub ## 답변 편집, 진행·토큰대기 알림=회신 불필요). remote.sh·milestones.sh·resilience.sh, 테스트 전체 green, push(`8d7919b`). [[올림푸스-기획요청서-작성요령]] §5 갱신.

## [2026-07-09] 자료넣기 | v0.4.0 기획서 작성 — 레퍼런스 플로우 시각화 (올림푸스 자율 개발용)
- 📄 사용자: v0.4.0은 올림푸스로 개발 — 기획요청서만 제작. `olympus/spec/CogInsight-Generator-v0.4.0/기획.md` 작성(구조 다이어그램+usecase 흐름도(산출물 품질·PNG 내보내기)+풀스크린 피그마류 UX+v0.5 편집 대비, react-flow 도입 확정, AC=deno fixture 테스트+빌드, main 머지·배포 금지).
- 버전 포함 spec 폴더 규약 신설 → [[올림푸스-기획요청서-작성요령]] §4에 추가(PROJECT+TARGET_REPO 동시 지정). dev 브랜치 `feat/v0.4.0-reference-visualization`·0.4.0 선반영·CHANGELOG 섹션 준비 완료. [[CogInsight-Generator]] 진행 로그 기록.

## [2026-07-09] 자료넣기 | 공개 개요 문서 v0.3.0 본문·매뉴얼 최신화 (사용자 지시)
- 릴리스 때 배지·통계·버전표만 갱신됐던 coginsight-overview를 본문까지 최신화: "진행 현황 & 한계" 섹션을 릴리스 상태로 재작성(프로덕션 v0.3.0·5종 승격·조립 57건 검증·다음 v0.4.0), 남은 항목 목록 현행화(조립 완료분 제거, 미리보기·다중 후보·도매 승격 예정 반영).
- 사용자 매뉴얼 보강: A-2 "(v0.3.0) 레퍼런스로 시작하기"(구조 시드·흐름 요약 카드·필드 비활성화) 신설, A-6 화면 첨부(캡처·미리보기) 추가, B-9 어드민 썸네일·7일 자동 정리 추가. 재배포 200 + 아티팩트 동기화(label v0.3.0-doc-refresh).

## [2026-07-09] 자료넣기 | 릴리스 규약에 dev 서버 재세팅 명문화 (사용자 지시)
- 📄 "앞으로 dev 서버 세팅도 프로덕션 릴리스 규약에 추가" → 저장소 CLAUDE.md DEV 규약 갱신(PR #104 머지, main `a3d1f6d`): 4축 후 dev 리셋·재세팅까지가 릴리스 절차, dev 슬러그 7종 main 기준 재배포, **미승격 dev-원본 레퍼런스 보존**(TRUNCATE 유실 금지), 질문 id 재발급·Storage API 삭제 주의. 메모리 규약도 동기화.

## [2026-07-09] 자료넣기 | v0.3.0 프로덕션 릴리스 — 시나리오 레퍼런스 라이브러리 (4축 + dev 리셋)
- 📄 사용자 지시("프로덕션에 머지·버전 라벨링 정리·dev 세팅 포함")로 규약 4축 수행: ①코드 PR #103→main `ae99f4d`·tag v0.3.0·Release, CHANGELOG/ROADMAP 라벨링 확정 ②DB diff 0 확인·마이그레이션 push·**레퍼런스 5종 승격**(사용자 선별, 도매 제외) ③함수 27종 재배포+프로덕션 스모크(few-shot 실주입 확인 후 삭제) ④Vercel 번들 0.3.0. dev 리셋(5테이블 미러·diff 0·스토리지 dev/ 정리·슬러그 main 기준, 도매 레퍼런스는 dev 보존=의도된 diff 1건).
- 공개 개요 페이지·아티팩트 v0.3.0 반영(배지·통계 741커밋·버전 히스토리). [[CogInsight-Generator]] 진행 현황·버전표·진행 로그 갱신.

## [2026-07-09] 질문 | v0.3.0 릴리스 사전점검 + 조립 생성 테스트(로드맵 항목 3) — 조립기 루프 body 버그 발견·수정
- 📄 사전점검: deno 366 통과(실패 8건=v0.2.1에도 있던 레거시 테스트, 무관 확인)·빌드 통과·회귀 하네스 4/4 PASS. 조립 전수 검사(신규 assembleCheck.ts, 57조합)에서 **조립기가 루프 body를 누락·미재작성하는 실버그** 발견(46 FAIL) → 수정·TDD·dev 재배포 후 57/57 PASS(`d5236a8`). [[CogInsight-Generator]] 로드맵 항목 3 ✅.
- 잔여: 항목 4(다중 후보 스코어), 항목 6 백로그. 릴리스 결정 대기(레퍼런스 승격 선별 포함).

## [2026-07-09] 자료넣기 | PR #102 머지(표기 통일) + 공식 링크 모음 페이지 신설
- 📄 사용자 지시로 PR #102("CogInsight POC Generator"→"CogInsight Generator" 표기 통일) 머지(main `7c597a7`), dev 브랜치 main 동기화, Vercel 재배포로 앱 타이틀 "CogInsight Generator" 확인.
- [[CogInsight-Generator-링크]] 신설 — 접속 검증된 현행 링크(공개 개요/테스터 앱/소유자 전용) + 구 URL 폐기 고지 + 재안내 문구. [[index]]·[[CogInsight-Generator]]에서 연결.

## [2026-07-09] 자료넣기 | 프로젝트명 전면 변경 — CogInsight Generator (v0.2.2 릴리스 + 전 인프라·위키·메모리 리네임)
- 📄 사용자 확정: 구명(4글자 코드네임)이 **사용 불가 판정** → "모든 곳의 모든 흔적" 변경 지시. 범위=라이브 인프라까지 전부 + raw/ 수정 예외 승인, git 이력은 유지.
- 집행: ① 저장소 main 리네임(122파일)+PR #101 머지·tag v0.2.2·Release ② 라이브 DB 객체 48건 rename(데이터 무손실 검증) ③ 엣지함수 25종 재배포·신규 슬러그 `coginsight-generator(-dev)`·구 슬러그 삭제 ④ GitHub repo `CogInsight-Generator`·로컬 폴더 rename ⑤ Vercel 앱 `coginsight-generator.vercel.app`·개요 `coginsight-overview.vercel.app`(구 URL 폐기·404 확인)+아티팩트 동기화 ⑥ v0.3.0 dev 브랜치 동일 적용(134파일, deno 228 green)+dev 래퍼 7종 재배포 ⑦ 위키 23파일 치환+페이지 파일명 `CogInsight-Generator.md`+raw 4파일(파일명 1건 포함) ⑧ 메모리 갱신.
- ⚠ 소급 치환 고지: log.md 과거 항목·위키 본문 속 구명·구 URL·구 테이블명도 새 이름으로 일괄 치환됨(append-only 원칙의 승인된 예외 — 사실 관계는 불변, 명칭만 현행화). 의도 잔존 = 양 저장소 git 커밋 이력.
- 영향 페이지: [[CogInsight-Generator]](스냅샷·버전표·진행로그) · [[index]] · [[프로젝트-포트폴리오]] · [[parking]] 외 링크 페이지 15종(문자열 치환).

## [2026-07-08] 질문 | CogInsight v0.2.1 핫픽스 — ESD 스키마 파생 버그 (발표 준비 중 발견)
- 데모 봇에서 ESD 산출물(esd_schemas)이 항상 빈 배열 → 원인=collectEsdFields의 schemaName 경로 버그(config.query.schemaName). 수정+회귀테스트, PR #100 머지·tag v0.2.1·프로덕션 coginsight-generator 재배포·재생성 검증(e72f4e26). 공개 coginsight-overview·아티팩트·[[CogInsight-Generator]]·시연대본 v0.2.1 반영.

## [2026-07-08] 질문 | CogInsight 생성 파이프라인 스테이지 라벨 함수명化
- 누적 삽입 뜀번호(2.9·3.65·3.75 등) → 함수명 라벨 일괄 치환(17파일), index.ts에 이름↔레거시번호 매핑표 추가(이력 추적). deno 221 green. v0.3.0 dev 브랜치(feat/v0.3.0-observability-regression)에 ff-머지·push(7cf1d75), main·프로덕션 미반영. [[CogInsight-Generator]] 진행로그 기록.

## [2026-07-08] 질문 | CogInsight 발표용 공개 개요 페이지 v0.3.0 진행분 반영
- 오늘 발표(공개 문서·사내 실무/보고 톤)용으로 [[CogInsight-Generator]] 현 개발분(프로덕션 v0.2.0 + v0.3.0 dev 진행)까지 정리해 공개 페이지 **coginsight-overview.vercel.app** 재배포(200) + claude.ai 아티팩트(1e30660a) 동기화.
- 갱신: 히어로 배지·통계(713커밋/29함수/64마이그레이션)·"진행 현황"에 v0.3.0 진행 섹션 신설·버전 히스토리 v0.3.0 (계획→개발 중). 위키 버전표·진행 로그 미러 갱신.
- 추가(사용자 요청): 공개 doc "생성 내부 로직"의 뜀 번호(2.9·2.95·3.65·3.75)를 **①설계→②전개→③안전장치 3단계 계층 번호**(앞자리=단계, 2.1~2.3·3.1~3.8)로 정리, 표에 단계 그룹 헤더 추가·함수명 유지. ⚠ 공개 doc는 **표시용 간소 번호**, 실제 코드 스테이지 번호(위키 [[CogInsight-Generator]] §주요기능·§생성 파이프라인은 2.9/3.65/3.75 유지)와 의도적 분리 — 함수명이 대응 앵커. 재배포·아티팩트 동기화 완료.

## [2026-07-08] 자료넣기 | CogInsight 결정 대기 3건 사용자 결정·집행
- 📄 사용자 결정: ① node_modules 6,780파일 → **v0.3.0 브랜치에서** 추적 해제(`209995d` push, 머지 PR에 -6,780 포함 감수) ② AGENTS.md → .gitignore 등록(같은 커밋) ③ "LLM 노드 샘플 (7/2 발췌)" → **지금 파생 실행**: `derive-node-specs` 호출, pending→completed(노드 7종·경고 0) 재조회 검증 — coginsight_references 4건 전부 completed. [[CogInsight-Generator]] 해소 표시 갱신.
- 🧠 잔여(결정 아님·사용자 실행 몫): 서비스 롤 키 재발급, 피드백 스크린샷 로컬 화면 실검증, llmloop 런타임 검증.

## [2026-07-07] 자료넣기 | CogInsight 오늘 작업 문서 전체 정합화 (프로젝트 업데이트)
- 📄 라이브 저장소 대조(마지막 커밋 17:51 `8471c0c` ≤ 위키 갱신 17:59): 메인 페이지 진행 로그는 최신 확인. 뒤처진 문서 정합화 — ①[[CogInsight-Generator]] 진행 현황 헤더를 7/7(v0.2.0 유지·v0.3.0 dev 진행)로, 로드맵 작업 항목을 저장소 ROADMAP.md 미러로(1·2 ✅, 3 시드 추가 구현, 4 🔶 부분), 버전표 v0.3.0 행·피드백 기능 줄 보강, 깨진 진행 현황 앵커 수정 ②[[프로젝트-포트폴리오]]·[[index]]의 CogInsight 상태가 "v0.1.0 동결·v0.2.0 설계만"으로 낡아 있던 것을 현행(v0.2.0 릴리스·v0.3.0 dev)으로 갱신.
- 📄 저장소 CHANGELOG [0.3.0]에 7/7 누락분 보강 커밋·push(`5e8e487`): 시드 UX 3건·드롭다운 렌더 경로 픽스·피드백 스크린샷 첨부. (ROADMAP.md·CLAUDE.md는 이미 최신, 공개 개요 페이지는 dev 상세 비공개 원칙이라 무변경)

## [2026-07-07] 자료넣기 | CogInsight 피드백 스크린샷 첨부 구현 — 체크 시 뷰포트 캡처·미리보기·어드민 확대 (dev 전용)
- 📄 사용자 제안: 팝오버 체크박스 → 체크 시점 DOM 캡처(html-to-image, 피드백 UI 제외)·미리보기·best-effort 전송. `dev_coginsight_feedback` 사본(+screenshot 컬럼)·`feedback-dev` 슬러그·프로덕션 마이그레이션 파일(작성만). dev API 검증 4종+격리 통과. [[CogInsight-Generator]] 갱신.
- ⚠ 별건 발견: node_modules 6,780파일 git 추적 중(기존 결함 — 정리 여부 사용자 결정 대기), 루트 미추적 AGENTS.md(타 도구 생성 추정).

## [2026-07-07] 자료넣기 | CogInsight v0.4.0 계획(레퍼런스 다이어그램 시각화) 문서 전체 반영
- 📄 사용자 지시("전체 문서에도 적용"): v0.4.0 계획을 ①저장소 ROADMAP.md(기반영) ②공개 개요 페이지 버전 히스토리에 "v0.4.0 (예정)" 행 추가 → **`vercel --prod` 재배포**(200·행 라이브 확인) ③claude.ai 아티팩트 원본 동기화(label `v0.4.0-plan-row`) ④위키 버전표에 v0.4.0(예정)·v0.3.0(계획) 행 추가(공개 페이지 mirror 규칙 — 위키표에 v0.3.0 행이 누락돼 있던 것도 정합화).

## [2026-07-07] 자료넣기 | CogInsight 레퍼런스 구조 시드 생성 구현 — 설문에서 레퍼런스 선택 → 결정론 복제 생성
- 📄 사용자 제안 기능: 설문 시나리오 항목에 "레퍼런스 선택" 드롭다운(프론트 주입 — 공유 templates 무접촉) → 선택 시 STAGE 3.68이 레퍼런스 플로우를 구조 시드(결정론 복제, 진입 발화만 설문 값). `scenario_examples.seeded` 관측성 + 하네스 실측 어서션 + fixture. dev 전용(브랜치 25커밋, main 미머지).
- ⚠ 최종 브랜치 리뷰가 결함 3건 발견·수정: 이중 트리거 게이트(설문 발화≠레퍼런스 트리거면 도달 불가) / 3.7 수집형 체인의 시드 파괴 / 동어반복 어서션 — **3중 검증이 같은 사각지대를 공유**했던 사례. 다른 진입 발화 실검증 PASS 후 Ready. [[CogInsight-Generator]] 갱신.

## [2026-07-07] 셋업 | 올림푸스 마일스톤 진행도 알림 구현 + push
- 📄 "전부 진행" 지시: ①토큰로깅+완료메일 커밋 origin push(71a360e) ②사용자 스펙(마일스톤 진행도 알림) 구현.
- 📄 milestones.sh 신설(backlog_progress/titles/milestone_notify, 무중단 계약) + config NOTIFY_MILESTONES + run.sh 훅 3곳(분석완료/작업n·N/전체완료). test 13개+전체스위트 통과. main 머지·push(40cf52b). 런북 §G 추가.

## [2026-07-07] 셋업 | 올림푸스 토큰로깅 완료메일 첨부 + main 머지
- 📄 usage_summary() 추가: state/usage.tsv에서 이번 RUN_ID 역할별 집계 → 완료(승인)메일 본문($APPROVE_Q)·완료 콘솔에 표시. 모니터링 3곳(완료메일/tsv/로그).
- 📄 feat/usage-logging → main 머지(71a360e, no-ff, 미push), 브랜치 삭제. ⚠머지에 사용자 본인 선행커밋 1506c40(마일스톤알림 스펙·문서만) 동반 — 무해, 완료메일과 겹치는 설계. push 여부 사용자 확인 대기.

## [2026-07-07] 셋업 | 올림푸스 자체 토큰 로깅(run.sh, 브랜치)
- 📄 요구 정정: 외부 조회 도구 말고 **올림푸스가 돌며 자동 기록** → 최적화 검토용. run.sh에 log_usage() + metis/worker 래핑(호출 직후 세션 jsonl usage 합산→state/usage.tsv, run/round/role별). claude 호출·한도감지 불변(가산형). USAGE_TRACK 토글.
- 📄 브랜치 feat/usage-logging 커밋(cf07d17, main 미머지·미푸시). bash -n 통과, 집계=usage-report 합계 일치 검증. 런북 §F ④ 추가. ⚠E2E는 다음 실행 때.

## [2026-07-07] 자료넣기 | usage-report.sh --html 브라우저 대시보드
- 📄 `--html [일수]` 모드 추가: 자기완결 다크 텔레메트리 HTML(프로젝트별 소비막대·요약스탯·tabular-nums) → usage.html 생성·자동 open. 재실행 시 최신 갱신. 런북 §F ③ 추가.
- 🧠 현 시점 스냅샷은 Artifact로도 발행(정적). 상시최신=로컬 재실행.

## [2026-07-07] 자료넣기 | usage-report.sh 개요모드(전 프로젝트 누적)
- 📄 usage-report.sh 확장: 인자없음=전 프로젝트 누적 개요(프로젝트별 호출·출력·총tok·환산$·사용기간, 소비순), 숫자=개요+기간, 문자=상세. 라벨정리(홈-CLI세션 등). 런북 §F 갱신.
- 📄 개요 실측: 홈-CLI 최다 / CogInsight $274·sj-wiki $235·올림푸스(dev-pipeline) $101·mailer $88.

## [2026-07-07] 자료넣기 | 올림푸스 토큰 사용량 관측(모델은 Claude 유지)
- 📄 `~/IdeaProjects/olympus/usage-report.sh` 신규(read-only, 파이프라인 무수정). ~/.claude/projects/*.jsonl(assistant 라인 .message.usage) 집계 → 모델별·일자별·환산$. bash3.2/BSD awk 호환(mapfile·asorti 제거) 검증 완료.
- 📄 실측: 올림푸스(dev-pipeline 폴더) 6/30~7/2 3일=998호출·Opus환산≈$100 → 캡 부딪힘 정량 확인. ⚠폴더명 pipeline로 조회(리네임 전). [[올림푸스-실행-런북]] §F 신설, /usage·/cost 병기.

## [2026-07-07] 자료넣기 | 올림푸스 GLM 백엔드 연동 구현 가이드
- 📄 신규 [[올림푸스-GLM-백엔드-연동]]: repo(config.sh·run.sh·resilience.sh) 직접 확인 후 작성. 역할 순차실행·각 역할 별도 claude 프로세스 → 빌더 서브셸에만 z.ai env 주입해 구현만 GLM/설계·심판 Claude Pro 유지.
- 🧠 정확한 diff(config.sh BUILDER_MODEL=glm-4.6·ZAI_BASE_URL, run.sh worker() case glm-* env주입, .env.local ZAI_API_KEY) + 무료 Flash 미확인→테스트 절차 + 롤백. 사용자가 이 문서 보고 개발 예정.

## [2026-07-07] 질문 | 예산 ~$20 제약 해법 (§4.7, 사용자 확정)
- 📄 확정: 현재 Claude Pro $20, 그 이상 지출 의향 없음 → Max/GLM Max 옵션 배제.
- 🧠 핵심: GLM 무료 Flash($0)가 지렛대. 추천 ①Claude Pro 유지+잡일(헤파이스토스)만 GLM 무료 Flash 오프로드(추가 $0) ②GLM Coding Plan Lite $18로 갈아타기(프롬프트쿼터 테스트) ③전역할 Flash 무료 실험. verify.sh 게이트라 싼 구현모델 안전.

## [2026-07-07] 질문 | GLM vs Claude 예상비용 시나리오 (§4.6)
- 📄 단가표(Opus$5/$25·Sonnet인트로$2/$10·GLM-4.6$0.6/$2.2·Air$0.2/$1.1·Flash무료) + 🧠 "1 표준 run" 가정(신규3M+캐시30M+출력2M)으로 run당 추정: Opus≈$80 / GLM-4.6≈$9.5 / Air≈$3.7 → **1/8~1/20**.
- 🧠 월 강도별 총비용표. 결론: Claude구독=정액이나 캡 벽, 무거우면 GLM Coding Plan Max$160<Claude$200 / 캡 싫으면 GLM API. 비율은 견고, 절대값은 /usage 실측 후 재보정 권고.

## [2026-07-07] 질문 | Claude 플랜 vs GLM 비교 + 올림푸스 효율 문제
- 📄 [[GLM-Zhipu-Z-ai]] §4.5 신설: Claude 구독(Pro $20/Max5x $100/Max20x $200, 주당 Opus~40h/Sonnet~480h) vs GLM 비교표. 사용자 관찰(올림푸스 4세션 병렬→Opus시간 캡 빨리 소진, "토큰 너무 적음") 확정 기록.
- 🧠 제안: ①GLM API 종량제(주당 캡 없음)로 올림푸스 백엔드 ②GLM Coding Plan Max($160<$200) ③심판/설계=Claude·구현=GLM 이중화(verify.sh 게이트라 교체 안전). index takeaway 갱신.

## [2026-07-07] 자료넣기 | GLM(Zhipu/Z.ai) 모델·요금 웹 스크랩 정리
- 📄 신규 페이지 [[GLM-Zhipu-Z-ai]]: 모델 라인업(GLM-4.5~5.2·무료 Flash) + API 요금표(공식 z.ai) + Coding Plan 3티어(Lite $18/Pro $72/Max $160) + GLM-4.6 스펙(200K·357B MoE·MIT).
- 🧠 사용자 관점 적용: [[올림푸스-Olympus]] 토큰비·[[CogInsight-Generator]] 백엔드(현 gpt-4o) 저가 대체 후보로 프레이밍. ⚠ 중국 모델→회사 데이터 거버넌스 주의 명시. index.md 도구/스킬에 등록.

## [2026-07-06] 자료넣기 | CogInsight 시나리오 레퍼런스 6종 제작·등록 + few-shot 전/후 비교 (로드맵 항목 1·2 완료)
- 📄 산업군별 미니봇 6종(계좌 잔액 조회/배송 조회/반품 접수/대량주문 견적/진료 예약/이용 안내 FAQ)을 **생성기 초안→수동 교정→품질 게이트→dev 등록**으로 제작. 게이트 6/6 PASS, dev 6건·프로덕션 0건(격리 유지).
- 📄 **few-shot 첫 실검증**: 전/후 비교에서 3개 fixture 전부 `injected=true`, 산업군별 올바른 레퍼런스 선택(picked), `rules_hash` 완전 동일(순수 레퍼런스 효과 분리 — 관측성 스냅샷의 실전 성과). ROADMAP 항목 1·2 ✅, 항목 4 부분 완료.
- ⚠ 발견 2건: ① 도매 초안에서 **백로그 1번(LLM flag 루프 탈출 set 누락)이 실재현** — 하네스가 잡아내고 교정으로 해소(하네스 실전 첫 성과) ② few-shot 도입 후 api-esd에 `placeholder-leak` 신규 FAIL — Instruction Bleed형 부작용을 하네스가 포착, 항목 6 백로그. → [[CogInsight-Generator]] 갱신.

## [2026-07-06] 자료넣기 | CogInsight 시나리오 레퍼런스 dev 사본 체계 구축 — dev_coginsight_scenario_references + 승격 규약
- 📄 사용자 확정: 레퍼런스 등록은 **dev 사본에서 테스트 후 프로덕션으로 마이그레이션(승격)**. `dev_coginsight_scenario_references` 생성(프로덕션 미러, 0건) + generator·scenario-references 함수 T() 배선 + `scenario-references-dev` 슬러그 + 프론트 devable 전환 + 러너 `--only` 필터. 승격·리셋 절차를 저장소 CLAUDE.md DEV 규약에 명문화(dev 테이블 3→4개, 래퍼 5→6개).
- 📄 **dev 스모크 전수 통과**: 등록→dev 1건/프로덕션 0건(격리)→조립→few-shot 생성 `injected=true`·`picked=[스모크-진료예약봇]`→정리(dev 0건 복귀, 프로덕션 0건 재확인). 프론트 빌드 그린. 브랜치 `feat/v0.3.0-observability-regression`에 2커밋 추가(총 16), origin 푸시.
- ⚠ DDL은 Management API 토큰(과거 방식: `mailer/.env`의 `SUPABASE_ACCESS_TOKEN`)이 자동 모드에서 차단돼 사용자가 `!`로 직접 실행 — 다음부터 CogInsight `.env.local`에 토큰 두면 자동화 가능. → [[CogInsight-Generator]] 갱신. 다음 단계 = 로드맵 항목 1(산업군별 레퍼런스 제작·dev 등록).

## [2026-07-06] 질문 | Instruction Bleed 개선 논의 → CogInsight 생성 관측성 + 프롬프트 회귀 하네스 구현 (dev 전용)
- [[AI-주간-소식-2026-W26]]의 **Instruction Bleed**(프롬프트 모듈 교차 간섭)를 [[CogInsight-Generator]]에 적용할 개선안 논의 → 사용자 승인으로 **설계→계획→구현까지 완료**. 📄 브랜치 `feat/v0.3.0-observability-regression`(13커밋, origin 푸시 완료, main 미머지 — dev 전용 규약 준수).
- **Part C 관측성**: 모든 생성 결과 `generation_tiers`에 `scenario_examples`(few-shot 주입 기록 — "조용한 skip" 제거)·`rules_snapshot`(규칙 세트 SHA-256 지문 + 스테이지별 해시 = 다단계 규칙 blast radius 노출) 기록. DDL 없음.
- **Part A-lite 회귀 하네스**: `scripts/prompt-regression/` — fixture 3종(수집형+검증루프/LLM Q&A/API+ESD) × 속성 어서션(welcome 루트·anythingelse 1회성·단일부모·도달성·llmloop 빈 키/모델·**flag 루프 탈출 set 존재**(백로그 "육안 확인"의 자동화)·placeholder leak). `coginsight-generator-dev` 실호출, 질문 text 매칭(dev 리셋 id 재발급 대응).
- **기준선 확보**: 레퍼런스 등록 前 3 fixture 전부 PASS(`runs/2026-07-06-baseline.json`) = 로드맵 항목 2 "전/후 비교"의 '전' 데이터. 서브에이전트 구동 개발(태스크 6개+리뷰 게이트, 최종 판정 Ready).
- ⚠ 발견: `.env.local`의 `VITE_SUPABASE_SERVICE_ROLE_KEY` **무효(401)** — anon 키로 우회(dev_questions 읽기 가능). 재발급 필요 시 대비 기록. / 기존 코드-스키마 불일치(`deriveApiDefs.ts`의 'API 이름'·'받을 정보' 필드가 현 템플릿에 없음) — 별도 백로그.

## [2026-07-06] 자료넣기 | CogInsight v0.3.0 로드맵 수립 — 시나리오 레퍼런스 라이브러리 테스트·고도화
- 📄 사용자 확정: **v0.3.0 = 시나리오 라이브러리 테스트·고도화**(레퍼런스 0건·조립 미테스트 → 라이브러리 활용 결과 생성 테스트). 단 **v0.3.0 작업은 프로덕션 무배포·dev 전용**(같은 날 정정 확정) — 배포는 로드맵 문서만. [[CogInsight-Generator]]에 로드맵 섹션 신설 + 진행 현황·업데이트 로그 갱신, 기존 v0.3 후보는 백로그(버전 미정)로 이동.
- 저장소: `ROADMAP.md` 신설 + CLAUDE.md 포인터 — **PR #99 머지 완료**(사용자 승인, main `14cca10`, 문서만). 공개 개요 페이지에 v0.3.0(계획) 행 **재배포 완료**(200 확인) + claude.ai 아티팩트 원본 동기화.

## [2026-07-06] 자료넣기 | AI 다이제스트 2026-07-06 위키화 검증 — W27에 이미 전량 반영 (중복 작업 없음)
- raw/ai-digest/2026-07-06.md(자동 수집 13건, 6/29~7/1 기사)를 [[AI-주간-소식-2026-W27]]과 전수 대조: 📄 **13건 전부 07-05 다이제스트(14건)와 동일 항목**(07-05에만 있던 HP Frontier 1건이 빠졌을 뿐 신규 기사 0건)이라 이미 W27 페이지에 반영 완료 확인. 새 페이지·본문 수정 없음, W27 frontmatter `source:`에 07-06.md 추가·updated 갱신만 수행.
- 🧠 RSS 수집 window가 겹쳐 연속 다이제스트에 중복이 생기는 구조 — 다음 위키화 때도 직전 다이제스트와 먼저 diff 후 신규 항목만 처리하면 됨.

## [2026-07-05] 자료넣기 | AI 주간 소식 2026-W27 위키화 (영문 다이제스트 14건)
- raw/ai-digest/2026-07-05.md(자동 수집, 6/29~7/1 기사 14건) → [[AI-주간-소식-2026-W27]] 신설. 빅 이슈: **SkillOpt**(에이전트 스킬을 학습 가능 파라미터로 — W26 Instruction Bleed의 해법 방향) · **Memora**(저장·검색 분리 에이전트 메모리 — 이 vault 철학과 동일) · **ScarfBench**(엔터프라이즈 Java 마이그레이션 벤치마크 — 내 SM 레거시 경력 접점). 그 외 Gemma 4 실시간 음성, Nano Banana 2 Lite/Gemini Omni Flash(저비용 라인업 지속), Every Eval Ever·GeneBench-Pro(벤치마크 도메인 특화), HP Frontier(엔터프라이즈 레퍼런스), OpenAI 코어덤프 역학조사 디버깅.
- [[AI-주간-소식-2026-W26]]에 다음 주 forward link 추가, index 등록. ⚠ HF/DeepMind 항목 다수는 raw에 제목만 수록 — 해석은 🧠 표기로 분리.

## [2026-07-03] 자료넣기 | 팀숲 베타 발표 덱(pptx) 점수/배점 시스템 위키화
- 루트의 `팀숲-베타시연-발표.pptx`(6/26 발표 덱, 8슬라이드) 텍스트 추출·대조: slide 1~6·8은 기존 [[팀숲-bible-forest]]·[[팀숲-베타-시연-시나리오]]에 이미 반영됨(개요·작동방식·핵심기능·시연흐름·남은작업·회수장치). **slide 7 「점수 배점 — 확정 요청」만 위키에 없던 신규 자료** → [[팀숲-bible-forest]]에 **「점수/배점 시스템」 섹션 신설**(배점 제안 초안 6항목 표 + 확정요청 3건: 랭킹기준 개인→팀·오프라인 입력방법·기간외 활동). 그동안 "기획 필요"로만 남아 있던 **다음 작업 ③ 신약 1독 리워드의 기획 출발점** 확보. 🧠 자동/수동 소스 분리·이중 랭킹 표시범위 등 설계 함의 첨부.
- ⚠️ pptx는 여전히 repo 루트(raw/ 밖)에 있음 — 이동은 사용자 영역이라 보류(기존 로그 방침 유지), 위키엔 출처로만 인용.

## [2026-07-03] 자료넣기 | 팀숲 raw 2건 위키화 검증 — index.md 최신화
- raw/팀숲-배포후-현황·이펙트-역제안(2026-07-03) 2건은 [[팀숲-bible-forest]]·log에 이미 반영 완료 확인(중복 작업 없음). 다만 index의 팀숲 항목이 "7/1 배포 예정"으로 stale → **7/2 배포 완료·서비스 중, 다음 작업(②랭크·이펙트→①도감, ③신약 1독 리워드 기획), 협업 규칙(디자인은 디자이너 경유)** 기준으로 갱신.

## [2026-07-03] 질문 | CogInsight 공개 페이지 그림 A-3 교체 — v0.2.0 UI 실캡처(Playwright CDP)
- 사용자 Chrome 로그인 세션을 임시 프로필(Local Storage·쿠키)로 이전해 CDP(9223)+playwright-core로 프로덕션 앱 설문을 자동 구성(수집·ESD 연동·AI 자유응답=예/문서 검색) → 외부 연동~AI 지식소스 영역을 2x 클립 캡처. 그림 A-3 이미지·캡션("AI 자유응답 필드 — 사용=예 선택 시 지식소스 표시") 교체 — 사용자 피드백으로 조각 크롭 → **앱 전체 화면 캡처**(헤더·v0.2.0 배지 포함, 1440×1200@2x)로 재교체, vercel 재배포·아티팩트 동기화. 캡처 후 임시 프로필(쿠키 사본) 삭제. ⚠ 기본 프로필 CDP는 최신 Chrome에서 차단 — 이 우회가 재사용 패턴.

## [2026-07-03] 질문 | CogInsight 공개 페이지 본문을 v0.2.0 기준으로 개정·재배포
- coginsight-overview.vercel.app 본문 개정: 배지 "현재 버전 v0.2.0", 통계 갱신, 파이프라인에 Stage 3.65/3.7/3.75, 신규 "v0.2.0 — AI 자유응답(LLM 노드)" 섹션(지식소스 표·수집형 체인·키 입력 안내), 매뉴얼 A-2/A-5 보강. 라이브 200·내용 확인, claude.ai 아티팩트 원본 동기화. [[CogInsight-Generator]] SoP 섹션 기록.

## [2026-07-03] 프로젝트업데이트 | CogInsight v0.2.0 프로덕션 릴리스 — 4축 완료·dev 리셋·버전 히스토리 갱신
- **릴리스 수행**: PR #98 머지(`36d0181`, 충돌은 롤백 무효화 merge로 해소 — 잘못 태깅된 v0.2.0을 삭제 후 재태깅), tag `v0.2.0`+GitHub Release, DB 마이그레이션 6개 push·재조회 검증(AI 질문 3행·규칙 2행 dev 일치), 프로덕션 함수 5종 배포, **프로덕션 스모크 생성 전수 통과 후 삭제**, Vercel 번들 v0.2.0 확인.
- **dev 리셋(규약)**: dev_ 테이블 프로덕션 미러 재시드(diff 0)·results 비움. ⚠ 질문 id 재발급 — 이후 dev 테스트는 새 id.
- **문서**: [[CogInsight-Generator]] 릴리스 기준 전면 갱신(스냅샷·진행 현황·v0.2.0 블록·버전표), 공개 페이지(coginsight-overview.vercel.app) 버전 히스토리에 v0.2.0 행 추가·재배포(200 확인).

## [2026-07-03] 질문 | CogInsight — STAGE 3.75 api 결과 예외 처리 보장 추가, 홀드 지점 c4b97bf
- 사용자 요구("api 결과에는 항상 예외 처리") 반영: 레퍼런스(한화 봇) 관용구 [성공 자식(저장 변수 조건)→catch-all 실패 output]을 모든 api 노드에 결정론 보장(apiResultGuard.ts, deno 203 tests). dev 재검증 `d7083216` 통과. [[CogInsight-Generator]] 홀드 지점 `c4b97bf` 갱신.

## [2026-07-03] 질문 | CogInsight — LLM-구동 플로우 체인(수집형 새 규격) 구현·검증, 홀드 지점 886f55f로 갱신
- 사용자 재정의(시나리오 LLM은 Q&A 부착이 아니라 llmloop이 플로우 자체를 구성 — 항목별 전담 llmloop·tool 분기·기본 응답) 반영: `llmFlowChain.ts` 체인 규격 구현(TDD 197 tests), 루트 부재 결정론 보장, docsearch 카탈로그 제외, 규칙·마이그레이션(130000). dev API 매트릭스 `bc678750` 전수 통과(2단계 체인+ESD 재배선+전 경로 회귀). [[CogInsight-Generator]] v0.2.0 블록에 "확장 2" 추가, 홀드 지점 `886f55f`.

## [2026-07-03] 자료넣기 | 팀숲 — 랭크 이펙트 진행 방식 확정 (사용자 구두 확정)
- 이펙트는 **프론트(유혁상)가 공개 에셋/라이브러리 조사 후 역제안**, 2026-07-03 밤 진행 예정. raw/팀숲-이펙트-역제안-사용자전달-2026-07-03.md 보관, [[팀숲-bible-forest]] 다음 작업 표 갱신.

## [2026-07-03] 자료넣기 | 팀숲 — 배포일 7/2 정정·협업규칙·다음 작업 3건 (사용자 구두 확정)
- 사용자 전달을 raw/팀숲-배포후-현황-사용자전달-2026-07-03.md 보관, [[팀숲-bible-forest]] 정정·보강: **배포일 7/1→7/2 정정**(PR 머지 7/1과 하루 차이 명시), **협업 규칙 신설(디자인은 무조건 디자이너 경유** — 소통 오류 소요 후 합의), 다음 작업 **②랭크·이펙트→①도감 순 디자인, ③신약1독 리워드(신규, 기획 필요)** 우선순위 확정.

## [2026-07-03] 프로젝트 업데이트 | 팀숲 Bible Forest — 배포 완료·운영 중 반영
- GitHub `seongjinYU/bible_forest`(public) 직접 확인해 [[팀숲-bible-forest]] 갱신: **7/1 배포 완료(dev→main PR #4), 라이브 bible-forest-lake.vercel.app 운영 중**. 시연 피드백 4건 중 2건 구현(닉네임 중복→"이어가기 팝업" 방식, 닉네임 수정), 배경보기·도감은 미구현 추정. 가중치 랜덤+랭크 B/A/S(65/30/5%) 구현, 파비콘 완료. z_index serial 이슈는 `Date.now()` 방식으로 종결, 동시성·타임존 버그 5건 수정(concurrency-fixes.md), troubleshooting.md(포트폴리오용 템플릿) 신설 반영.

## [2026-07-03] 자료넣기 | 올림푸스 실행 런북 + 새 환경 부트스트랩 신설
- 실행 세팅 문서 요청 → [[올림푸스-실행-런북]] 신설(config.sh·run.sh·reset.sh 직접 확인): 매실행 env·spec·노브 표·폰 개입·복붙 체크리스트. index 등록 + [[올림푸스-Olympus]]·[[올림푸스-기획요청서-작성요령]] 상호링크.
- 추가 요청 "새 환경 세팅법" → §A를 **새 기기 부트스트랩 전체 절차**로 확장: 사전요구→repo 클론→claude CLI(setup-token)→gh→.env.local(SMTP=IMAP 공용)→olympus-inbox 클론(자동클론 안 됨 주의)→검증 스모크(run_tests·notify dry-run·IMAP 로그인). 의존성 최소(bash·git·python3 stdlib·claude·gh), macOS bash 3.2 대응 명시.

## [2026-07-03] 질문 | 올림푸스 원격 브리지 재검토 → 최종 승인 Gmail 답장 경로 구현·E2E
- 브리지 과설계/토큰/더 나은 방식 고민 → "구조 유지, 최종 승인(잦은 yes/no)만 경량화" 결론. 블로커·의도질문=GitHub 유지, 최종 승인=**메일 답장 첫 줄 y/n**(신규 서비스 0, SMTP 앱비번 IMAP 재사용). `inbox_imap.py`+`remote_approve_email`+`run.sh` 분기, 라이브 E2E 통과(발송→폰 y→감지). 실버그 1건(bash 3.2 빈배열 crash) E2E로 포착·수정. 올림푸스 repo PR #2 스쿼시 머지 완료(main `5178882`). [[올림푸스-Olympus]]·[[올림푸스-기획요청서-작성요령]] 갱신.

## [2026-07-03] 질문 | CogInsight v0.2.0 머지 전 최종 검증(전 기능 매트릭스) — 버그 1건 발견·수정 후 전수 통과
- dev API로 시나리오 6종(docs/general/mixed+수집·검증루프/미사용/API 연동/ESD 연동+LLM 결합)+전역 둘 다(docs)를 한 봇으로 생성해 전수 점검. **메뉴 llmloop 주입이 시나리오 llmloop에 가려지는 결합 버그** 발견 → TDD 수정(`9a5e96a`, deno 185 tests) → 최종 `8598c9c5` 전 항목 통과(API 정의·ESD 스키마는 generation_tiers 별도 산출물임도 확인). [[CogInsight-Generator]] 홀드 지점을 `9a5e96a`로 갱신.

## [2026-07-03] 프로젝트업데이트 | CogInsight v0.2.0 확장(지식소스·시나리오 LLM) 후 홀드 기록
- [[CogInsight-Generator]] 갱신(라이브 repo git log + dev API 실생성 검증 근거): 7/3 오후 확장 — 생성 결함 3건 수정(anythingelse 1회성 STAGE 3.65·챗봇 정보 prompt·레퍼런스 풀 body), LLM 지식소스 3종(문서/일반/혼합)+시나리오별 LLM(하이브리드 배치), apiKey·model·storeId 빈 값 불변식. **v0.2.0을 `3ca4282`(650커밋·마이그레이션 62)에서 홀드**(사용자 지시) — 진행 현황·v0.2.0 블록·머지 주의(미적용 마이그레이션 5개)·업데이트 로그 반영.
- 특이 기록: 공유 templates 테이블에 시나리오 AI 필드 2개 라이브 반영(사용자 승인), dev 최종 샘플 결과 `09bde7a9`(지식검증봇_V5).

## [2026-07-03] 프로젝트업데이트 | 올림푸스 토큰 소진 자동 대기·재개 반영
- [[올림푸스-Olympus]] 갱신(이번 세션 직접 구현 근거): §헤드리스 무인 실행에 원격 결정 브리지(`REMOTE`)·**토큰 소진 자동 대기·재개(`TOKEN_WAIT`, `resilience.sh`)** 추가, §현재 상태에 "무인 실행 안정성 강화" ✅, 진행 로그 2026-07-03 추가, frontmatter updated 갱신.
- [[올림푸스-기획요청서-작성요령]] §6 실행에 `TOKEN_WAIT` 사용법(런타임 기능·요청서에 쓸 필요 없음·끄기/간격 노브) 반영.
- 근거: `qtw9723/olympus` main 머지·푸시(`d3fd8bb`, 사용법 doc `6ed7db8`). 크로스플랫폼(macOS+Windows), 대기 중 토큰≈0. 한계=프로세스 종료 시 유실→재실행으로 재개(B안 후속).

## [2026-07-03] 프로젝트업데이트 | CogInsight v0.2.0 구현→롤백→dev 테스트 체제 반영 + apiKey 마스킹 기록
- [[CogInsight-Generator]] 갱신(라이브 repo git log + Supabase DB 직접 조회 근거): v0.2.0 섹션을 "설계만"→"구현 완료·main 롤백(PR #97)·dev 테스트 중"으로 교체, DEV 테이블 모드·워크플로우 규약(저장소 CLAUDE.md `5c4bb3d`) 기록, 진행 현황 수치 갱신(커밋 646·엣지함수 26·마이그레이션 60), 7/3 로그 추가.
- 보안 정리 기록: 레퍼런스·결과 JSON의 비어있지 않은 apiKey 8건 전수 마스킹(재스캔 0건). ⚠ 프로덕션 머지 시 llm 마이그레이션 3개 미적용·no-op 주의를 위키에 명시.

## [2026-07-02] 자료넣기 | MSW 개발 레퍼런스 작성 + 게임 컨셉 확정·기획서 이관
- [[개발-위시리스트-메이플스토리]] 콘테스트를 넥슨 코리아 트랙 공식 요강으로 확정(언어 Lua). 브레인스토밍으로 게임 컨셉 확정 = **턴제 몬스터-소환 덱빌딩 로그라이크**(직업 하이브리드, 결정론+데이터구동+순수Lua코어/MSW바인딩 분리).
- 올림푸스용 기획서 6종 작성 → **정본을 `sj-wiki/specs/MonsterBookSaga/`로 이관**(동기화·타기기 진행용, 올림푸스 spec은 gitignore).
- [[MSW-개발-레퍼런스]] 신설: 공식 API+커뮤니티 실코드 종합(Entity/Component·이벤트 함수·서버/클라 실행모드·DataStorage·UI 컴포넌트). 기획서 04 §4.5 확인항목 대응표(문서확인/hands-on 구분) 포함. index 도구/스킬에 등록.

## [2026-07-02] 프로젝트업데이트 | 3개 프로젝트 라이브 저장소 재확인 후 최신화 (mailer·CogInsight·올림푸스)
- 사용자 요청("위키화 진행하되 각 프로젝트는 실제 소스 확인하며 최신화")으로 병렬 조사 에이전트 3개가 각 repo git log·diff·파일 확인 → 근거(커밋/파일) 기반 갱신.
- [[mailer]] (6/25→7/2, 179→**192커밋**, +13 전부 main 병합): Grafana AI 로그분석 고도화 반영 — ①과거 히스토리 참조 분석(`listTypesWithHistory`, PR #22) ②AI 전용 메모 `ai_note` 영속화(PR #22) ③분석 재시도(지수백오프)+발송/분석 디커플링(`b2b8830`, "분석 실패 시 그날 유실" 버그 해소) ④리포트 메일 가독성·딥링크(PR #21, `GRAFANA_REPORT_URL` 제거). 마이그레이션 2건 추가(총 15). 기능·DB진화·진행현황·포트폴리오 포인트·frontmatter 갱신.
- [[CogInsight-Generator]] (7/1→7/2): 🚧 **v0.2.0 AI 자유응답(LLM 노드) 블록 설계 착수**를 백로그에 추가 — ⚠ 설계 문서만(`d6e57d5`, 브랜치 `feat/llm-response-block`)·코드 0줄·미머지·**버전 v0.1.0 그대로**임을 명시. PR #93(낡은 개요 초안 폐기, 7/1) 로그 기록.
- [[올림푸스-Olympus]]: 이미 7/2 리네임까지 최신 → 정밀 보정 1건(Mindboard는 커밋 0인 로컬 작업 트리 산출물이지 커밋 저장소 아님).
- notepad/parking/schedule-reporter/몬스터게임: 위키 갱신일 이후 소스 변경 없음 → 현행 유지. 팀숲·콜링: 로컬 저장소 없음(교회 git/기획)이라 소스 확인 불가.
- [[index]] mailer·CogInsight 요약 줄 갱신.

## [2026-07-02] 프로젝트업데이트 | 올림푸스 리네임 완료 (dev-pipeline → olympus)
- 사용자 지시로 실제 이름 정리 수행: 로컬 dir `~/IdeaProjects/dev-pipeline→olympus`(mv), GitHub `qtw9723/dev-pipeline→olympus`(gh repo rename), 코드 참조 커밋+push(`640bc3a`), spec를 `spec/Mindboard/` 하위폴더로 정렬, `.DS_Store`·`.claude/` gitignore.
- [[올림푸스-Olympus]] §계보 ⚠박스→✅로 전환, 현재상태·진행로그에 리네임 완료 반영.

## [2026-07-02] 프로젝트업데이트 | 올림푸스 라이브 저장소 반영 + 이름·저장소 정정
- 라이브 저장소(`~/IdeaProjects/dev-pipeline`, GitHub `qtw9723/dev-pipeline`) 직접 확인 후 [[올림푸스-Olympus]] 보강.
- ⚠ 정정: 위키가 `qtw9723/olympus`로 이름·구조 정리·push 완료라 기술했으나, 실제로는 **repo·로컬 디렉토리 모두 여전히 dev-pipeline**이고 "Olympus" 리네임은 **미커밋 워킹트리 수정**(README 제목·config.sh·run.sh)뿐임을 §계보 ⚠박스로 명시.
- 신규 `## 진행사항 업데이트 로그`: 역할별 모델(planner/critic=opus-4-8, builder=sonnet-4-6=비대칭 원칙 증거), 커밋 이력 6개(06-29~07-01), spec/의 Mindboard 기획서가 도구 규칙과 달리 플랫 배치(미커밋)임 기록.

## [2026-07-02] 건강검진 | 전체 점검 (31페이지)
- 링크그래프 스크립트 점검: **고아 0 · index 미등록 0 · 실질 끊긴링크 0**(모든 페이지 incoming ≥2, 연결성 양호). 끊긴링크 후보 26건은 이전 검진들과 동일하게 전부 정상 — forward-link(`claude-api`·`schedule-to-todomate`·`Gemini`·`GitHub Actions`·`Playwright`·`ProvenanceGuard`), 백틱 리터럴(`![[파일명]]`·`[[개발-위시리스트-<항목>]]`), cross-vault 참조(`sj-wiki-work`), 스크린샷 대기 임베드(mailer `cs-smarthub_*.png`).
- 모순 정밀확인: CogInsight LLM 모델 gpt-4o가 [[공통-기술스택]]·[[CogInsight-Generator]] 일치 / [[콜링]] 리네임 후 옛이름 본문 잔존 0 / [[팀숲-bible-forest]]·[[팀숲-베타-시연-시나리오]]의 "비밀번호 없음"은 콜링 아닌 팀숲 자체 사양이라 모순 아님. stale 낮음(최고 3주, 동향 Opus 4.8 현행).
- 수정사항 없음(건강함). 소프트 항목: AI 주간소식 W26까지 → W27 자료 대기(콘텐츠 인제스트 대상, 건강 이상 아님).

## [2026-07-01] 자료넣기 | 올림푸스(Olympus) 위키화 + 콜링 새 데모 HTML 보강
- `raw/projects/olympus.md` 위키화 → **신규 페이지 [[올림푸스-Olympus]] 생성**(로컬 다세션 자율 개발 파이프라인). 발견: 이 프로젝트 = [[헤르메스-개인비서-Hostinger]] §7-2 `dev-pipeline`의 정식화/졸업판(같은 4역할·verify.sh 계보). 헤르메스 §7-2 콜아웃·notepad 페이지에 [[올림푸스-Olympus]] 교차참조 추가. 의외의 연결점: [[콜링]]·[[팀숲-bible-forest]] 자동 개발 후보, "LLM을 실행으로 검증"([[CogInsight-Generator]]·[[mailer]]) 계열, [[에이전트-자동화-도구]]/[[Claude-Code-업데이트-동향]] workflows를 bash로 손수 구현.
- `raw/교회-일정캘린더-와이어프레임-데모.html`(최신 단일 데모) 정밀 확인 → [[콜링]] 「와이어프레임」에 "새 데모 HTML 상세" 소섹션 신설(인증 3화면·캘린더·일정 모달·관리자 4화면·임시 비밀번호 모달). 설계 정합 2건 부각: **반복 드롭다운=절기(반복 등록) 시연 가능**, **7/17 장소충돌=관리 용이성 라이브 시연**.
- [[index]] 프로젝트 카테고리에 [[올림푸스-Olympus]] 등록, 헤르메스·발표대본 항목 주석 갱신.

## [2026-07-01] 질문 | 콜링 발표 대본 정정 + 발표자료(PDF) 재제작 가이드
- 다운로드 폴더 `콜링 제안서.PDF`(9p) 전체 재확인 = raw 보관본과 동일. 발표자료(PDF)와 오늘 결정(절기=반복등록 1차, 기도제목·소통=로드맵) 사이 정합 충돌 발견.
- 사용자 결정: **대본을 정답으로 삼고 PDF를 새로 제작**. [[교회-캘린더-제안-발표-대본]] 갱신 — 4장 도입계획(절기 반복등록·소통 로드맵), Q&A 2건 추가(절기/기도제목), 체크리스트 결정완료 처리, **「발표자료(제안서 PDF) 재제작 반영사항」 섹션 신설**(슬라이드별 정정: 절기 문구·핵심기능③→로드맵·도입방안 문구).

## [2026-07-01] 질문 | 콜링 — 제안서 신규 2건(절기·기도제목) 처리 확정
- 사용자 결정: **절기 표시 = 1차 포함**(관리자가 반복 절기 일정을 직접 설정하는 방식, 일정 CRUD 반복 기능 재사용) / **기도제목 나눔·성도 소통 = 로드맵 Phase2.5로 이동**.
- [[콜링]] 갱신: 「기능 범위」 표 2행 수정, 경고 콜아웃 → [!check] 해결로 전환, 「확장 로드맵」에 Phase2.5 소통·기도 편입, 「리더십 제안서」 핵심기능③ 처리 표기, 진행 로그 추가.

## [2026-07-01] 자료넣기 | 교회 캘린더 리더십 제안서(콜링) 위키화 + 페이지명 정정
- 사용자가 claude.ai/design 공유 링크로 제안서 위치를 알려줬으나 로그인 필요로 접근 불가 → 다운로드 폴더의 `콜링 제안서.PDF`(9p)로 재확인, `raw/교회-일정공유캘린더-콜링제안서.pdf`에 보관.
- 프로젝트 정식명 **콜링(Calling)** 확인. 페이지에 「리더십 제안서」 섹션 신설(배경·솔루션·핵심기능3·기대효과·도입방안·요청사항 전문 정리).
- 기존 기획 자료와 불일치 발견(⚠️): 제안서의 "절기 자동 표시"·"기도제목 나눔"이 기획 3종·와이어프레임엔 없음 → 「기능 범위」 표에 신규 항목으로 추가하고 경고 콜아웃 남김.
- [[교회-캘린더-제안-발표-대본]] 갱신: 제안서 출처 명시, "개발 기간" Q&A·체크리스트에 제안서의 가정치(파일럿 MVP 2~3개월) 반영(단, 제안서 자체가 "가정"이라 밝힌 값이라 재검토 필요 표시).
- **사용자 요청(2026-07-01)으로 프로젝트명을 콜링으로 정정**: 페이지 파일명 `교회-일정공유-캘린더.md` → **`콜링.md`**로 rename, frontmatter title·aliases(구 이름 보존) 갱신. 백링크 8개 파일([[index]]·[[프로젝트-포트폴리오]]·[[개발-위시리스트]]·[[교회-백엔드-회의-2026-06-12]]·[[팀숲-bible-forest]]·[[교회-개발-회의-2026-06-17]]·log·[[교회-캘린더-제안-발표-대본]]) 전부 `[[콜링]]`으로 갱신, 조사(은/는·과/와) 교정. [[팀숲-bible-forest]]의 "콜링=비밀번호 없음" 옛 설명도 최신(비밀번호+승인제)으로 함께 정정. ⚠️ git add/commit/push는 사용자가 직접 진행(로컬 git lock 이슈로 Claude 쪽 커밋 불가 상태였음).

## [2026-07-01] 프로젝트 업데이트 | CogInsight 개요 공개 페이지 v0.1.0 changelog 교정 (3 surface 동기화)
- coginsight-overview.vercel.app 검수: v0.1.0 changelog에 **앱 버전 배지**가 잘못 포함(실제 PR #85=태그 이후 Unreleased, CHANGELOG.md 기준)·커밋수 612(태그 실제 610).
- 3개 surface 동일 교정: ① 라이브 페이지(vercel --prod 재배포, favicon.svg 동반 복구) ② 편집 아티팩트 1e30660a(동일 URL 재배포) ③ 위키 버전표(70·101·21·69: 612→610, 배지는 v0.1.0 기준선에서 빼고 PR #85로 명시). 배지 사실은 line 114에 이미 정확.
- 낡은 로컬 초안 docs/…초안.md(버전 "1.0.1" 오기) 폐기 — PR #93 머지.

## [2026-07-01] 프로젝트 업데이트 | 교회 캘린더 새 클릭 데모 검수·수정(raw 한시 편집) + 대본 동기화
- 사용자가 raw/교회-일정캘린더-와이어프레임-데모.html 생성 → 대본과 대조 검수. 사용자 승인 하에 **한시적으로 raw 직접 수정**.
- 데모 수정: ① 가시성=내 소속 카테고리만(핵심 pitch 구현) ② 박목사(전체 관리자) 역할 추가(조율 시연) ③ 삭제 반복범위 다이얼로그 ④ 7/17 예수홀 장소충돌 데이터 ⑤ 사용자관리 툴바 버튼 ⑥ 오늘=7/3(발표일).
- 대본 동기화: 3역할 시연·이청년 가시성 문구·조율 관점(박목사·충돌)·회원가입 승인흐름·체크리스트(폰트 CDN 경고, 새 데모로 시연). 프로젝트 페이지 와이어프레임 섹션에 새 데모 등록.

## [2026-07-01] 자료넣기 | 개발 위시리스트 시스템 신규 (마스터 + 메이플스토리)
- raw 2건(개발-위시리스트.md, 개발-위시리스트-메이플스토리.md) 위키화 → [[개발-위시리스트]](교회/개인/회사 3영역 마스터), [[개발-위시리스트-메이플스토리]](개인·게임, 🎯 07 중순 마감).
- 교차링크: [[프로젝트-포트폴리오]]와 역할 분담(진행 중 vs 하고싶은 것), 개인 게임은 [[게임-프로젝트-MonsterCollector-MonsterRank]] 연결. index 등록.

## [2026-07-01] 자료넣기 | 교회 캘린더 로그인 재정정 — 비밀번호 추가
- 사용자: 로그인에 비밀번호도 필요. 최종 = **이름+소속기관+생년월일+비밀번호 + 관리자 승인제**. 직전 '비밀번호 없음' 표기를 기획·대본·index 전부 정정. 비번 분실=관리자 재설정.

## [2026-07-01] 자료넣기 | 교회 캘린더 설계 정정 3건 (로그인·비용·관리용이성) + 대본 반영
- 사용자 결정 반영: ① 로그인=이름+소속기관+생년월일(비번 없음)+관리자 승인제 → 06-17 '이름+팀+비번' 확정안 폐기(구버전 이력보존) ② 비용=1차 개인서버 무료→추후 교회서버 이관 ③ 핵심 강점 '관리 용이성(전체 일정 조율)' 디벨롭.
- [[콜링]]: 로그인 콜아웃 정정+failure 콜아웃, 「핵심 강점」·「비용·배포」 섹션 신설, takeaway·ⓒ·제안·진행로그 갱신.
- [[교회-캘린더-제안-발표-대본]]: 카드 4개로(관리용이성 추가), 해결책·시연 조율관점·도입계획·Q&A(비용/가입승인/로그인)·체크리스트 반영. index 갱신.
- ⚠️ raw 3종 docx·와이어프레임은 옛 로그인 방식 잔존 → 사용자 갱신 필요(Claude는 raw 읽기전용).

## [2026-07-01] 자료넣기 | 교회 캘린더 제안 발표 대본 + 예상 Q&A 작성
- 금요일 제안 발표 준비. 청중=대학부 실무/사역자 + 예산·승인 결정자(혼합), 목표=도입승인+피드백, 15~20분(사용자 확인).
- A안(문제→해결→시연→요청) 확정 → 신규 [[교회-캘린더-제안-발표-대본]]: 5섹션 대본(타이밍·전달팁) + 예상 Q&A(결정자/실무/기술) + 발표 직전 체크리스트.
- 내용은 전부 [[콜링]] 기획(📄) 근거, 대본 문구·Q&A판단은 🧠. 개발기간·운영책임·실비는 ⚠️로 발표자 사전 확정 표시. index 등록.

## [2026-07-01] 프로젝트 업데이트 | 헤르메스 §7-2 구현체 dev-pipeline 반영 + notepad 테스트 인프라
- 라이브 저장소 확인(운영 D): flagship [[mailer]](6/25)·[[CogInsight-Generator]](6/30)는 이미 최신. 뒤처진 2건 갱신.
- [[헤르메스-개인비서-Hostinger]] §7-2: "구상/미구축" → **로컬 구현체 `IdeaProjects/dev-pipeline`**(6/29~30) 반영. 기획자(메티스) 추가된 4역할·5단계·상태파일·헤드리스 자동실행/자율 트리아지·Phase3 미구현 등 📄 정리. 구현현황 callout+표 추가.
- [[notepad]]: 6/29 커밋(vitest+`verify` 게이트, 태그 순수함수 추출) 반영 — dev-pipeline의 `VERIFY_CMD` 검증 대상으로 준비됨(교차링크).

> [!tip] 핵심 takeaway
> 위키에 무슨 일이 있었는지 시간순으로 쌓는 기록장. 최신 항목이 맨 위.
> 형식: `## [날짜] 운영유형 | 제목` (운영유형: 자료넣기 / 질문 / 건강검진 / 셋업)
> ⚠️ 이 vault는 **동기화 대상(개인/포트폴리오)**. 회사 기밀 이력은 PC 전용 `sj-wiki-work` vault의 log에 있다.

---

## [2026-06-30] 자료넣기 | CogInsight 다음 버전 확인·개선 항목(백로그) 기록
- 사용자가 다음 버전에 확인할 2건 제시: ①탈출 set 누락(LLM 의존, 미해결·우선) ②자동 회귀 검증 부재(시뮬 하네스, 급하지 않음).
- [[CogInsight-Generator]]에 "다음 버전 확인·개선 항목 (v0.1.0 이후 백로그)" 섹션 신설(공개 페이지 미노출 명시). 메모리 coginsight-llm-flag-loops에 백로그 포인터 추가.

## [2026-06-30] 자료넣기 | CogInsight 한계 추가 — 변수/JSON 출력 처리 미숙
- 사용자: 변수 처리 미숙 → 솔루션이 JSON을 자동으로 못 뿌려서 JSON 열어 내부 데이터를 키로 직접 써야 함, 개선 필요.
- [[CogInsight-Generator]] "현재 상태 스냅샷" 한계 + "남은 결"에 항목 추가. 개요 공개 페이지(coginsight-overview.vercel.app) 한계에도 일반화해 반영·재배포(아티팩트 동기화). 기존 메모리(함수 금지·정확한 키 참조)에 개선필요 노트 추가.

## [2026-06-30] 자료넣기 | CogInsight v0.1.0 프로토타입 배포 — 현재 상태 스냅샷
- 사용자: "지금 v0.1.0 상태 그대로 프로토타입 배포할 거야, 지금까지 상황 정리해둬".
- [[CogInsight-Generator]] 상단에 "현재 상태 스냅샷 — v0.1.0 프로토타입 배포" 섹션 추가: 앱(coginsight-generator.vercel.app)·개요문서(coginsight-overview.vercel.app) 둘 다 200 확인, 코드 기준선(tag v0.1.0·엣지 v87·612커밋·마이그 54), 버전관리 원칙, 검증/미검증(루프 런타임 탈출 미검증), 이번 세션 한 일 요약.

## [2026-06-30] 자료넣기 | CogInsight 개요·매뉴얼 공개 배포 SoP + 버전 히스토리
- 📄 CogInsight "개요 및 매뉴얼" 아티팩트를 공개 정적 호스팅으로 배포: **https://coginsight-overview.vercel.app** (무계정 열람, Vercel `qtw9723`/프로젝트 `coginsight-overview`, 200 확인). 원본 아티팩트 `1e30660a…`와 mirror.
- [[CogInsight-Generator]]에 "공개 배포 — 개요·매뉴얼 페이지 (운영 SoP)" 섹션 추가: 공개 URL·재배포 절차(`vercel deploy --prod`)·**버전 히스토리 표**(v0.1.0). 공개 페이지에도 "버전 히스토리" 섹션 추가(둘 mirror).
- 메모리 저장: "이 문서 수정해서 적용"=공개 페이지 재배포+아티팩트 동기화+버전표 갱신.

## [2026-06-30] 프로젝트 업데이트 | CogInsight Generator v0.1.0 동결 반영
- 사용자 요청: 프로젝트 업데이트 내용 반영 + 공유용 문서 현행화.
- 📄 라이브(`CogInsight-Generator`) 확인: 총 **612커밋**, 6/29 이후 PR #76~#85. **v0.1.0 프로토타입 동결**(tag `v0.1.0`, package.json 0.1.0, GitHub Release, 엣지함수 coginsight-generator **v87** 기준) + 앱 버전 배지. 결정론 안전장치 체인(Stage 2.9~3.6: 루프 탈출변수 정합화·반복수집 결정론화·검증루프·무의미 컨디션 제거·누적배열 초기화) + API 결과 멘트 노출·placeholder 정리. 마이그레이션 49→54.
- [[CogInsight-Generator]] 보강(신규 X): 개요 버전 1.0.1→v0.1.0, 파이프라인을 안전장치 체인까지 확장, 백엔드 마이그레이션 수치, 진행 현황(6/30)·진행사항 로그(PR #76~#85) 추가. frontmatter updated 6/30.
- [[프로젝트-포트폴리오]](공유용) 현행화: CogInsight 상태 v0.1.0 동결 반영, 팀숲 "6/26 예상 시연"→"베타 시연 완료". updated 6/30.

## [2026-06-29] 프로젝트 업데이트 | CogInsight Generator 최신화 (보고/매뉴얼 작성용)
- 사용자 요청: 곧 작성할 프로젝트 개요·매뉴얼(보고용) 준비 위해 라이브 저장소(`CogInsight-Generator`) 확인 → 위키 최신화.
- 📄 확인: 총 **575커밋**(~6/29), 06-25 이후 PR #42~#67. 엣지함수 20→21·마이그레이션 40→49·solution_rules 7→8 카테고리(`Loop Rule`)·어드민 9→8탭(규칙 학습이 솔루션 규칙 탭에 통합).
- [[CogInsight-Generator]] 보강(신규 페이지 X): 주요 기능에 **반복 루프 생성**·**규칙 학습+정합화** 추가, API 레퍼런스 고도화·변수명 규칙 반영, 기술스택 수치·어드민 탭 갱신, 아키텍처에 루프 하이브리드 사례 추가, 진행 현황(6/29)·진행사항 로그(PR #42~#67) 갱신. frontmatter updated 6/29.

## [2026-06-29] 질문 | 헤르메스 §7-2 확장 — 스펙주도 생성↔비평 개발 파이프라인 방향
- 사용자 요청: "기획서 넣으면 LLM이 자체검증하며 개발 → 두 세션 교차검증·수정 → 요구사항 완료 후 추가기능 추천·상호검증·개발" 파이프라인 방향 설계.
- [[헤르메스-개인비서-Hostinger]] §7-2에 반영: 두 세션 **비대칭(생성자/비평가) 권장**, **5단계 수명주기**(스펙인테이크→빌드루프→수용검증→기능추천(대등모드)→승인분 재투입), 통제장치(승인게이트 2곳·예산상한·다른모델·외부상태·zod 핸드오프), **언어무관 어댑터**(검증 하네스만 교체). frontmatter updated 6/29.

## [2026-06-29] 건강검진 + 자료넣기 | 팀숲 시연 완료·후속 피드백 정리
- 건강검진(25페이지): 끊긴 링크·고아·분류 정합성 이상 0건(후보 전부 false positive — 앵커/forward-link/주석 예시). git도 origin/main과 동일(3df4a45).
- 시연 후속(📄 사용자 전달): [[팀숲-bible-forest]]에 **시연 결과 & 후속 피드백** 섹션 추가 — 시연 완료, 7/1 배포 예정(7/5 주일 논의 중), 피드백 4건(닉네임 중복차단·닉네임 변경·메인 배경보기·요소 도감) + 추가 의견 2건(나무 합치기·팀 마을화=디자인 검토). 개발일정 표에 6/26 완료·7/1 배포 반영. takeaway/frontmatter(updated 6/29) 갱신.
- [[index]] 팀숲 설명 갱신(시연 완료·피드백 요약). 카톡 추가개발 공지문 별도 초안 제공(위키 외).

## [2026-06-29] 자료넣기 | AI 주간 소식 W26 신규 작성 (영문 다이제스트 2건)
- 요청: `raw/ai-digest/2026-06-27.md`·`2026-06-29.md`(ai-crawler 자동수집)를 위키화. 작업 전 pull(승인필요 안내).
- 내용이 6/22~6/26에 집중 → **W26(6/22~6/28)** 주차. W26 페이지 부재 → 주차별 패턴(W24·W25)대로 **[[AI-주간-소식-2026-W26]] 신규 작성**. 6/27 파일이 6/29의 상위집합(arXiv 멀티에이전트 섹션·삼성 추가 포함)이라 둘 합쳐 중복 제거.
- 핵심 픽([[내-프로필]] 관점): ① **Instruction Bleed**(2606.26356, 프롬프트 모듈 간 간섭) → [[CogInsight-Generator]] 6단계 파이프라인 직격 ② **OpenAI Daybreak**(Codex Security·GPT-5.5-Cyber) → [[Claude-Code-업데이트-동향]] security plugin과 동궤 ③ **Gemini 3.5 Flash 컴퓨터 사용** → [[웹-크롤링-기초]] Playwright 보강. + Semantic Early-Stopping·CUGA·삼성 Codex 전사배포 등.
- [[index]] AI/업계동향에 W26 등록(맨 위), updated 6/29. [[AI-주간-소식-2026-W25]] 관련문서에 다음 주(W26) 역링크 추가.

## [2026-06-26] 자료넣기 + 건강검진 | 팀숲 베타 시연 시나리오 등록 + 전체 점검 (26페이지)

### 자료넣기
- `wiki/팀숲-베타-시연-시나리오.md` (미커밋 상태) 등록: 교회 리더·대학부(비개발자)용 6/26 베타 시연 대본 + 장면별 체크리스트 8장면.
- [[index]] 팀숲 카테고리에 `[[팀숲-베타-시연-시나리오]]` 등록.
- [[팀숲-bible-forest]] 관련 문서에 `[[팀숲-베타-시연-시나리오]]` 역링크 추가.

### 건강검진 결과
- ✅ 고아 페이지 해소: `팀숲-베타-시연-시나리오`(인커밍 0) → index·bible-forest에 링크 추가 완료.
- ✅ 분류 정합성: index 팀숲 카테고리에 시나리오 페이지 추가 완료.
- ⚠️ 보고(미수정): `팀숲-베타시연-발표.pptx`가 repo 루트에 있음 → raw/ 규칙상 `raw/`에 있어야 하나 사용자 영역이므로 이동 보류. 사용자가 옮겨주면 raw/에 보관.
- ⚠️ stale 유지: [[Claude-Code-업데이트-동향]] W22까지만(W23~W26 누락). raw 자료 없어 보류 유지.
- ✅ 이상 없음: 끊긴 링크(claude-api·schedule-to-todomate·Gemini·Playwright·GitHub Actions 모두 index 등록 forward-link로 정상), 나머지 분류 정합성 이상 없음.

## [2026-06-25] 자료넣기 | raw 프로젝트 4종 재점검 — mailer 누락 사실 2건 보강
- 요청: raw/projects의 mailer·coginsight·schedule-reporter·parking 4종을 CLAUDE.md 규칙대로 위키화. 작업 전 `git pull --rebase`.
- **완전 확인 결과**: 4개 raw는 직전 커밋 `952dd12`(자료넣기)+`2929963`(건강검진)에서 이미 위키 4페이지·index·log에 정합 반영돼 있었음(working tree clean). 새 페이지 생성 X, 보강만.
- **[[mailer]] 2건 보강**: ① **이중 인증 체계**(`auth` x-app-password 헤더 / `cronAuth` Bearer CRON_SECRET — pg_cron·dispatch용) ② **Supabase 마이그레이션 이력 7건**(스키마 진화 추적). 둘 다 raw엔 있었으나 위키 누락분.
- [[CogInsight-Generator]]·[[schedule-reporter-kakao]]·[[parking]]·[[index]]: raw와 정합 — 변경 없음.

## [2026-06-25] 건강검진 | 프로젝트 갱신 후속 정합성 점검
- 전체 25페이지 점검(사용자 승인 후 수정). 끊긴링크 실제 0건(검출 후보는 전부 false positive: 같은-페이지 앵커 `[[#..|..]]`, mailer png는 `<!-- -->` 주석 내 예시, `[[파일명]]` 규칙 리터럴, log 서술 리터럴, index 등록 forward-link). 고아 0건, index 분류 누락 0건.
- **P1 모순 수정**: [[프로젝트-포트폴리오]]가 어제 갱신과 충돌 → 목록표 정정. schedule-reporter "풀스택(일정+카카오)"→"리포트 스케줄러(⚠️카카오 제거·Grafana 단일페이지)", CogInsight "프론트/배포준비"→"풀스택(Edge Functions 백엔드)/POC 운영", mailer 비고 보강.
- **P2 stale 보강**: [[공통-기술스택]]에 CogInsight가 프론트전용→**풀스택(Edge Functions)** 반영, Edge Functions 사용처(CogInsight·mailer·notepad)·스택매핑 행 추가.
- **P3 forward-link 등록**: [[mailer]]발 신규 끊긴링크 `[[Gemini]]`·`[[Playwright]]`·`[[GitHub Actions]]`을 [[index]] 작성후보 노트에 등록(끊긴링크=추적됨 불변식 유지).
- 팀숲 시연일 6/26 일관·미래(오늘 6/25)로 정상. 영향: 프로젝트-포트폴리오·공통-기술스택·index·log.

## [2026-06-25] 자료넣기 | 프로젝트 업데이트 — mailer·CogInsight 대규모 갱신 + parking API + schedule-reporter 정정
- 사용자 요청: 라이브 저장소를 읽기전용으로 확인해 raw에 최신화 + 위키화(프로젝트 수정 중이라 repo는 미수정). 작업 전 `git pull --rebase`(최신).
- **[[mailer]]** (06-10 이후 +80커밋, 99→179): 병렬 에이전트로 라이브 확인. NOC 관제콘솔 리디자인(디자인토큰·Cmd+K·하트비트·send_log), **Chatbot 모니터링 신설**(Playwright+GitHub Actions+pg_cron 08:30 정시 트리거), **Grafana 쿼리 UI 관리**(하드코딩→DB JSONB+테스트게이트), **Grafana LLM(Gemini) 로그분석**(요약+영속 로그유형+발생시각 보존). raw·wiki 갱신. 시크릿/회사기밀(챗봇 솔루션명·셀렉터·HUB_URL·키) redact·제외.
- **[[CogInsight-Generator]]** (06-09 이후 ~200커밋): 병렬 에이전트로 확인. Flow 1급화(LLM 설계→결정론 전개), 6단계 생성 파이프라인, **데이터구동 규칙엔진(solution_rules SoT)**, 레퍼런스 학습(derive-node-specs/learn-rules), 시나리오/API 레퍼런스 라이브러리, **테스터 OTP 인증·승인·신뢰기기**, 토큰/비용 집계, features·값할당 레거시 제거. LLM=OpenAI gpt-4o(Gemini 아님·혼동 주의). 어드민 자격증명·SMTP 등 제외.
- **[[parking]]**: 라이브 확인. **parking API 연동 정보** 추가(엔드포인트·init 순서·verify_jwt 인증·anon key는 형제 repo .env 공유·CORS 미처리·응답스키마·주의점) → raw·wiki. 인증키 질문 답: parking/.env엔 anon 없고 mailer/notepad/schedule/CogInsight의 .env에 VITE_SUPABASE_ANON_KEY로 저장됨(공개키).
- **[[schedule-reporter-kakao]]** 정정: 06-09 `simplify to schedule settings page only` 리팩터로 **카카오 코드 제거·GrafanaPage 단일페이지로 축소**됨을 확인 → 위키의 구버전 서술(카카오 연동·드래그앤드롭·일정리포팅) 현행화. raw·wiki·index 정정.
- index 프로젝트 한줄설명 4건 현행화. notepad/MonsterCollector/MonsterRank는 06-09 이후 커밋 0 → 변경 없음.
- ⚠️ raw 수정은 본래 Claude 금지(읽기전용)이나 이번엔 사용자 명시 지시("raw파일에 최신정보 넣어줘")로 진행.

## [2026-06-24] 자료넣기 | 모닝 브리핑(Apps Script) 전체 원본 반영 보강
- raw가 요약본→**전체 원본 소스**로 확장됐으나 wiki가 미반영이던 상태 발견(완전 확인 원칙 교차 점검). [[모닝-브리핑-AppsScript]] "설계 포인트"에 소스 근거(📄) 디테일 보강: 메일 수집=스레드 마지막 메시지만+본문 앞 300자 snippet(토큰 절약), 위클리 요일별 그룹핑/종일 처리, 드라이브 폴더 자동생성·저장실패 무해화, 백오프 식(2^n)·muteHttpExceptions 분기, 보조함수(setGeminiKey/checkKey/diagnoseGemini).
- 기존 페이지 보강만(신규 생성 X). index는 변경 없음(이미 등록·설명 정확).

## [2026-06-24] 자료넣기 | 모닝 브리핑(Apps Script) 위키화
- 사용자가 매일 아침 받는 "DAILY BRIEFING" 메일의 정체 위키화 → 신규 [[모닝-브리핑-AppsScript]] 생성.
- 메커니즘: **Google Apps Script** 시간 트리거 → 기본 캘린더(오늘 일정) + Gmail 받은편지함 → **개인 Gemini 무료분(gemini-2.5-flash)** 요약 → HTML 메일 발송(sjpark@) + 구글 드라이브(MWW/) 저장. 위클리는 일정만(Gemini 미사용).
- 🔴 **보안**: 사용자 전달 원본에 Gemini API 키 평문 포함 → raw·wiki 모두 `<REDACTED>` 처리, 키 폐기·재발급 권고 명시. 실제 키는 스크립트 속성 `GEMINI_API_KEY`에만.
- 교차참조: [[Teams-Gmail-캘린더-Gemini-연동]](수집/온디맨드층 ↔ 이건 푸시층) 양방향 링크, [[schedule-reporter-kakao]] 관련문서 추가, [[index]] 도구/스킬 등록. raw: `raw/모닝-브리핑-AppsScript.md`(키 redact).

## [2026-06-22] 건강검진 | 시연일 6/23→6/26 이동 미반영 정합성 점검
- 전 23개 페이지 점검(완전 확인 원칙 적용 — 모든 섹션 교차 점검). **stale/모순 3건 해소** (시연일이 6/26로 이동했는데 잔존 "6/23"):
  - [[index]] 팀숲 설명 "6/23 시연 목표" → "6/26(금, 예상) 시연 목표".
  - [[프로젝트-포트폴리오]] 팀숲 행 "6/23 시연 목표" → "6/26(금, 예상)", frontmatter updated 갱신.
  - [[팀숲-bible-forest]] 가중치 항목 "시연(6/23) 이후" → "시연(6/26 예상) 이후" (같은 페이지 내 6/26과 불일치 해소).
- 🧠 [[교회-개발-회의-2026-06-17]]의 "6/23" 잔존은 **의도적 보존** — 그 회의에서 실제 6/23으로 확정한 역사적 기록(원본 정정 아님). 일정 이동 경위는 [[팀숲-bible-forest]] 개발 일정 표에 "기존 6/23 화에서 이동"으로 명시됨.
- 끊긴 링크 없음(`claude-api`·`schedule-to-todomate`=index forward link, `파일명`=규칙 리터럴, `ProvenanceGuard`=log 백틱 리터럴). 고아 없음. 분류 정합성 OK.

## [2026-06-22] 자료넣기 | 팀숲 시연 전 항목에 '읽은 장 드래그 체크/등록' 추가
- 누락 보완 → [[팀숲-bible-forest]]: 성경 인증 핵심 UX인 **드래그 체크/등록(+여러 권 동시)** 을 시연 전 필수 개발 항목으로 추가(담당 유혁상, 시연 전 개발 필요). 코드 프리징 범위에 포함.

## [2026-06-22] 자료넣기 | 팀숲 디코 공지 기준 갱신(시연 6/26·코드프리징·디코 비동기 논의)
- 디스코드 공지 내용 반영 → [[팀숲-bible-forest]]:
  - **시연 6/23 화 → 6/26 금(예상)** 으로 이동. 개발 일정·takeaway 갱신.
  - **코드 프리징 정책**: z-index 확인 + 로그인 수정까지만 하고 프리징, 이후 작업은 별도 브랜치에서만.
  - 테마(팀별 선택) **테스트 완료** → 시연 전 확인 항목에서 해소.
  - 담당 명확화: z-index=백은률, 로그인=유혁상/유성진.
  - 이미지 공유 UI: 휑하지 않게 **닉네임 함께 표기** 검토(위치·디자인 이다혜 확인 중).
  - 확률표 논의 = **이번 주 디스코드 채팅 비동기 진행**(수/목 바빠 모임 어려움).

## [2026-06-22] 건강검진 | 팀숲 배치취소 폐기 후속 정합성 점검
- 전 23개 페이지 점검. **모순 3건 해소** (모두 "배치취소 폐기" 최종 결정 ↔ 잔존 "배치취소 가능" 표현):
  - [[팀숲-bible-forest]] 핵심 기능 코드블록 "(배치취소 가능)" → "(배치취소 없음 — 회수로만)".
  - [[index]] 팀숲 설명 "배치(취소 가능)" → "배치(취소 없음·회수만)" + 시연 후 항목 명시.
  - [[index]] 회의록 설명 "6/22 디스코드에서 배치취소 허용 추가 확정" → "테마 3종·드래그/멀티권·배치취소 폐기 등 추가 확정"으로 정정.
- 정합성: 테마 선택 주체 표기를 개요 표도 "팀별 최초 로그인자"로 통일(본문과 일치). index frontmatter updated 갱신.
- 끊긴 링크 없음(`[[ProvenanceGuard]]`는 log 백틱 리터럴, `claude-api`·`schedule-to-todomate`·`파일명`은 기존 forward-link/리터럴로 정상). 고아 없음. 분류 정합성 OK.

## [2026-06-22] 자료넣기 | 팀숲 6/23 시연 전 최종 확정사항 반영
- 사용자 12개 항목 확정/정정 → [[팀숲-bible-forest]]:
  - 테마 선택 = **팀별** 최초 로그인자(확정). DB는 기존 `trees`/`species` 유지(일반화 안 함, 단기·폐기 예정).
  - 확률표·랭크·이펙트 = 미정, **시연 후 개발**. 이미지 저장 UI·파비콘도 시연 후.
  - **배치취소 기능 폐기** — 회수(읽기 취소)만. unplace 엔드포인트 폐기.
  - 서버 배포/소스 이전 ✅ 완료. 시연용 디자인 ✅ 완료. 환경변수 분리 안 함(판단).
  - ⚠️ 시연 전 필수: **z_index 마이그레이션 확인**, **로그인 방식 수정**(닉네임 존재 시 로그인/없으면 등록).
  - 신규 "6/23 시연 전 최종 점검 / 시연 후 진행" 섹션 추가.

## [2026-06-22] 자료넣기 | 팀숲 테마·요소·랭크·등록UX·이미지/파비콘 확정 위키화
- 사용자 확정 사양 반영 → [[팀숲-bible-forest]]:
  - 테마 3종 동시 운용(숲=나무·바다=바다생물·밤하늘=별, 최초 로그인자 선택) — 신규 "테마 & 요소 시스템" 섹션.
  - 요소 지급 = 가중치 랜덤, 요소별 랭크 + 랭크별 이펙트.
  - 장 등록 UX: 드래그 등록 + 여러 권 동시 등록 (핵심 설계 결정 표).
  - 이미지 저장(공유) 시 닉네임 표시 + 디자인 필요, 파비콘 추후 제작 — 신규 "할 일/추가 필요" 섹션.
  - 컨셉·핵심 기능·DB 스키마 메모를 요소/테마 일반화로 갱신.
- 🧠 미정/확인필요 표기: 테마 선택 주체(팀별/전체), 가중치 확률표, 랭크 단계·이펙트 사양, `trees` 스키마 일반화.

## [2026-06-22] 자료넣기 | 팀숲 배치취소 결정 위키화
- 6/22 디스코드 확정: 숲에 배치한 나무를 **배치취소(인벤토리 복귀) 가능**으로 결정. 기존 "배치 1회성·좌표 수정 불가" 규칙 폐기.
- [[팀숲-bible-forest]]: 핵심 설계 결정 표에 `배치취소` 행 추가(번복 표시) + `확정 사항(2026-06-22, 디스코드)` callout + API 구조에 배치취소 엔드포인트 🟡 예정 추가. frontmatter updated/source 갱신.
- 배치취소 ≠ 나무 회수(시스템 삭제) 구분 명시.

## [2026-06-22] 건강검진 | wiki 전체 점검
- 점검 23개 페이지. **모순 1건 해소**: [[팀숲-bible-forest]] "배치 1회성" ↔ 신규 배치취소 결정 → 위 자료넣기로 정정.
- **끊긴 링크 1건 수정**: [[AI-주간-소식-2026-W25]]의 `[[ProvenanceGuard]]`(존재하지 않는 페이지) → 같은 페이지 섹션 앵커 `[[#...|ProvenanceGuard]]`로 교정.
- **stale 1건 수정**: [[index]] 회의록의 "✅ 오늘 회의"(6/17 기준) 표현 → "2차 회의"로 정정 + 배치취소 후속 결정 링크 추가.
- 고아 페이지 없음. 분류 정합성 OK(23개 모두 index 등록). forward link(`claude-api`·`schedule-to-todomate`)와 규칙 리터럴(`[[파일명]]`)·이미지 임베드는 정상(의도된 것).

## [2026-06-18] 자료넣기 | 네이버 AI 다이제스트(06-18) 국내 동향 W25 보강
- `raw/ai-digest/naver-2026-06-18.md` (NaverSearch MCP 한국어 수집) 위키화 → 기존 [[AI-주간-소식-2026-W25]]에 「🇰🇷 국내 동향」 섹션 신규 추가(같은 W25 주차, 국내 산업 적용 중심).
- 핵심: **앤트로픽 서울 오피스 개소 + 네이버 Claude Code 도입**(넥슨·삼성·LG CNS 1천명+), 더존비즈온(일반 LLM의 도메인 약점→특화), 포스코DX 1인 N에이전트, 딜로이트 멀티에이전트 거버넌스, 마키나락스 LLM+RAG+XAI, 정부 물가 LLM 추출·표준화.
- 비용/HW/지정학(V4프로·HBM4E·소버린·수출통제)은 저관련 요약만. 취재수첩(AI 산출량 가시화) 메모.
- 교차참조: 글로벌 연구↔국내 실무 매핑(LegalHalluLens↔더존, ProvenanceGuard↔XAI, 제안-검증↔포스코DX) "의외의 연결점"에 추가. [[Claude-Code-업데이트-동향]]에 네이버 도입 노트, [[index]] W25 설명 보강.
- 저관련 단신(정상제이엘에스 교육 MOU·삼성 모듈러홈 등)은 의도적 제외.

## [2026-06-18] 자료넣기 | AI 다이제스트(06-17) 미반영 항목 W25 보강
- `raw/ai-digest/2026-06-17.md` 재대조 → 기존 [[AI-주간-소식-2026-W25]]에 미반영 핵심 7건 추가 보강
- 에이전트 신뢰성: LegalHalluLens(타입별 환각 감사·멀티에이전트 토론), AI 에이전트 네트워크 신뢰성(제안-검증 구조), Tacit Coordination(통신 없는 협응)
- 자동화: DRFLOW(개인화 워크플로우 예측), Trustworthy BDaaS(LLM 오케스트레이션 MLOps)
- 안전/평가: In-Context 평가 인식 / 엔터프라이즈: OpenAI Preply·Oracle Cloud
- "의외의 연결점"에 '평가의 신뢰성'·'제안-검증-종합'·'자동화 라이프사이클' 패턴 추가, [[index]] W25 설명 보강
- 저관련 항목(순수 수학·물리로봇·행정 인사 등)은 의도적으로 제외

## [2026-06-17] 자료넣기 | 팀숲 회의록 위키화 + 설계 문서 업데이트
- 교회 개발팀 2차 회의(2026-06-17) 내용 위키화: [[교회-개발-회의-2026-06-17]] 신규 생성
- [[팀숲-bible-forest]] 프로젝트 페이지 신규 생성 (개요·스택·결정·일정)
- [[프로젝트-포트폴리오]] 팀숲 항목 추가
- [[index]] 팀숲 섹션 신설 + 회의록 2개 항목 정렬
- `D:\Projects\bible_forest\app\docs\backend-decisions.md` 신규 결정 반영: A1 나무 회수 허용(번복)·A3 권 단위 bulk replace·B3 배치 나무 회수 가능·C1 기간 이후 조회 허용·D1 z_index 시퀀스 신규

## [2026-06-17] 자료넣기 | AI W25 보강 (06-17 34건) + 건강검진
- `raw/ai-digest/2026-06-17.md` (34건) 수집 후 `wiki/AI-주간-소식-2026-W25.md`에 신규 6건 추가: OpenAI Deployment Simulation · Intelligence Entropy · ProvenanceGuard(MCP) · 멀티에이전트 동시성 이상 · Strands+LeRobot · DeepMind UK 주택 AI.
- 건강검진 (22페이지): 고아 없음, 끊긴 링크 없음(mailer 이미지 기존 알려진 문제 유지). `웹-크롤링-기초.md` 파이프라인 현행화(WakeToRun · Resend 이메일 · Public 레포 반영).

## [2026-06-17] 자료넣기 | 교회 캘린더 와이어프레임 HTML 직접 검증·반영
- 나열된 raw(docx 3종·디자인프롬프트.md·와이어프레임.zip)는 모두 직전 커밋에서 이미 위키화 완료 확인. `.DS_Store`·펼친 와이어프레임 폴더는 `.gitignore`대로 의도적 제외(zip만 커밋).
- 펼친 와이어프레임 HTML을 직접 열람해 [[콜링]] 「와이어프레임」 섹션 "포함 화면"을 정밀화(관리자 4화면·4단계 역할 매트릭스·마이페이지 카테고리별 역할 배지 명시).

## [2026-06-17] 건강검진 | 전체 점검 (22페이지)
- 고아 2건 해소: ✅ [[AI-주간-소식-2026-W25]](인커밍 0) → [[AI-주간-소식-2026-W24]]에 "다음 주" 링크 추가로 주차 체인 연결. ✅ [[헤르메스-개인비서-Hostinger]](인커밍 0).
- 누락 교차참조 ✅: [[프로젝트-포트폴리오]]에 「그 외 프로젝트(IdeaProjects 외)」 섹션 신설 → [[콜링]]·[[헤르메스-개인비서-Hostinger]] 등록(둘 다 포트폴리오를 가리키나 역링크 없던 문제 해결). frontmatter updated 갱신(W24·포트폴리오).
- ⚠ 보고만(미수정): [[mailer]]가 임베드한 이미지 2종(`cs-smarthub_*.png`)의 `raw/assets/`가 repo에 부재 → 다른 기기에 원본 추정, 사용자가 넣어야 복구. [[Claude-Code-업데이트-동향]] W22까지 stale(경고 기존재)·raw 입수 후 갱신 보류 유지.
- 이상 없음: 분류 정합성(전 페이지 index 등록), forward-link(`claude-api`·`schedule-to-todomate`)·리터럴(`파일명`) 기존 결정대로 정상.

## [2026-06-17] 자료넣기 | 교회 캘린더 계정 정책 3건 확정 + 와이어프레임 업데이트 프롬프트
- 사용자 결정 반영: ① (이름+팀) 유일식별, 비밀번호는 인증 전용(식별자로 쓰는 건 안티패턴이라 폐기), 동명이인은 생년월일 보조 ② 비밀번호 분실→관리자 임시 발급·재설정(다음 로그인 변경 강제·감사로그), `/forgot-password`는 관리자 요청 안내 ③ 팀 변경 시 로그인 팀 목록·마이페이지 소속 즉시 갱신.
- 반영: `기술설계서.docx` §6.4 신설(python-docx로 6.3 뒤 삽입), `기능화면정의서.docx` §4.11 신설(4.10 뒤 삽입), `디자인프롬프트.md` 화면2(동명이인)·8(비번 재설정·팀변경)·신규11(비밀번호 찾기) + 「와이어프레임 업데이트 프롬프트」 블록 추가.
- [[콜링]] 확정 콜아웃에 계정 정책 3건 추가, 진행로그 갱신. (와이어프레임은 클로드 디자인 제작 → 업데이트 프롬프트 제공.)

## [2026-06-17] 자료넣기 | 교회 캘린더 로그인 방식 확정 → 전 자료 싱크
- 사용자 확정: **와이어프레임이 최종** → 로그인 = 이름+소속 팀+비밀번호(소셜·이메일 로그인 미지원).
- 전 자료를 와이어프레임 기준으로 정정: `raw/...디자인프롬프트.md`(화면1 로그인·화면2 회원가입+개인정보 동의), `raw/...기능화면정의서.docx`(로그인 입력/액션/검증·회원가입 입력에 팀 선택 추가), `raw/...기술설계서.docx`(6.2 소셜 로그인→미채택, provider=local, email=식별·연락용으로 강등, password_hash 소셜 null 문구 제거).
- docx는 python-docx로 셀/문단 정확 매칭 편집(부분문자열 오염 방지) 후 무결성 재검증(열기 OK·잔여 충돌어 0).
- [[콜링]] 콜아웃을 ⚠상충→📄확정으로 승격, ⓒ·진행로그·index 정합. 이전 소셜 로그인 안 폐기.

## [2026-06-17] 자료넣기 | 교회 캘린더 와이어프레임(HTML) 위키화 + 파일명 정리
- raw에 들어온 `순서대로 진행` 폴더+zip(교회 캘린더 클릭형 HTML 와이어프레임) → 규칙대로 이름 변경: `raw/교회-일정공유캘린더-와이어프레임.zip`(+ 동명 폴더). 중복이라 zip만 커밋, 펼친 폴더는 `.gitignore` 처리(로컬 열람용).
- [[콜링]] 「화면 디자인」에 '와이어프레임' 하위 섹션 추가: 포함 화면(캘린더 메인·일정 모달·로그인·회원가입·마이페이지·관리자)·카테고리 예시·권한 시연·개인정보 동의 전문.
- ⚠ 로그인 설계 변경 발견·반영: 와이어프레임=**이름+팀+비밀번호(소셜 미지원)** vs 디자인프롬프트=이메일+소셜. 최신 와이어프레임 기준으로 본문(요구사항↔UI·제안) 정정, 상충은 경고 콜아웃으로 명시.
- 잔존 깨진 참조 정리: 관련문서의 삭제된 `피그마프롬프트.md` → `디자인프롬프트.md`+`와이어프레임.zip`. frontmatter source/tags·진행현황·index 설명 갱신.

## [2026-06-17] 자료넣기 | 교회 캘린더 화면 디자인 도구 변경 (Figma → 디자인 웹)
- 화면 생성 도구를 Figma Make → **AI 디자인 웹**으로 변경(디자인 웹에서 바로 작업). 프롬프트 파일 `raw/교회-일정공유캘린더-피그마프롬프트.md` 삭제 → `raw/교회-일정공유캘린더-디자인프롬프트.md`로 교체(특정 도구 비종속, 영어 지시문+한글 UI).
- [[콜링]] 「화면 디자인」 섹션·frontmatter(source/tags)·진행현황·index 설명에서 Figma 표현 제거·정리.

## [2026-06-17] 자료넣기 | 교회 캘린더 Figma Make 화면 디자인 프롬프트
- 새 raw `raw/교회-일정공유캘린더-피그마프롬프트.md`(기능화면정의서 v1.1 기반, 1차 대학부) 위키화.
- [[콜링]]에 「화면 디자인 — Figma Make 프롬프트」 섹션 추가: 디자인 시스템(Pretendard·Navy/Blue·8px 그리드·컴포넌트 라이브러리), 화면 11종, 요구사항↔UI 반영(카테고리별 권한 노출·영혼관리 식별정보·소셜 로그인), 데스크톱 우선 반응형.
- frontmatter(tags+figma/ui, source+피그마프롬프트, updated 06-17)·진행현황·진행로그 갱신. [[index]] 설명 보강.
- ⚠ 정합성 수정: v1.1에서 '고령 접근성' 항목이 삭제됐는데 `제안`에 잔존 → 소셜 로그인만 유지하고 고령 강조 제거.

## [2026-06-16] 자료넣기 | 교회 캘린더 기획 v1.1 개정
- 사용자 피드백으로 기획 3종 개정: 목차(실제 페이지번호) 추가, 배경=여러 카톡방 분산·공지 누락/지연, 그룹 예시=목양기관·봉사기관·교역자, 시나리오=대학부 사역자/교역자, **권한 카테고리별 부여**, **영혼관리시스템 연동**(식별 기본정보 수집→매핑), 로드맵 순서 캘린더→모바일→알림→ERP(인력·재정/회계 제외), 스택 협의가능 명시, 고령 접근성 삭제, **1차 대학부** 우선.
- `raw/교회-일정공유캘린더-*.docx` 3종 최신본 갱신, [[콜링]] 위키 반영.

## [2026-06-16] 자료넣기 | 교회 일정 공유 캘린더 기획
- 새 교회 프로젝트 "일정 공유 캘린더" 기획 → 종합기획서·기술설계서·기능화면정의서 docx 3종 작성, `raw/교회-일정공유캘린더-*.docx`로 보관.
- 신규 위키 페이지 [[콜링]] 생성(카테고리: 프로젝트). 핵심: 카테고리 소속 기반 일정 노출 + RBAC×카테고리 2단계 권한, ERP(인력관리 제외)·모바일 확장 대비.
- 교차링크: [[index]] 프로젝트 카테고리 등록, [[교회-백엔드-회의-2026-06-12]]와 상호링크, [[공통-기술스택]]·[[내-프로필]] 연결.
- 확정(사용자 확인): [[교회-백엔드-회의-2026-06-12]] 프로젝트와 **별개의 신규 프로젝트**이며, **같은 교회 개발팀**에서 다른 구성원들과 진행.
- git: 이전 세션에서 stale `.git/index.lock`으로 보류됐던 commit을 2026-06-17 세션에서 lock 정리 후 commit·push 완료.

## [2026-06-16] 자료넣기 | 헤르메스 개인비서 Hostinger 호스팅 검토
- 웹 리서치로 Hostinger 가격·장단점(공유/KVM VPS/n8n/Docker, 갱신가 폭등 등) 정리.
- 사용자 확정: 헤르메스=전반 업무 포함 개인비서 → 활용방안(n8n 오케스트레이션·LLM 에이전트 컨테이너·하이브리드(Supabase 유지)) 제시.
- 새 페이지 [[헤르메스-개인비서-Hostinger]] 작성, index.md 프로젝트 카테고리 등록.

## [2026-06-15] 자료넣기 | AI 주간 소식 W25 위키화 (영문 RSS 34건)
- `raw/ai-digest/2026-06-15.md` 기반 `wiki/AI-주간-소식-2026-W25.md` 신규 작성.
- 주요: OpenAI Ona 인수(지속형 에이전트 환경) · WorkBench 2026(Claude Opus 1위) · MASLab · Gemini 3.5 Live Translate.
- `wiki/index.md` AI/업계 동향에 W25 등록.

## [2026-06-15] 건강검진 | 전체 점검 (18페이지) + 자동 위키화 충돌 내성 강화
- 고아·분류 정합성·신규 2페이지 형식 이상 없음. 발견 4건 처리:
  - ✅ 끊긴 링크 `[[schedule-to-todomate]]`(Teams 페이지 참조) → index.md "작성 후보(forward link)"로 등록(작성후보 강등).
  - ✅ 이중 기기 구성 명시 → `내-MCP-커넥터-환경`에 Mac(Cowork/위키)+Windows(ai-crawler) 분리 운영 추가.
  - ⚠️ `Claude-Code-업데이트-동향` stale(W22까지, W23~W25 누락) → frontmatter에 stale 경고만 추가, 갱신은 raw 입수 후 보류(사용자 결정).
  - ⏸ `[[claude-api]]`(5곳 참조)는 작성후보로 유지(사용자 결정).
- 별도: `.wiki-sync.sh` 충돌 내성 강화 + `.gitattributes`(log.md union 머지) 적용 — 한 번의 git 충돌이 자동 위키화를 영구 wedge시키던 문제 해결(자가 치유·abort·재시도·백업브랜치 복구).

## [2026-06-15] 건강검진 | 전체 점검 (17페이지) + 교차참조·frontmatter 정리
- 끊긴 링크·고아·분류 정합성 이상 없음(의심 후보 3종 모두 정상: `[[파일명]]`=규칙 설명 리터럴, 이미지 임베드=HTML 주석 내 예시, `claude-api`·`schedule-to-todomate`=index 등록 forward link).
- 발견 3건 처리:
  - ✅ frontmatter `updated` 미갱신 → `index.md`(06-12→06-15)·`log.md`(06-10→06-15) 갱신.
  - ✅ 누락 교차참조 → [[Teams-Gmail-캘린더-Gemini-연동]]로 들어오는 콘텐츠 링크가 없던 것 보완: `schedule-reporter-kakao`·`에이전트-자동화-도구` 관련문서에 역링크 추가.
  - ⏸ [[Claude-Code-업데이트-동향]] stale(W18~W22, 현재 ~W25 약 3주 뒤처짐) → frontmatter 경고 이미 현행화됨, 내용 갱신은 raw 입수 후 보류 유지.

## [2026-06-15] 셋업 | 연동 정상 동작 확인 (사용자 검증)
사용자 확인: 메일(A2 전달)·일정(B1 구독)·Gemini 통합 조회 모두 문제없이 동작 중. 통합 구성 최종 검증 완료.

## [2026-06-15] 셋업 | 통합 구성 완료(읽기 전용: 메일 A2 + 일정 B1 + Gemini)
✅ Gemini 연결 완료. ❎ B2(캘린더 초대 자동등록)는 **사용자 선택으로 미적용**(회의는 B1 구독으로 들어오므로, 새 초대 ~24h 지연만 감수). 페이지 확정사항·C·B2·체크리스트를 완료/미적용 상태로 마감. 남은 선택 항목은 전달 수신 테스트뿐. 최종 구성: 메일=A2(Outlook 자동전달), 일정=B1(ICS 구독), 통합조회=Gemini.

## [2026-06-15] 셋업 | B2 캘린더 자동등록 두 설정 구분 보강
질문 중 정리한 핵심 구분을 위키에 반영: **"내 캘린더에 초대 추가→모든 사람"(핵심, Teams .ics 초대 자동등록의 실제 스위치)** vs **"Gmail의 일정/Events from Gmail"(보조, 항공·예약 추측용·구글이 단계적 제거 중→없으면 생략)**. B2 섹션·체크리스트에 구분 명시(PC 브라우저 전용 주의 포함).

## [2026-06-15] 셋업 | Teams/M365→Gmail·캘린더 실연동 진행 (메일 A1→A2 전환)
설정 진행 중 확정 사실 반영: ✅ 캘린더 B1(ICS 게시→구글 구독) 정상 표시 확인. ❌ 메일 A1(POP)은 POP 토글은 켜졌으나 **앱 비밀번호 미제공(기본 인증 차단)**으로 인증 불가 → ✅ **A2(Outlook 자동 전달)로 전환, 전달 토글 켜짐 확인**. Gmail 주소 `qyw9723@gmail.com`로 확정(`qtw9723`는 git 소유자명, 철자충돌 해소). 페이지에 A1 불가/A2 채택/B1 완료/체크리스트·주소 반영. 남은 단계: B2(초대 자동추가)·Gemini 확장 연결.

## [2026-06-15] 셋업 | Teams/M365→Gmail·캘린더→Gemini 통합 설계 확정
브레인스토밍으로 통합 방향 확정(허브=개인 Gmail, 읽기 전용 단방향, 메일=A1 POP3 가져오기, 일정=B1 캘린더 게시 구독+B2 보완). 기존 [[Teams-Gmail-캘린더-Gemini-연동]] 페이지를 자동전달(A2) 중심에서 A1+B1 확정 설계 런북으로 재작성하고 A2/B2는 대체·보완안으로 보존. index.md 설명 갱신.

## [2026-06-12] 자료넣기 | Teams→Gmail→Calendar Gemini 연동 조사 위키화
- 대화+서칭 결과 → `raw/Teams-Gmail-캘린더-Gemini-연동.md` 저장.
- `wiki/Teams-Gmail-캘린더-Gemini-연동.md` 신규 작성 (.ics 감지·Gemini 분석·자동 초대 추가 3가지 방식, OWA 규칙 설정, 체크리스트).
- `wiki/index.md` 도구/스킬 카테고리에 등록.

## [2026-06-12] 자료넣기 | 교회 개발팀 백엔드 회의 위키화
- 대화 기반 회의 내용 → `raw/교회-개발-백엔드-회의-2026-06-12.md` 저장(회사 아닌 교회 사이드 프로젝트 → 개인 vault 적합, `raw/meetings/` gitignore 회피해 raw 루트에 플랫 저장).
- `wiki/교회-백엔드-회의-2026-06-12.md` 신규 작성 (현황·개인 브랜치 전략·app/docs 문서화·Vercel용 개인 Git 배포·액션아이템). 📄/🧠 구분 표기.
- `wiki/index.md` "회의록" 카테고리 첫 등록(기존 "없음" 대체).
- 투두메이트 "교회-개발"에 다음 회의(2026-06-17 수 21:00) 등록 완료.
- claude.ai 원격 에이전트 `trig_01N49aP6vcKKxFJpzCb1nbpX` 생성: 매일 10:00 KST.
- 동작: git pull → CLAUDE.md 규칙대로 위키화 → git push → KakaotalkChat MemoChat 리포트.
- `wiki/웹-크롤링-기초.md` 전체 파이프라인 다이어그램 갱신.

## [2026-06-12] 셋업 | 크롤러 멀티에이전트 소스 추가 + NaverSearch 재활성화
- `D:\Projects\ai-crawler\crawler.py`: RSS 소스 6→9개 추가 (LangChain Blog, Microsoft Research, arXiv cs.MA), 멀티에이전트 키워드 10개 추가.
- claude.ai 원격 에이전트(`trig_0135s5oX7Xm2gn3NTrgXXQXM`): "멀티에이전트", "에이전트 AI" 키워드 추가 + auto_disabled 상태 재활성화.
- `wiki/웹-크롤링-기초.md` 시스템 현황 갱신.

## [2026-06-12] 자료넣기 | AI 주간 소식 W24 보강 + 크롤링↔주간소식 교차참조
- 수동 보강(사용자 요청)과 18:06 자동 위키화가 같은 페이지를 보강 → rebase 충돌을 정보 보존 방향으로 병합 해결.
- `wiki/AI-주간-소식-2026-W24.md`: raw 23건 중 누락분 반영 — HF Spaces 체이닝 에이전트·Nemotron 3.5 Content Safety는 본문 추가(에이전트/안전 섹션), Gemini RCT(시에라리온)·MIT RAISE PATH는 본문 전체 서술, LSEG·MIT 윤리 심포지엄은 "그 외 수집 항목"으로 기록(Oracle Cloud는 본문에 기존재).
- 의외의 연결점 교차참조: W24 다이제스트가 [[웹-크롤링-기초]]의 ai-crawler 첫 산출물임을 양쪽 페이지에 상호 링크.
- `index.md`는 변경 없음(두 페이지 모두 기등록).

## [2026-06-12] 자료넣기 | AI 주간 소식 W24 위키화
- `raw/ai-digest/2026-06-12.md` (RSS 수집 23건) 기반으로 `wiki/AI-주간-소식-2026-W24.md` 작성.
- 주요 내용: OpenAI IPO S-1 · Codex+GPT-5.5 실사례(Nextdoor·Notion) · Gemma 4 12B · 멀티에이전트 안전 $10M.
- 앞으로 주간 단위로 `AI-주간-소식-YYYY-WXX.md` 형식으로 위키화 예정.
- `wiki/index.md` AI/업계 동향 카테고리에 등록.

## [2026-06-12] 자료넣기 | 웹 크롤링 기초 학습 + AI 뉴스 수집 시스템 구축
- 대화 기반 자료 → `raw/웹-크롤링-기초.md` 저장.
- `wiki/웹-크롤링-기초.md` 신규 작성 (RSS/API/BeautifulSoup/Playwright 4방식 + ai-crawler 시스템).
- Python RSS 크롤러(`D:\Projects\ai-crawler\crawler.py`) + Windows Task Scheduler(08:00 KST) 구축.
- Claude 원격 에이전트(NaverSearch MCP, 09:00 KST) 등록 — `trig_0135s5oX7Xm2gn3NTrgXXQXM`.
- `wiki/index.md` 도구/스킬 카테고리에 등록.

## [2026-06-12] 건강검진 | 위키 전체 점검 (15페이지)
- 고아 페이지·분류 누락 없음. 발견 문제 3건:
  - ⚠️ `Claude-Code-업데이트-동향` W23~W24(6/1~6/12) 2주치 stale — raw 자료 대기 중.
  - ⚠️ `내-MCP-커넥터-환경` macOS 환경 기재 → 현재 Windows 기기 사용 (확인 필요).
  - ✅ `schedule-reporter-kakao` 관련 문서에 `[[공통-기술스택]]` 교차참조 추가 (즉시 수정).

## [2026-06-10] 자료넣기 | 회사 전파사항 1건 → work vault로 라우팅 (이 vault 위키 변경 없음)
- `raw/meetings/2026-06-10_전파사항.md`(회사 프로젝트 전파사항)가 이 vault에 들어옴 → **기밀 분리 원칙(CLAUDE.md §1)에 따라 이 vault에는 위키화하지 않고** work vault(`sj-wiki-work`)로 복사 후 거기서 기존 페이지 4곳 보강(상세 이력은 work vault log).
- 이 vault 원본 파일은 읽기 전용 규칙대로 그대로 둠(`.gitignore`의 `raw/meetings/` 안전망으로 push 대상 아님). 🧠 권장: 원본은 work vault로 옮기고 이 vault에서는 삭제(사용자 작업).
- 클라우드 동기화를 위해 **회사 기밀을 PC 전용 `sj-wiki-work` vault로 분리**(A안).
- 이동: 회사 wiki 8p, 회사 raw(회의록·정의서·커넥터 원본 등), 기존 log 전체 → work vault.
- 정리(redaction): 개인 vault 잔존 페이지들의 회사 참조(회사 페이지 링크·사내 플랫폼 용어·로컬 경로)를 제거/일반화.
- 이 log는 개인 vault용으로 새로 시작. `.gitignore`·`CLAUDE.md`에 분리 원칙 반영.
- 결과: 이 vault에는 회사 기밀·동료 실명·내부 아키텍처·금액 정보 없음(검증 완료).
