#!/usr/bin/env python3
"""게임 크롤러 — Steam 유저 평가 + OpenCritic/Metacritic 평론가 점수.

목적: 게임 요소 라이브러리(wiki/게임요소-라이브러리.md)에 넣을 '좋은 게임' 후보를
      유저 평가(점수 x 리뷰 수) 기준으로 선별하고, 평론가 점수와 나란히 비교한다.

의존성 없음(표준 라이브러리만). Python 3.9+.

사용 예 (저장소 루트에서):
    python tools/game-crawler/crawler.py --self-test
    python tools/game-crawler/crawler.py --source steamspy-top --limit 10
    python tools/game-crawler/crawler.py --source appids --appids-file my_appids.txt
    RAPIDAPI_KEY=xxxx python tools/game-crawler/crawler.py --source steamspy-top --opencritic
    python tools/game-crawler/crawler.py --source steamspy-top --metacritic   # 비공식, 약관 직접 확인

환경변수:
    RAPIDAPI_KEY   OpenCritic(RapidAPI) 호출용 키. 없으면 OpenCritic은 건너뜀.
    STEAM_API_KEY  선택. 있으면 Steam 호출에 함께 보냄.

주의 (README.md 참고):
    - 이 스크립트를 개발한 환경에서는 외부 사이트에 접속할 수 없어, 실제 API로는 실행해 보지 못했다.
      --self-test(모의 응답)로 선별·병합 로직만 검증했다. 처음엔 --limit 5로 시험할 것.
    - Steam/SteamSpy/OpenCritic/Metacritic 의 엔드포인트·필드·약관은 바뀔 수 있다. 확인 필요 지점은 'VERIFY'로 표시.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path

UA = "sj-game-crawler/0.1 (personal research; contact: repo owner)"
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
CACHE_DIR = HERE / ".cache"
CACHE_TTL = 24 * 3600

STEAM_REVIEWS_URL = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"
STEAMSPY_URL = "https://steamspy.com/api.php"
OPENCRITIC_HOST = "opencritic-api.p.rapidapi.com"  # VERIFY: RapidAPI 호스트·요금제
STORE_APP_URL = "https://store.steampowered.com/app/{appid}"

GAP_FLAG = 15  # 유저-평론가 점수 차이가 이 이상이면 '불일치' 표시


# --------------------------------------------------------------------------- HTTP
def fetch(url: str, headers: dict | None = None, as_json: bool = True,
          retries: int = 4, pause: float = 1.5):
    """GET 요청. 429/5xx는 지수 백오프 재시도. 24시간 디스크 캐시."""
    key = hashlib.sha1((url + json.dumps(headers or {}, sort_keys=True)).encode()).hexdigest()
    cache_file = CACHE_DIR / key
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        text = cache_file.read_text(encoding="utf-8")
        return json.loads(text) if as_json else text

    req_headers = {"User-Agent": UA, "Accept": "application/json" if as_json else "text/html"}
    req_headers.update(headers or {})
    delay = pause
    last_err = None
    for attempt in range(retries):
        try:
            time.sleep(pause)
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(text, encoding="utf-8")
            return json.loads(text) if as_json else text
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429 or 500 <= e.code < 600:
                wait = float(e.headers.get("Retry-After", delay * 2))
                print(f"  [{e.code}] {wait:.0f}s 대기 후 재시도 ({attempt + 1}/{retries})", file=sys.stderr)
                time.sleep(wait)
                delay *= 2
                continue
            raise
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            time.sleep(delay)
            delay *= 2
    raise RuntimeError(f"요청 실패: {url} ({last_err})")


# --------------------------------------------------------------------------- 점수
def wilson_lower_bound(pos: int, neg: int, z: float = 1.96) -> float:
    """긍정 비율의 95% 신뢰구간 하한(0~1). 리뷰 수가 적을수록 보수적으로 낮아진다."""
    n = pos + neg
    if n == 0:
        return 0.0
    p = pos / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)
    return max(0.0, (centre - margin) / denom)


def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", re.sub(r"[™®©]", "", s).lower()).strip()


# --------------------------------------------------------------------------- Steam
def candidates_steamspy(source: str, pages: int) -> list[dict]:
    """SteamSpy(비공식)에서 후보를 가져온다. positive/negative가 함께 와서 사전 필터에 유용."""
    out: dict[int, dict] = {}
    if source == "steamspy-top":
        for req in ("top100forever", "top100in2weeks"):
            data = fetch(f"{STEAMSPY_URL}?request={req}")
            for k, v in data.items():
                out[int(k)] = v
    else:  # steamspy-all
        for page in range(pages):
            data = fetch(f"{STEAMSPY_URL}?request=all&page={page}", pause=61)  # VERIFY: all은 분당 1회 제한
            for k, v in data.items():
                out[int(k)] = v
    return list(out.values())


def candidates_appids(path: str) -> list[dict]:
    ids = [int(x) for x in re.findall(r"\d+", Path(path).read_text(encoding="utf-8"))]
    return [{"appid": i, "name": "", "positive": None, "negative": None} for i in ids]


def steam_summary(appid: int) -> dict | None:
    """공식 IUserReviewsService/GetAppReviews 로 전체 언어 요약(점수·긍정/부정 수)을 가져온다."""
    params = {"appid": appid, "languages": ["all"], "num_per_page": 5}
    q = {"input_json": json.dumps(params, separators=(",", ":"))}
    key = os.environ.get("STEAM_API_KEY")
    if key:
        q["key"] = key
    data = fetch(f"{STEAM_REVIEWS_URL}?{urllib.parse.urlencode(q)}")
    body = data.get("response", data)  # VERIFY: 응답이 'response'로 감싸이는지
    qs = body.get("query_summary") or {}
    if "total_positive" not in qs:
        return None
    pos, neg = int(qs["total_positive"]), int(qs["total_negative"])
    return {
        "positive": pos,
        "negative": neg,
        "total": pos + neg,
        "ratio": round(pos / (pos + neg), 4) if pos + neg else 0.0,
        "wilson": round(wilson_lower_bound(pos, neg), 4),
        "review_score_desc": qs.get("review_score_desc"),
    }


def steam_sample_reviews(appid: int, n: int) -> list[dict]:
    """추천(helpful) 리뷰 일부. 본문은 400자로 자른다. 개인 분석용 — 재게시 금지."""
    params = {"appid": appid, "languages": ["all"], "num_per_page": min(n, 100)}
    q = {"input_json": json.dumps(params, separators=(",", ":"))}
    data = fetch(f"{STEAM_REVIEWS_URL}?{urllib.parse.urlencode(q)}")
    body = data.get("response", data)
    out = []
    for r in (body.get("reviews") or [])[:n]:
        author = r.get("author") or {}
        out.append({
            "voted_up": r.get("voted_up"),
            "votes_up": r.get("votes_up"),
            "playtime_hours": round((author.get("playtime_forever") or 0) / 60, 1),  # VERIFY: 분 단위
            "language": r.get("language"),
            "text": (r.get("review") or "")[:400],
        })
    return out


# --------------------------------------------------------------------------- 평론가
def opencritic_lookup(name: str, rapid_key: str) -> dict | None:
    """OpenCritic(RapidAPI): 이름 검색 → 상세. 이름이 거의 일치할 때만 채택."""
    headers = {"X-RapidAPI-Key": rapid_key, "X-RapidAPI-Host": OPENCRITIC_HOST}
    base = f"https://{OPENCRITIC_HOST}"
    hits = fetch(f"{base}/game/search?criteria={urllib.parse.quote(name)}", headers)
    if not isinstance(hits, list) or not hits:
        return None
    best = next((h for h in hits if norm_name(h.get("name", "")) == norm_name(name)), None)
    if best is None:
        return None  # 보수적: 이름이 정확히 같을 때만 (오매칭이 누락보다 해롭다)
    d = fetch(f"{base}/game/{best['id']}", headers)
    score = d.get("topCriticScore")
    if score is None or score < 0:
        return None
    return {
        "id": best["id"],
        "score": round(float(score), 1),
        "percent_recommended": d.get("percentRecommended"),
        "num_reviews": d.get("numReviews"),
        "tier": d.get("tier"),
    }


_robots: urllib.robotparser.RobotFileParser | None = None


def metacritic_lookup(name: str) -> dict | None:
    """Metacritic(비공식, 공식 API 없음). robots.txt 허용 시에만, 최선 노력으로 메타스코어를 읽는다.
    VERIFY: 이용약관상 허용 여부는 직접 확인할 것. 차단·구조 변경 시 None."""
    global _robots
    slug = re.sub(r"[^a-z0-9]+", "-", norm_name(name)).strip("-")
    if not slug:
        return None
    url = f"https://www.metacritic.com/game/{slug}/"
    if _robots is None:
        _robots = urllib.robotparser.RobotFileParser("https://www.metacritic.com/robots.txt")
        try:
            _robots.read()
        except Exception:
            return None
    if not _robots.can_fetch(UA, url):
        return None
    try:
        html = fetch(url, as_json=False, pause=3)
    except Exception:
        return None
    m = re.search(r'"aggregateRating"\s*:\s*\{[^}]*?"ratingValue"\s*:\s*"?(\d{1,3})', html)
    if not m:
        return None
    return {"slug": slug, "score": float(m.group(1))}


# --------------------------------------------------------------------------- 파이프라인
def run(args) -> list[dict]:
    if args.source == "appids":
        cands = candidates_appids(args.appids_file)
    else:
        cands = candidates_steamspy(args.source, args.pages)

    # 1) SteamSpy 수치로 사전 필터(호출 절약). appids 모드는 수치가 없어 통과.
    pre = []
    for c in cands:
        pos, neg = c.get("positive"), c.get("negative")
        if pos is not None and neg is not None:
            n = pos + neg
            if n < args.min_reviews or (pos / n if n else 0) < args.min_ratio:
                continue
        pre.append(c)
    pre.sort(key=lambda c: wilson_lower_bound(c.get("positive") or 0, c.get("negative") or 0), reverse=True)
    pre = pre[: args.limit * 3]  # 공식 확인에서 탈락할 몫을 감안해 여유를 둔다
    print(f"후보 {len(cands)} → 사전필터 통과 {len(pre)}", file=sys.stderr)

    # 2) 공식 Steam 요약으로 확정 + 최종 필터
    games = []
    for c in pre:
        appid = int(c["appid"])
        try:
            s = steam_summary(appid)
        except Exception as e:
            print(f"  steam {appid} 실패: {e}", file=sys.stderr)
            continue
        if not s or s["total"] < args.min_reviews or s["ratio"] < args.min_ratio:
            continue
        games.append({"appid": appid, "name": c.get("name") or "", "url": STORE_APP_URL.format(appid=appid), "steam": s})
    games.sort(key=lambda g: g["steam"]["wilson"], reverse=True)
    games = games[: args.limit]

    # 3) 평론가 점수
    rapid_key = os.environ.get("RAPIDAPI_KEY")
    if args.opencritic and not rapid_key:
        print("RAPIDAPI_KEY 없음 → OpenCritic 건너뜀", file=sys.stderr)
    for g in games:
        g["opencritic"] = g["metacritic"] = None
        if not g["name"]:
            continue
        if args.opencritic and rapid_key:
            try:
                g["opencritic"] = opencritic_lookup(g["name"], rapid_key)
            except Exception as e:
                print(f"  opencritic {g['name']} 실패: {e}", file=sys.stderr)
        if args.metacritic:
            g["metacritic"] = metacritic_lookup(g["name"])
        if args.sample_reviews:
            g["sample_reviews"] = steam_sample_reviews(g["appid"], args.sample_reviews)

    for g in games:
        merge_scores(g)
    return games


def merge_scores(g: dict) -> None:
    """유저 점수(긍정 %)와 평론가 평균을 만들고 불일치를 표시한다."""
    user = round(g["steam"]["ratio"] * 100, 1)
    critics = [x["score"] for x in (g.get("opencritic"), g.get("metacritic")) if x]
    g["user_score"] = user
    g["critic_score"] = round(sum(critics) / len(critics), 1) if critics else None
    if g["critic_score"] is None:
        g["gap"], g["flag"] = None, "평론가 없음"
    else:
        g["gap"] = round(user - g["critic_score"], 1)
        g["flag"] = ("유저>평론가" if g["gap"] >= GAP_FLAG else
                     "평론가>유저" if g["gap"] <= -GAP_FLAG else "일치")


def write_outputs(games: list[dict], out_dir: Path, args) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    day = dt.date.today().isoformat()
    jf, mf = out_dir / f"steam-critic-{day}.json", out_dir / f"steam-critic-{day}.md"
    slim = [{k: v for k, v in g.items() if k != "sample_reviews"} for g in games]
    jf.write_text(json.dumps({"date": day, "params": {
        "source": args.source, "min_reviews": args.min_reviews, "min_ratio": args.min_ratio,
        "limit": args.limit}, "games": slim}, ensure_ascii=False, indent=2), encoding="utf-8")
    for g in games:
        if g.get("sample_reviews"):
            (out_dir / f"reviews-{g['appid']}.json").write_text(
                json.dumps(g["sample_reviews"], ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# 게임 선별 결과 {day}", "",
             f"- 기준: 리뷰 {args.min_reviews:,}개 이상 · 긍정 {args.min_ratio:.0%} 이상 · 정렬 = Wilson 하한(95%)",
             f"- 출처: Steam GetAppReviews(유저) · OpenCritic/Metacritic(평론가, 있는 것만)", "",
             "| # | 게임 | 유저 긍정% | 리뷰 수 | Wilson | 평론가 | 차이 | 판정 |",
             "|--:|---|--:|--:|--:|--:|--:|---|"]
    for i, g in enumerate(games, 1):
        s = g["steam"]
        lines.append(f"| {i} | [{g['name'] or g['appid']}]({g['url']}) | {g['user_score']} | {s['total']:,} | "
                     f"{s['wilson'] * 100:.1f} | {g['critic_score'] if g['critic_score'] is not None else '–'} | "
                     f"{g['gap'] if g['gap'] is not None else '–'} | {g['flag']} |")
    mf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return jf, mf


# --------------------------------------------------------------------------- 자체 테스트
def self_test() -> None:
    """네트워크 없이 선별·병합·출력 로직을 검증한다."""
    import tempfile

    # 1) Wilson: 같은 긍정 비율이면 리뷰가 많은 쪽이 높아야 한다
    assert wilson_lower_bound(9, 1) < wilson_lower_bound(900, 100)
    assert wilson_lower_bound(0, 0) == 0.0
    assert 0 < wilson_lower_bound(95, 5) < 0.95

    # 2) 모의 응답
    spy = {"1": {"appid": 1, "name": "Alpha Quest", "positive": 9500, "negative": 500},
           "2": {"appid": 2, "name": "Tiny Gem", "positive": 90, "negative": 10},       # 리뷰 수 미달
           "3": {"appid": 3, "name": "Meh Game", "positive": 5000, "negative": 5000},   # 비율 미달
           "4": {"appid": 4, "name": "Beta Saga", "positive": 4000, "negative": 400}}

    def fake_fetch(url, headers=None, as_json=True, **kw):
        if "steamspy.com" in url:
            return spy
        if "GetAppReviews" in url:
            appid = json.loads(urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["input_json"][0])["appid"]
            v = spy[str(appid)]
            return {"response": {"query_summary": {"total_positive": v["positive"], "total_negative": v["negative"],
                                                   "review_score_desc": "Very Positive"}, "reviews": []}}
        if "/game/search" in url:
            name = urllib.parse.unquote(url.split("criteria=")[1])
            return [{"id": 77, "name": name, "dist": 0}] if name == "Alpha Quest" else []
        if "/game/77" in url:
            return {"topCriticScore": 70.0, "percentRecommended": 60, "numReviews": 50, "tier": "Strong"}
        raise AssertionError(url)

    global fetch
    real, fetch = fetch, fake_fetch
    os.environ["RAPIDAPI_KEY"] = "test"
    try:
        args = argparse.Namespace(source="steamspy-top", pages=1, appids_file=None, min_reviews=1000,
                                  min_ratio=0.8, limit=5, opencritic=True, metacritic=False, sample_reviews=0)
        games = run(args)
    finally:
        fetch = real
    assert [g["appid"] for g in games] == [1, 4], games           # 2(리뷰 수)·3(비율) 탈락, 1이 4보다 위
    assert games[0]["critic_score"] == 70.0 and games[0]["flag"] == "유저>평론가", games[0]  # 95 - 70 = 25
    assert games[1]["flag"] == "평론가 없음"
    with tempfile.TemporaryDirectory() as d:
        jf, mf = write_outputs(games, Path(d), args)
        assert json.loads(jf.read_text(encoding="utf-8"))["games"][0]["name"] == "Alpha Quest"
        assert "Alpha Quest" in mf.read_text(encoding="utf-8")
    print("self-test OK (모의 응답 기준 — 실제 API 응답은 별도 확인 필요)")


# --------------------------------------------------------------------------- CLI
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", choices=["steamspy-top", "steamspy-all", "appids"], default="steamspy-top")
    ap.add_argument("--appids-file", help="--source appids 일 때: appid가 적힌 텍스트 파일")
    ap.add_argument("--pages", type=int, default=3, help="steamspy-all 페이지 수(페이지당 약 1000개, 분당 1회)")
    ap.add_argument("--min-reviews", type=int, default=1000)
    ap.add_argument("--min-ratio", type=float, default=0.80, help="긍정 비율 하한(0~1)")
    ap.add_argument("--limit", type=int, default=30, help="최종 선별 게임 수")
    ap.add_argument("--opencritic", action="store_true", help="OpenCritic 조회(RAPIDAPI_KEY 필요)")
    ap.add_argument("--metacritic", action="store_true", help="Metacritic 조회(비공식·약관 직접 확인)")
    ap.add_argument("--sample-reviews", type=int, default=0, help="게임당 추천 리뷰 N개 저장(개인 분석용, 400자 절단)")
    ap.add_argument("--out", default=str(REPO_ROOT / "raw" / "games"))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return
    if args.source == "appids" and not args.appids_file:
        ap.error("--source appids 에는 --appids-file 이 필요합니다")
    games = run(args)
    jf, mf = write_outputs(games, Path(args.out), args)
    print(f"{len(games)}개 게임 저장: {jf}\n요약 표: {mf}")


if __name__ == "__main__":
    main()
