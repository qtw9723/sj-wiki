#!/usr/bin/env python3
"""raw/ 변경 감지 보조 — '본문 내용' 기준 (graphify cache.py 아이디어 차용).

mtime만 보면 frontmatter 수정·touch·git checkout만으로도 재위키화가 돌아 토큰이 샌다.
이 스크립트는 .md의 YAML frontmatter를 뺀 본문(그 외 파일은 전체 바이트)의 sha256을
.raw_hashes(기기 종속, gitignore)에 저장해 두고, 실제로 본문이 바뀐 파일만 골라낸다.

사용법 (파일 목록은 stdin, 한 줄에 하나):
  raw_hash.py filter   # 본문이 바뀌었거나 처음 보는 파일만 stdout으로
  raw_hash.py update   # 해당 파일들의 현재 해시를 저장(위키화·push 성공 후 호출)
  raw_hash.py seed     # 저장소가 비었을 때 기준선 생성(현재 상태를 '처리됨'으로 기록)
"""
import hashlib
import os
import re
import sys

STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".raw_hashes")
FM = re.compile(rb"\A---\r?\n.*?\r?\n---\r?\n", re.S)


def body_hash(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    if path.lower().endswith((".md", ".markdown")):
        data = FM.sub(b"", data, count=1)
    return hashlib.sha256(data).hexdigest()


def load() -> dict:
    store = {}
    if os.path.exists(STORE):
        with open(STORE, encoding="utf-8") as f:
            for line in f:
                p, _, h = line.rstrip("\n").rpartition("\t")
                if p:
                    store[p] = h
    return store


def save(store: dict) -> None:
    tmp = STORE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for p in sorted(store):
            f.write(f"{p}\t{store[p]}\n")
    os.replace(tmp, STORE)


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    files = [l.strip() for l in sys.stdin if l.strip()]
    store = load()
    if cmd == "filter":
        for p in files:
            if not os.path.isfile(p):
                continue
            if store.get(p) != body_hash(p):
                print(p)
    elif cmd in ("update", "seed"):
        for p in files:
            if os.path.isfile(p):
                store[p] = body_hash(p)
        save(store)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
