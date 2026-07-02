---
title: MSW 개발 레퍼런스 (메이플스토리 월드 · Lua)
category: 도구/스킬
tags: [메이플스토리월드, msw, lua, 게임개발, 콘테스트, 레퍼런스, api]
source: "MSW Creator Center 공식 문서(개념) + 커뮤니티 실코드(velog @gfs0101·@dohui, 조코딩 튜토리얼) 종합, 확인 2026-07-02"
created: 2026-07-02
updated: 2026-07-02
---

> [!tip] 핵심 takeaway
> 🧠 [[개발-위시리스트-메이플스토리|글로벌 개발 콘테스트]] 출품작(몬스터북 사가)을 [[올림푸스-Olympus]]로 개발하기 위한 **MSW 함수/패턴 사전**. "내부 함수 많다"는 게 사실 — MSW는 **Entity/Component/Property + 서비스 + 자동호출 이벤트 함수** 구조라 API가 많지만, **공식 API Reference + 커뮤니티 실코드로 상당 부분 미리 파악 가능**하다.
> 📄 결론: 기획서 `04 §4.5`의 확인필요 7항목 중 **라이프사이클·UI·저장 API는 문서로 확인됨**(아래 §대응표), **Lua 단독실행(CI)·실제 성능·에디터 감각·제출 빌드는 여전히 hands-on** 필요.
> ⚠ 공식 docs 페이지는 JS 렌더링이라 본문 자동수집이 막힘 → 아래는 커뮤니티 실코드로 교차확인한 것. 최종은 에디터에서 검증.

## 1. 플랫폼 개요 📄
- **언어 = Lua**. 스크립트 문법은 Lua + MSW 전용 API 다수. (드래그앤드롭 제작 + 스크립트 병행)
- **서버-클라이언트 권위 모델**: 다수 클라이언트가 단일 서버에 연결. Entity를 생성하면 **서버·클라이언트 양쪽에 생성**됨. 동기화는 **서버→클라 단방향**(같은 이름 프로퍼티를 같은 값으로 맞춤).
- **Entity / Component / Property** 구조(컴포넌트 기반). 엔티티에 컴포넌트를 붙이고, 컴포넌트의 프로퍼티로 상태를 갖는다.
- 에디터 구성: **Workspace**(리소스 폴더) · **Hierarchy**(부모-자식 계층) · **Property**(컴포넌트 프로퍼티 편집) · **스크립트 에디터**.

## 2. 스크립트 기본 문법 📄
- 스크립트는 **엔티티에 컴포넌트로 부착**해 동작.
- `self` = 이 스크립트가 붙은 컴포넌트. **`self.` = 변수(프로퍼티) 접근, `self:` = 함수 호출**. `self.Entity`로 소속 엔티티 참조.
- 프로퍼티 선언(에디터/스크립트): `Property: [None] number KeyDownTime = 0` 형태(동기화 옵션·타입·초기값).
- 예: `self.Entity.StateComponent:ChangeState("CROUCH")` — 엔티티의 StateComponent 함수 호출.

## 3. 이벤트 함수 (자동 호출) 📄
"기본 이벤트 함수" = 직접 호출 안 해도 특정 조건에 **자동 호출**되는 함수.
- **`OnBeginPlay`**: 컴포넌트 초기화(처음 시작) 시 로직. (초기 세팅)
- **`OnUpdate`**(틱)·기타 라이프사이클 함수 존재(정확 목록은 API Reference).
- **Entity Event Handler**: 특정 이벤트 수신 핸들러. 실코드 예(Z키 입력):
```lua
Property: [None] number KeyDownTime = 0

-- Entity Event Handler: [service : InputService] HandleKeyDownEvent (KeyDownEvent event)
function HandleKeyDownEvent(event)
    local key = event.key
    if key == KeyboardKey.Z then
        self.Entity.StateComponent:ChangeState("CROUCH")
        self.KeyDownTime = _UtilLogic.ElapsedSeconds
    end
end
```
- `HandleKeyDownEvent`(키 입력), `HandleScreenTouchEvent`(화면 터치) 등 **Handle*Event** 계열. 이벤트는 특정 서비스/엔티티에서 발생.

## 4. 서버 / 클라이언트 실행 제어 📄
- 함수 실행 위치를 모드로 지정: **Client · ClientOnly · Server · ServerOnly · Multicast**.
  - 권위 로직(검증·저장) = Server, 입력·연출 = Client, 전체 브로드캐스트 = Multicast.
- 동기화는 단방향(서버→클라)이라, **클라의 요청을 서버가 처리**하고 결과 프로퍼티를 동기화하는 패턴. (클라→서버 호출·이벤트 전달 API의 정확한 이름은 API Reference의 이벤트/함수 섹션 확인 — 🧠 미확정)
- 🧠 1인용이어도 저장 등은 서버 측에서 도는 게 자연스러움.

## 5. 주요 서비스 (Service) 📄
전역 기능은 `_ServiceName:Method()` 형태로 호출(언더스코어 접두).
- **`_DataStorageService`**: 영속 저장(§7).
- **`_HttpService`**: `JSONEncode()` / `JSONDecode()` (테이블↔JSON 문자열).
- **`InputService`**: 키/입력 이벤트(HandleKeyDownEvent 등). [API](https://maplestoryworlds-creators.nexon.com/ko/apiReference/Services/InputService)
- **`UserService`**: 유저 엔티티 조회(userId로 접근).
- **`_UtilLogic`**: 유틸(예: `ElapsedSeconds` 경과시간).

## 6. 주요 컴포넌트 (Component) 📄
- **TransformComponent**: 위치/회전/스케일. **StateComponent**: 상태 전환(`ChangeState`).
- UI 계열: **TextComponent**(텍스트), **SpriteGUIRendererComponent**(스프라이트 UI), **ButtonComponent**(버튼). [TextComponent API](https://maplestoryworlds-creators.nexon.com/ko/apiReference/Components/TextComponent)
- 물리/렌더/애니메이션 등 컴포넌트 다수 → API Reference `Components/` 참조.

## 7. 저장 / 영속화 (DataStorage) 📄 — 도감·해금 저장의 핵심
- 종류:
  - **GlobalDataStorage**: 월드 단위, 이름으로 여러 개 생성 가능. `_DataStorageService:GetGlobalDataStorage("StorageName")`.
  - **UserDataStorage**: **유저당 1개**, userId로 조회. (개인 세이브에 적합)
- 저장/불러오기: `Storage:SetAsync("키","값", callback)` / `Storage:GetAsync("키", callback)`. 동기형 `SetAndWait`/`GetAndWait`, 다건 `Batch`도 있음.
- ⚠ **string 타입만 저장 가능** → 복잡한 테이블(덱·도감)은 `_HttpService:JSONEncode()`로 문자열화해 저장, `JSONDecode()`로 복원.
- ⚠ **사용량 제한** 존재(용량/호출) → 세이브 구조를 콤팩트하게 설계. (Creator Center "DataStorage 사용량 제한")
- 🧠 몬스터북 사가 매핑: 런 상태는 메모리(런 종료 시 리셋), **도감/해금/통계만 UserDataStorage에 JSON으로 영속**.

## 8. UI 제작 📄
- **UI 편집기**로 화면(대화창·HUD) 구성 → 데이터 테이블에 값 세팅 → **스크립트로 호출/갱신**.
- 입력은 **HandleScreenTouchEvent**(터치/클릭), 버튼은 ButtonComponent. 텍스트는 TextComponent로 갱신.
- 🧠 몬스터북 사가: 손패·필드 슬롯·의도 아이콘·에너지/HP를 이 컴포넌트들로 구성. 레이아웃 세부는 hands-on 확정.

## 9. API Reference 위치 📄
- 공식: `maplestoryworlds-creators.nexon.com/ko/apiReference/` — **Services/**·**Components/**·이벤트별 정리. [사용법](https://maplestoryworlds-creators.nexon.com/ko/apiReference/How-to-use-API-Reference)
- 개념 가이드: `.../ko/docs` (루아 기초·서버와 클라이언트·이벤트 함수·DataStorage 등).

## 10. 🎯 기획서 04 §4.5 확인항목 대응표
| # | 확인 항목 | 상태 | 근거/비고 |
|---|---|---|---|
| 1 | Lua 런타임 **단독 실행(CI)** 가능? | ⚠ **hands-on 필요** | MSW는 자체 런타임·API 의존. 순수 코어를 **MSW API 미사용**으로 짜면 표준 Lua로 테스트 가능성은 있으나 미확인(가장 중요한 리스크) |
| 2 | 스크립트 라이프사이클/이벤트 함수 | ✅ **문서 확인** | OnBeginPlay·Handle*Event·Entity Event Handler 문법(§3) |
| 3 | UI 시스템 | 🟡 **대체로 확인** | UI 편집기 + Text/Button/SpriteGUIRenderer + HandleScreenTouchEvent(§8), 레이아웃 세부는 hands-on |
| 4 | 영속 저장 API | ✅ **문서 확인** | DataStorageService, UserDataStorage(userId), string+JSON, 사용량 제한(§7) |
| 5 | 제공 에셋(몬스터/스킬) 목록 | ⚠ **콘테스트 자료·hands-on** | 콘테스트 제공 월드/에셋·에디터에서 확인 |
| 6 | 1인용 구성 자연스러움 | 🟡 **부분 확인** | 서버-클라 모델이나 실행모드로 제어 가능(§4), 실제 구성은 스파이크 권장 |
| 7 | 제출 빌드/게시 형식 | ⚠ **hands-on 필요** | MSW 월드 게시 형태 → 올림푸스 verify "build" 의미 확정 필요 |

## 11. 아직 hands-on이 답인 것 🧠
- **실제 성능**(소환수·이펙트 다수 시 프레임), 에디터 조작 감각·워크플로우, 숨은 제약.
- 위 §10의 1·5·7. 특히 **1번(Lua 단독 CI 실행)**은 자동검증 전략(코어를 MSW 없이 시뮬)의 성패를 좌우 → 스파이크 1순위.
- 🧠 스파이크 계획: ① 빈 월드에 컴포넌트 1개 붙여 OnBeginPlay 로그 → ② InputService로 입력 → ③ TextComponent로 HUD → ④ UserDataStorage 저장/불러오기 왕복 → ⑤ 순수 Lua 모듈을 MSW 안/밖에서 각각 로드 시도(CI 가능성 판정).
- 📋 **상세 투두(다음주 실행용)**: `sj-wiki/specs/MonsterBookSaga/06_MSW_확인_체크리스트.md` — 항목별 할 일·판단 기준·"결과 기록" 칸까지. 그대로 따라 하면 됨.

## 관련 문서
- [[개발-위시리스트-메이플스토리]] — 이 레퍼런스의 사용처(몬스터북 사가 기획서 `04 §4.5`)
- [[올림푸스-Olympus]] — 개발 파이프라인(코어=순수 Lua를 주 개발·검증 대상으로)
- [[공통-기술스택]] · [[웹-크롤링-기초]]
- 출처: MSW Creator Center([docs](https://maplestoryworlds-creators.nexon.com/ko/docs) · [apiReference](https://maplestoryworlds-creators.nexon.com/ko/apiReference/How-to-use-API-Reference)), velog(@gfs0101 msw 스터디, @dohui MSW DataStorage), 조코딩 MSW 튜토리얼
