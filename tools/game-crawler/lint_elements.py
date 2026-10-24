#!/usr/bin/env python3
"""Lint wiki/게임요소-*.md pages against the hub convention (wiki/게임요소-라이브러리.md).

Checks: file name pattern, required frontmatter, controlled vocabulary, counts,
broken [[links]] in gl_* fields and body, required template sections, per-type sections.
stdlib only. Exit code 1 if any ERROR. Usage: python tools/game-crawler/lint_elements.py [--root .]
"""
import argparse
import re
import sys
from pathlib import Path

TYPES = ["기획", "시스템", "메커니즘", "수치", "레벨", "디자인", "코드", "사례", "조합"]
DOMAIN = "전투 이동 성장 경제 수집 탐험 퍼즐 생존 건설 소셜 내러티브 리텐션 수익화 온보딩".split()
EXPERIENCE = "감각 판타지 서사 도전 교감 발견 표현 소일".split()
GENRE = "액션 RPG 로그라이크 메트로배니아 퍼즐 시뮬레이션 전략 방치 플랫포머 슈팅 리듬 카드 샌드박스".split()
STATUS = ["수집", "정리", "검증", "폐기"]
REQUIRED = ["title", "category", "gl_type", "gl_domain", "gl_experience", "gl_status",
            "tags", "source", "created", "updated"]
BASE_SECTIONS = ["핵심 규칙", "왜 재밌나", "출처 게임별 변형", "조합 궁합", "구현 메모", "관련 문서"]
EXTRA = {
    "수치": ["공식·표", "조정 손잡이"], "레벨": ["구조도", "난이도·페이싱 흐름"],
    "디자인": ["레퍼런스 화면", "피드백 타이밍"], "코드": ["인터페이스", "코드", "테스트 방법"],
    "기획": ["코어 루프", "목표 플레이어"], "사례": ["이 게임에서 뽑은 요소", "한 줄 평"],
    "조합": ["재료 요소", "가설(왜 재밌을까)", "실험 결과·회고", "토큰 실측"],
}
# 사례 pages are a per-game hub: they do not need the generic element sections.
SKIP_BASE = {"사례"}
LINK = re.compile(r"\[\[([^\]|#]+)")


def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if mm:
            fm[mm.group(1)] = mm.group(2).split("#")[0].strip() if not mm.group(2).startswith(("[", '"')) else mm.group(2).strip()
    return fm, text[m.end():]


def as_list(v):
    v = v.strip()
    if v.startswith("["):
        v = v[1:v.rfind("]")]
    return [x.strip().strip('"').strip("'") for x in v.split(",") if x.strip()]


def lint(root):
    wiki = Path(root) / "wiki"
    pages = sorted(wiki.glob("게임요소-*.md"))
    names = {p.stem for p in wiki.glob("*.md")}
    errs, warns = [], []
    for p in pages:
        if p.stem == "게임요소-라이브러리":
            continue
        t = p.read_text(encoding="utf-8")
        fm, body = parse(t)
        e = lambda m: errs.append(f"{p.name}: {m}")
        w = lambda m: warns.append(f"{p.name}: {m}")
        mm = re.match(r"^게임요소-(.+?)-(.+)$", p.stem)
        if not mm or mm.group(1) not in TYPES:
            e("파일명이 `게임요소-<유형>-<이름>` 규칙이 아님")
        if fm is None:
            e("frontmatter 없음")
            continue
        for k in REQUIRED:
            if k not in fm or not fm[k]:
                e(f"필수 속성 누락: {k}")
        if mm and fm.get("gl_type") and fm["gl_type"] != mm.group(1):
            e(f"gl_type({fm['gl_type']})과 파일명 유형({mm.group(1)}) 불일치")
        if fm.get("gl_type") and fm["gl_type"] not in TYPES:
            e(f"gl_type 어휘 밖: {fm['gl_type']}")
        if fm.get("gl_status") and fm["gl_status"] not in STATUS:
            e(f"gl_status 어휘 밖: {fm['gl_status']}")
        for key, vocab, mx in (("gl_domain", DOMAIN, 3), ("gl_experience", EXPERIENCE, 3), ("gl_genre", GENRE, 99)):
            if key in fm:
                vals = as_list(fm[key])
                bad = [v for v in vals if v not in vocab]
                if bad:
                    e(f"{key} 어휘 밖 값: {bad}")
                if not 1 <= len(vals) <= mx and key != "gl_genre":
                    e(f"{key} 개수 1~{mx} 위반({len(vals)})")
        for k, v in fm.items():
            if k.startswith("gl_") and k in ("gl_games", "gl_parent", "gl_requires", "gl_synergy", "gl_conflict"):
                for l in LINK.findall(v):
                    if l.strip() not in names:
                        e(f"{k} 끊긴 링크: [[{l}]]")
        for l in set(LINK.findall(body)):
            if l.strip() not in names and not l.strip().endswith((".png", ".jpg", ".base")):
                w(f"본문 끊긴 링크(작성 후보): [[{l}]]")
        if "> [!tip] 핵심 takeaway" not in body:
            e("맨 앞 callout `[!tip] 핵심 takeaway` 없음")
        heads = {h.strip() for h in re.findall(r"^##\s+(.+)$", body, re.M)}
        gt = fm.get("gl_type")
        need = ([] if gt in SKIP_BASE else BASE_SECTIONS) + EXTRA.get(gt, [])
        # gl_status 수집 pages may be memo-level: missing sections are warnings only.
        for s in need:
            if not any(h.startswith(s) for h in heads):
                (w if fm.get("gl_status") == "수집" else e)(f"필수 섹션 누락: ## {s}")
        if gt != "사례" and "gl_games" not in fm:
            w("gl_games 비어 있음(사례 없는 요소)")
        if "📄" not in body and "🧠" not in body:
            w("📄/🧠 출처 표기가 없음")
    return pages, errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    pages, errs, warns = lint(a.root)
    n = len([p for p in pages if p.stem != "게임요소-라이브러리"])
    print(f"요소 페이지 {n}개 검사 — 오류 {len(errs)} · 경고 {len(warns)}")
    for x in errs:
        print("ERROR", x)
    for x in warns:
        print("WARN ", x)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
