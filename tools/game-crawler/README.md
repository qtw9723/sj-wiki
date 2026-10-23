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

- 개발 환경에서 외부 사이트에 접속할 수 없어 **실제 API로는 아직 실행하지 못했다.** 첫 실행에서 오류가 나면 `crawler.py`의 `VERIFY` 주석 지점(응답 감싸기, 필드명, 호스트)부터 본다.
- Steam 호출은 키 없이도 되지만 한도가 낮고 429가 올 수 있다. 요청 간 대기와 재시도, 24시간 디스크 캐시(`tools/game-crawler/.cache/`)가 들어 있다.
- Metacritic은 공식 API가 없다. `--metacritic`은 robots.txt가 허용할 때만 최선 노력으로 읽으며, 약관은 직접 확인해야 한다.
- 이름이 정확히 같을 때만 평론가 점수를 채택한다(오매칭 방지). 못 찾은 게임은 `평론가 없음`.
- 리뷰 본문은 재게시하지 않는다. 위키에는 규칙·수치 요약과 출처만 남긴다(`게임요소-라이브러리` §6).
