#!/usr/bin/env python3
"""매일 아침 실행용 래퍼: crawler.py(수집) → process.py(정제·분류) 를 차례로 실행한다.

    python tools/game-crawler/run_daily.py                       # 수집 + 정제
    python tools/game-crawler/run_daily.py --opencritic --limit 30
    python tools/game-crawler/run_daily.py --push                # 끝나면 raw/games 만 커밋·푸시(기본 꺼짐)

한 단계가 실패하면 즉시 멈추고 0이 아닌 코드로 끝난다(예약 작업이 실패를 알 수 있게).
"""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=REPO, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="steamspy-top")
    ap.add_argument("--limit", default="30")
    ap.add_argument("--min-reviews", default="1000")
    ap.add_argument("--min-ratio", default="0.80")
    ap.add_argument("--opencritic", action="store_true")
    ap.add_argument("--metacritic", action="store_true")
    ap.add_argument("--push", action="store_true", help="raw/games 변경분을 pull --rebase 후 커밋·푸시")
    a = ap.parse_args()

    py = sys.executable
    crawl = [py, str(HERE / "crawler.py"), "--source", a.source, "--limit", a.limit,
             "--min-reviews", a.min_reviews, "--min-ratio", a.min_ratio]
    if a.opencritic:
        crawl.append("--opencritic")
    if a.metacritic:
        crawl.append("--metacritic")
    try:
        run(crawl)
        run([py, str(HERE / "process.py")])
        if a.push:
            day = dt.date.today().isoformat()
            run(["git", "pull", "--rebase", "--autostash", "origin", "main"])
            run(["git", "add", "raw/games"])
            staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPO).returncode
            if staged:  # 1 = 변경 있음
                run(["git", "commit", "-m", f"data(games): {day} 일일 수집·정제"])
                run(["git", "push", "origin", "HEAD:main"])
            else:
                print("변경 없음 — 커밋 생략")
    except subprocess.CalledProcessError as e:
        print(f"실패: {e}", file=sys.stderr)
        return e.returncode or 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
