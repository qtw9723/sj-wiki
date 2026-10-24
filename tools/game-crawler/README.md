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

## 매일 아침 실행

`run_daily.py`가 수집 → 정제를 차례로 실행한다(`--push`를 주면 `raw/games`만 커밋·푸시, 기본 꺼짐).

**Windows PC에서 직접 실행 (선택됨, 2026-10-24)** — 저장소를 클론한 뒤 `tools\game-crawler\setup_windows.bat` 을 한 번 실행하면 모의 테스트 → 실제 수집 시험(5개) → 매일 07:30 작업 등록까지 한다. 실패하면 오류 메시지를 Claude에게 붙여넣는다.

수동으로 등록하려면 (아래 '네트워크' 참고):
```bat
schtasks /Create /SC DAILY /ST 07:30 /TN "sj-game-crawler" /TR "\"<저장소경로>\tools\game-crawler\run_daily.bat\"" /F
```
- 저장소를 PC에 클론해 두고 `<저장소경로>`를 바꿔 쓴다. Python(`py` 런처)과 git이 필요하다.
- PC가 꺼져 있으면 실행되지 않는다. 놓친 실행을 켜질 때 따라잡으려면 작업 스케줄러 설정의 '예약된 시작 시간을 놓친 경우 가능한 대로 빨리 작업 실행'을 켠다.

## 네트워크 (테스트 중 확인한 사실)

- Claude 클라우드 작업 환경과 Claude 데스크톱 앱의 작업 VM은 둘 다 접속 허용 목록 방식이라 `api.steampowered.com`이 프록시에서 **403**으로 막힌다(GitHub은 통과). 그래서 이 두 곳에서는 수집이 안 돌고, **PC에서 직접 실행**해야 한다.
- 해결책은 둘 중 하나: ① PC에서 직접 실행(위 작업 스케줄러), ② 계정의 네트워크 허용 목록에 `api.steampowered.com` · `store.steampowered.com` · `steamspy.com` (+ OpenCritic은 `opencritic-api.p.rapidapi.com`, Metacritic은 `www.metacritic.com`)을 추가.
