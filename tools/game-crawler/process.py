#!/usr/bin/env python3
"""2단계(검증·정제) + 3단계(게임 단위 장르 분류) — crawler.py 결과를 받아 정리한다.

입력 : raw/games/steam-critic-YYYY-MM-DD.json  (crawler.py 출력, 기본은 가장 최근 파일)
출력 : raw/games/clean-YYYY-MM-DD.json  (통과 / 탈락+사유 / 미분류 태그 / 경고)
       raw/games/clean-YYYY-MM-DD.md    (사람이 보는 요약. 신규 게임 강조)
       raw/games/state.json             (이미 본 게임 기록 → 매일 돌릴 때 '신규'만 구분)

하는 일
  - Steam 상점 appdetails 로 type 확인 → game 이 아닌 것(DLC·데모·소프트웨어 등) 탈락
  - 긍정 비율을 긍정/부정 수로 다시 계산해 대조, 이름 누락 등 경고
  - Steam 장르 + SteamSpy 태그를 genre_map.json 으로 통제 어휘(gl_genre)에 매핑
  - 매핑표에 없는 태그는 '미분류'로 모아 어휘표에 추가할지 사람이 결정하게 함

하지 않는 일 (설계상 보류)
  - 리뷰 폭탄(최근 리뷰 급변) 탐지: 최근 기간 리뷰를 따로 받아야 해서 아직 없음
  - 요소(메커니즘) 추출: 리뷰를 읽고 판단하는 단계라 대화에서 사람 확인과 함께 한다

사용:  python tools/game-crawler/process.py [--in FILE] [--offline] [--self-test]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import crawler  # noqa: E402  (같은 폴더의 crawler.py: fetch 캐시·재시도 재사용)

REPO_ROOT = HERE.parent.parent
GAMES_DIR = REPO_ROOT / "raw" / "games"
MAP_FILE = HERE / "genre_map.json"
APPDETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={appid}&l=english"  # VERIFY: 비공식, 호출 제한
SPY_DETAILS_URL = "https://steamspy.com/api.php?request=appdetails&appid={appid}"          # VERIFY: 비공식
GAP_TOL = 0.002  # 긍정 비율 재계산 허용 오차


def load_map() -> dict:
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def latest_input() -> Path:
    files = sorted(GAMES_DIR.glob("steam-critic-*.json"))
    if not files:
        raise SystemExit("raw/games/steam-critic-*.json 이 없습니다. 먼저 crawler.py 를 실행하세요.")
    return files[-1]


def enrich(game: dict, offline: bool) -> dict:
    """상점 type·장르, SteamSpy 태그를 붙인다. 실패해도 게임을 버리지 않고 비워 둔다."""
    info = {"type": None, "genres": [], "tags": {}, "is_free": None, "release": None}
    if offline:
        return info
    appid = game["appid"]
    try:
        d = crawler.fetch(APPDETAILS_URL.format(appid=appid), pause=1.5)
        entry = (d.get(str(appid)) or {})
        if entry.get("success"):
            data = entry["data"]
            info["type"] = data.get("type")
            info["genres"] = [g.get("description") for g in data.get("genres", []) if g.get("description")]
            info["is_free"] = data.get("is_free")
            info["release"] = (data.get("release_date") or {}).get("date")
            if not game.get("name"):
                game["name"] = data.get("name", "")
    except Exception as e:
        print(f"  appdetails {appid} 실패: {e}", file=sys.stderr)
    try:
        s = crawler.fetch(SPY_DETAILS_URL.format(appid=appid), pause=1.5)
        tags = s.get("tags")
        if isinstance(tags, dict):
            info["tags"] = tags
    except Exception as e:
        print(f"  steamspy {appid} 실패: {e}", file=sys.stderr)
    return info


def classify(info: dict, gmap: dict, top_tags: int = 12) -> tuple[list[str], dict]:
    """장르·태그 → gl_genre. (매핑된 값 목록, 미분류 태그 {태그: 득표})."""
    found: list[str] = []
    for g in info["genres"]:
        v = gmap["genres"].get(g)
        if v and v not in found:
            found.append(v)
    unmapped = {}
    ranked = sorted(info["tags"].items(), key=lambda kv: kv[1], reverse=True)[:top_tags]
    for tag, votes in ranked:
        if tag in gmap["ignore_tags"]:
            continue
        v = gmap["tags"].get(tag)
        if v:
            if v not in found:
                found.append(v)
        else:
            unmapped[tag] = votes
    return found, unmapped


def validate(game: dict, info: dict, offline: bool) -> tuple[str | None, list[str]]:
    """(탈락 사유 or None, 경고 목록)."""
    warns: list[str] = []
    s = game.get("steam") or {}
    if not s or not s.get("total"):
        return "Steam 요약 없음", warns
    if info["type"] and info["type"] != "game":
        return f"게임이 아님(type={info['type']})", warns
    if not offline and info["type"] is None:
        warns.append("상점 type 확인 실패(통과시키되 확인 필요)")
    recomputed = s["positive"] / s["total"]
    if abs(recomputed - s["ratio"]) > GAP_TOL:
        warns.append(f"긍정 비율 불일치(저장 {s['ratio']} vs 재계산 {recomputed:.4f})")
    if not game.get("name"):
        warns.append("이름 없음 → 평론가 매칭 불가")
    if "Early Access" in info["genres"]:
        warns.append("앞서 해보기(Early Access) — 평가가 변할 수 있음")
    return None, warns


def run(path: Path, offline: bool) -> dict:
    gmap = load_map()
    data = json.loads(path.read_text(encoding="utf-8"))
    state_path = GAMES_DIR / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    today = dt.date.today().isoformat()

    passed, rejected, unmapped_all, seen_ids = [], [], {}, set()
    for g in data["games"]:
        if g["appid"] in seen_ids:
            rejected.append({"appid": g["appid"], "name": g.get("name", ""), "reason": "중복 appid"})
            continue
        seen_ids.add(g["appid"])
        info = enrich(g, offline)
        reason, warns = validate(g, info, offline)
        if reason:
            rejected.append({"appid": g["appid"], "name": g.get("name", ""), "reason": reason})
            continue
        genres, unmapped = classify(info, gmap)
        for t, v in unmapped.items():
            unmapped_all[t] = unmapped_all.get(t, 0) + 1
        g["gl_genre"] = genres
        g["release"] = info["release"]
        g["warnings"] = warns
        g["is_new"] = str(g["appid"]) not in state
        if g["is_new"]:
            state[str(g["appid"])] = {"name": g.get("name", ""), "first_seen": today}
        passed.append(g)

    out = {"date": today, "source_file": path.name, "passed": passed, "rejected": rejected,
           "unmapped_tags": dict(sorted(unmapped_all.items(), key=lambda kv: kv[1], reverse=True))}
    return {"out": out, "state": state}


def write(result: dict) -> tuple[Path, Path]:
    GAMES_DIR.mkdir(parents=True, exist_ok=True)
    out = result["out"]
    day = out["date"]
    jf, mf = GAMES_DIR / f"clean-{day}.json", GAMES_DIR / f"clean-{day}.md"
    jf.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    (GAMES_DIR / "state.json").write_text(json.dumps(result["state"], ensure_ascii=False, indent=2), encoding="utf-8")

    new = [g for g in out["passed"] if g["is_new"]]
    L = [f"# 정제 결과 {day}", "",
         f"- 입력 `{out['source_file']}` → 통과 {len(out['passed'])} · 탈락 {len(out['rejected'])} · **신규 {len(new)}**", ""]
    L += ["## 통과", "", "| # | 게임 | 신규 | 장르(gl_genre) | 유저% | 리뷰 수 | 평론가 | 판정 | 경고 |",
          "|--:|---|:-:|---|--:|--:|--:|---|---|"]
    for i, g in enumerate(out["passed"], 1):
        L.append(f"| {i} | [{g.get('name') or g['appid']}]({g['url']}) | {'🆕' if g['is_new'] else ''} | "
                 f"{', '.join(g['gl_genre']) or '–'} | {g['user_score']} | {g['steam']['total']:,} | "
                 f"{g['critic_score'] if g['critic_score'] is not None else '–'} | {g['flag']} | {'; '.join(g['warnings']) or ''} |")
    if out["rejected"]:
        L += ["", "## 탈락 (사유)", ""] + [f"- {r['name'] or r['appid']} — {r['reason']}" for r in out["rejected"]]
    if out["unmapped_tags"]:
        L += ["", "## 미분류 태그 (어휘표에 추가할지 결정)", "",
              "`genre_map.json`에 매핑을 넣거나 `ignore_tags`에 넣으면 다음 실행부터 반영된다.", ""]
        L += [f"- {t} ({n}개 게임)" for t, n in list(out["unmapped_tags"].items())[:30]]
    mf.write_text("\n".join(L) + "\n", encoding="utf-8")
    return jf, mf


def self_test() -> None:
    import tempfile
    global GAMES_DIR
    gmap = load_map()
    # 매핑: 장르 + 태그, 미분류, 무시 태그
    info = {"genres": ["Action", "Indie"], "tags": {"Roguelike": 900, "Pixel Graphics": 800, "Weird Tag": 700, "Singleplayer": 600}}
    genres, unmapped = classify(info, gmap)
    assert genres == ["액션", "로그라이크"], genres
    assert unmapped == {"Weird Tag": 700}, unmapped

    with tempfile.TemporaryDirectory() as d:
        GAMES_DIR = Path(d)
        base = {"steam": {"positive": 950, "negative": 50, "total": 1000, "ratio": 0.95, "wilson": 0.93},
                "user_score": 95.0, "critic_score": None, "gap": None, "flag": "평론가 없음"}
        games = [dict(base, appid=1, name="Alpha", url="u1"),
                 dict(base, appid=2, name="Alpha DLC", url="u2"),
                 dict(base, appid=1, name="Alpha", url="u1"),                                  # 중복
                 dict(base, appid=3, name="", url="u3", steam=dict(base["steam"], ratio=0.5))]  # 이름 없음 + 비율 불일치
        (GAMES_DIR / "steam-critic-2026-10-23.json").write_text(json.dumps({"games": games}), encoding="utf-8")

        def fake_fetch(url, headers=None, as_json=True, **kw):
            if "store.steampowered.com/api/appdetails" in url:
                appid = url.split("appids=")[1].split("&")[0]
                typ = "dlc" if appid == "2" else "game"
                return {appid: {"success": True, "data": {"type": typ, "name": f"n{appid}", "is_free": False,
                                                          "genres": [{"description": "Action"}], "release_date": {"date": "1 Jan, 2024"}}}}
            if "steamspy.com" in url:
                return {"tags": {"Roguelike": 100, "Weird Tag": 50}}
            raise AssertionError(url)

        real, crawler.fetch = crawler.fetch, fake_fetch
        try:
            res = run(latest_input(), offline=False)
            jf, mf = write(res)
            res2 = run(latest_input(), offline=False)  # 두 번째 실행: 신규 없음이어야 함
        finally:
            crawler.fetch = real
        out = res["out"]
        assert [g["appid"] for g in out["passed"]] == [1, 3], out["passed"]
        assert {r["reason"].split("(")[0] for r in out["rejected"]} == {"게임이 아님", "중복 appid"}, out["rejected"]
        assert all(g["is_new"] for g in out["passed"])
        assert not any(g["is_new"] for g in res2["out"]["passed"])
        g3 = [g for g in out["passed"] if g["appid"] == 3][0]
        assert any("비율 불일치" in w for w in g3["warnings"]) and g3["name"] == "n3", g3  # 이름은 상점에서 보충
        assert out["unmapped_tags"] == {"Weird Tag": 2}, out["unmapped_tags"]
        assert "신규 2" in mf.read_text(encoding="utf-8")
    print("process self-test OK (모의 응답 기준)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="infile", help="crawler.py 출력 JSON (기본: raw/games 의 가장 최근 steam-critic-*.json)")
    ap.add_argument("--offline", action="store_true", help="상점·SteamSpy 조회 없이 검증만")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        self_test()
        return
    path = Path(a.infile) if a.infile else latest_input()
    res = run(path, a.offline)
    jf, mf = write(res)
    o = res["out"]
    print(f"통과 {len(o['passed'])} · 탈락 {len(o['rejected'])} · 신규 {sum(g['is_new'] for g in o['passed'])}\n{mf}")


if __name__ == "__main__":
    main()
