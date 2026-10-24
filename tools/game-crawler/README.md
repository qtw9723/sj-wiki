# game-crawler

Steam 유저 평가(점수 × 리뷰 수)로 게임을 선별하고, OpenCritic/Metacritic 평론가 점수와 나란히 비교하는 크롤러.
게임 요소 라이브러리(`wiki/게임요소-라이브러리.md`)에 넣을 후보를 고르는 용도. 설계와 판단 근거는 위키 `게임-크롤러-스팀-크리틱.md`.

## 실행 (저장소 루트에서, 외부 패키지 불필요)

```bash
python tools/game-crawler/crawler.py --self-test                      # 모의 응답으로 로직 검증 (네트워크 불필요)
python tools/game-crawler/crawler.py --source steamspy-top --limit 5  # 첫 실행은 소량으로
RAPIDAPI_KEY=... python tools/game-crawler/crawler.py --source steamspy-top --opencritic
python tools/game-crawler/crawler.py --source steamspy-top --metacritic
python tools/game-crawler/crawler.py --source appids --appids-file my_appids.txt
```

Windows PowerShell에서는 `$env:RAPIDAPI_KEY="..."` 로 키를 설정한다. 키는 `.env`에 두면 `.gitignore`로 커밋이 막힌다.

## 출력 (`raw/games/`)

- `steam-critic-YYYY-MM-DD.json` — 선별된 게임의 전체 수치
- `steam-critic-YYYY-MM-DD.md` — 요약 표(유저 긍정% · 리뷰 수 · Wilson 하한 · 평론가 · 차이 · 판정)
- `reviews-<appid>.json` — `--sample-reviews N` 사용 시 추천 리뷰 N개(400자 절단). 개인 분석용이며 `.gitignore`로 커밋 제외

## 선별 기준

1. SteamSpy 수치로 사전 필터(리뷰 수 ≥ `--min-reviews`, 긍정 비율 ≥ `--min-ratio`)
2. 공식 `IUserReviewsService/GetAppReviews`(전체 언어)로 요약을 다시 확인
3. **Wilson 하한(95%)** 으로 정렬 — 같은 긍정 비율이면 리뷰가 많은 게임이 위
4. 평론가 점수와의 차이가 15점 이상이면 `유저>평론가` / `평론가>유저`로 표시

## 알아둘 점

- **2026-10-24 PC에서 실제 실행 성공**(Steam `GetAppReviews`·SteamSpy·상점 appdetails, 5개 게임, 정제까지 약 50초). 아직 안 돌려 본 것: OpenCritic·Metacritic, `--push`, 작업 스케줄러 등록, `--sample-reviews`. 오류가 나면 `crawler.py`의 `VERIFY` 주석 지점부터 본다.
- `.bat` 파일은 영문·CRLF 줄바꿈이어야 Windows에서 실행된다(`.gitattributes`로 고정). `test_windows.bat`은 작업 등록 없이 모의 테스트 + 실제 5개 수집만 하고 `test_result.txt`에 기록한다.
- Steam 호출은 키 없이도 되지만 한도가 낮고 429가 올 수 있다. 요청 간 대기와 재시도, 24시간 디스크 캐시(`tools/game-crawler/.cache/`)가 들어 있다.
- Metacritic은 공식 API가 없다. `--metacritic`은 robots.txt가 허용할 때만 최선 노력으로 읽으며, 약관은 직접 확인해야 한다.
- 이름이 정확히 같을 때만 평론가 점수를 채택한다(오매칭 방지). 못 찾은 게임은 `평론가 없음`.
- 리뷰 본문은 재게시하지 않는다. 위키에는 규칙·수치 요약과 출처만 남긴다(`게임요소-라이브러리` §6).

## 정제·분류 (`process.py`) — 크롤링 다음 단계

```bash
python tools/game-crawler/process.py            # raw/games 의 가장 최근 steam-critic-*.json 을 정제
python tools/game-crawler/process.py --offline  # 상점·SteamSpy 조회 없이 검증만
```

- **탈락**: 게임이 아닌 항목(상점 `type` ≠ game: DLC·데모·소프트웨어 등), 중복 appid, Steam 요약 없음 — 사유와 함께 기록
- **경고**(통과는 시키되 표시): 긍정 비율 재계산 불일치, 이름 없음, 앞서 해보기(Early Access), 상점 type 확인 실패
- **장르 분류**: Steam 장르 + SteamSpy 태그 → `genre_map.json` → 통제 어휘 `gl_genre`. 매핑표에 없는 태그는 `미분류 태그`로 모아 보고서에 나온다. 어휘표(`게임요소-라이브러리` §4-3)에 추가할 값이면 `tags`에, 필요 없으면 `ignore_tags`에 넣는다
- **신규 표시**: `raw/games/state.json`에 본 게임을 기록해 매일 돌릴 때 새로 들어온 게임만 🆕로 구분
- 출력: `clean-YYYY-MM-DD.json` / `.md`
- 아직 없음: 리뷰 폭탄(최근 리뷰 급변) 탐지, 요소(메커니즘) 추출 — 후자는 대화에서 사람 확인과 함께 한다

## 매일 아침 실행 (PC) — 터미널 명령

`run_daily.bat`이 pull → 수집 → 정제 → **`raw/games`를 GitHub에 push**까지 하고, 출력은 `tools\game-crawler\run.log`에 쌓는다. Python(`py` 런처)과 git이 필요하고, PC에서 `git push`가 되는 상태(GitHub 로그인)여야 push된다.

cmd(명령 프롬프트)에서 한 번만 실행:

```bat
git clone https://github.com/qtw9723/sj-wiki.git "%USERPROFILE%\sj-wiki"
cd /d "%USERPROFILE%\sj-wiki"
tools\game-crawler\test_windows.bat
schtasks /Create /SC DAILY /ST 07:30 /TN "sj-game-crawler" /TR "\"%USERPROFILE%\sj-wiki\tools\game-crawler\run_daily.bat\"" /F
```

- 1~2번째 줄: 저장소를 홈 폴더에 받는다(`Documents\sj-wiki`에는 예전에 실패한 빈 폴더가 있을 수 있어 피한다).
- 3번째 줄(선택): 작업 등록 없이 모의 테스트 + 실제 5개 수집을 하고 `tools\game-crawler\test_result.txt`에 기록한다.
- 4번째 줄: 매일 07:30 작업 등록. `/F`는 같은 이름이 있으면 덮어쓴다.

확인·관리 명령(각각 한 줄씩 실행):

- 지금 바로 실행해 보기: `schtasks /Run /TN "sj-game-crawler"`
- 다음 실행 시각·마지막 결과 확인: `schtasks /Query /TN "sj-game-crawler" /V /FO LIST`
- 실행 기록 보기: `type "%USERPROFILE%\sj-wiki\tools\game-crawler\run.log"`
- 작업 삭제: `schtasks /Delete /TN "sj-game-crawler" /F`

(`setup_windows.bat`은 같은 일을 한 번에 해 주는 래퍼다. 단 위 4번 등록은 `run_daily.bat`을 가리키므로 결과는 같다.)

- 평론가 점수(OpenCritic)를 켜려면 Windows 환경변수 `RAPIDAPI_KEY`를 설정하고 작업에 `--opencritic`을 붙여야 한다(`run_daily.bat`의 인자로 전달됨). 지금은 Metacritic만 시도한다.
- PC가 꺼져 있으면 그날은 실행되지 않는다(Claude 쪽 예약 작업이 "결과 없음"을 카톡으로 알린다).

## 매일 아침 평론 + 카카오톡 (Claude 예약 작업)

PC 실행(07:30) 뒤 **08:17**에 Claude 예약 작업이 그날 결과 파일을 읽고, 위키 `게임-크롤러-일일-평론`에 평론을 남기고, 카카오톡(나에게 보내기)으로 요약을 보낸다. 결과 파일이 없으면 "오늘 결과 없음"만 카톡으로 보낸다. 작업 이름: `게임 크롤링 일일 평론`.

## 매일 아침 요소 정리 (Claude 예약 작업 2)

평론(08:17) 뒤 **08:47**에 `게임 요소 위키 정리` 작업이 돈다. 분석 대상은 **게임이 아니라 게임의 요소**(메커니즘·시스템·수치·레벨·디자인 등)다.

- 입력: 가장 최근 `clean-*.json`에서 **사례 페이지가 아직 없는 게임** 최대 3개(신규 우선). 큐가 비면 아무것도 쓰지 않고 카톡도 보내지 않는다.
- 출력: `wiki/게임요소-사례-<게임>.md`(출처 허브) + `wiki/게임요소-<유형>-<이름>.md`(요소, 게임당 2~4개). 통제 어휘만 사용, `gl_status`는 `수집`(템플릿을 근거와 함께 다 채우면 `정리`), `검증`은 사람이 직접 구현해 본 뒤에만.
- 근거: 웹에서 확인한 것만 📄(출처 URL), 나머지는 🧠. 상용 게임 코드·에셋은 저장하지 않는다.
- 검사: `python tools/game-crawler/lint_elements.py` — 파일명·필수 속성·어휘·끊긴 링크·유형별 필수 섹션을 확인(오류가 있으면 종료 코드 1).
- 끝나면 카카오톡으로 한 번 요약을 보낸다. 어휘표에 없는 값이 필요하면 쓰지 않고 보고서에 "어휘 결정 필요"로 남긴다.

## 네트워크 (테스트 중 확인한 사실)

- Claude 클라우드 작업 환경과 Claude 데스크톱 앱의 작업 VM은 둘 다 접속 허용 목록 방식이라 `api.steampowered.com`이 프록시에서 **403**으로 막힌다(GitHub은 통과). 그래서 이 두 곳에서는 수집이 안 돌고, **PC에서 직접 실행**해야 한다.
- 해결책은 둘 중 하나: ① PC에서 직접 실행(위 작업 스케줄러), ② 계정의 네트워크 허용 목록에 `api.steampowered.com` · `store.steampowered.com` · `steamspy.com` (+ OpenCritic은 `opencritic-api.p.rapidapi.com`, Metacritic은 `www.metacritic.com`)을 추가.
