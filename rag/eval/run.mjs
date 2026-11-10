// 검색 품질 평가: 페이지 단위 hit@1/3/5, MRR. 모드별(lexical/vector/hybrid) 비교.
// 사용: node eval/run.mjs            (로컬 인덱스, 벡터는 임베딩 환경변수가 있을 때만)
//       EVAL_BASE_URL=https://배포주소 node eval/run.mjs   (배포된 API 대상)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
process.chdir(ROOT);
const Q = JSON.parse(fs.readFileSync("eval/questions.json", "utf8"));
const chunks = JSON.parse(fs.readFileSync("index/chunks.json", "utf8"));
const BASE = process.env.EVAL_BASE_URL;

// 정답 페이지 결정: game은 명시, ai-news는 anchor 문자열이 실제로 들어있는 페이지(정확 일치)
const pagesOf = new Set(chunks.map((c) => c.page));
for (const q of Q) {
  if (q.anchor) q.expect = [...new Set(chunks.filter((c) => c.category === "ai-news" && c.text.includes(q.anchor)).map((c) => c.page))];
  q.expect = (q.expect || []).filter((p) => pagesOf.has(p));
  if (!q.expect.length) console.warn(`⚠ ${q.id}: 정답 페이지를 코퍼스에서 못 찾아 제외`);
}
const questions = Q.filter((q) => q.expect.length);
// 앵커가 너무 흔한 질문(정답 페이지가 절반 이상)은 변별력이 없어 제외
const usable = questions.filter((q) => q.expect.length <= 8);

let doSearch;
let vectorOk = false;
if (BASE) {
  doSearch = async (q, mode) => (await fetch(`${BASE}/api/search?` + new URLSearchParams({ q, k: 20, mode }))).json();
  const h = await (await fetch(`${BASE}/api/health`)).json();
  vectorOk = !!h.vectorSearchActive;
} else {
  const { search, vectorsAvailable } = await import("../lib/search.mjs");
  doSearch = (q, mode) => search({ q, k: 20, mode });
  vectorOk = vectorsAvailable();
}

const modes = vectorOk ? ["lexical", "vector", "hybrid"] : ["lexical"];
const report = {};
for (const mode of modes) {
  const rows = [];
  for (const q of usable) {
    const r = await doSearch(q.q, mode);
    const pages = [];
    for (const x of r.results) if (!pages.includes(x.page)) pages.push(x.page);
    const rank = pages.findIndex((p) => q.expect.includes(p)) + 1;
    rows.push({ id: q.id, cat: q.cat, hard: !!q.hard, rank });
  }
  const agg = (rs) => ({
    n: rs.length,
    "hit@1": +(rs.filter((x) => x.rank === 1).length / rs.length).toFixed(3),
    "hit@3": +(rs.filter((x) => x.rank >= 1 && x.rank <= 3).length / rs.length).toFixed(3),
    "hit@5": +(rs.filter((x) => x.rank >= 1 && x.rank <= 5).length / rs.length).toFixed(3),
    MRR: +(rs.reduce((s, x) => s + (x.rank ? 1 / x.rank : 0), 0) / rs.length).toFixed(3),
  });
  report[mode] = { all: agg(rows), game: agg(rows.filter((x) => x.cat === "game" && !x.hard)), "hard(영어·동의어 질의)": agg(rows.filter((x) => x.hard)), "ai-news": agg(rows.filter((x) => x.cat === "ai-news")), misses: rows.filter((x) => !x.rank || x.rank > 5).map((x) => `${x.id}:${x.rank || "-"}`) };
}
console.log(JSON.stringify({ questions: usable.length, wikiCommit: JSON.parse(fs.readFileSync("index/meta.json", "utf8")).wikiCommit, vectorEvaluated: vectorOk, report }, null, 2));
if (!vectorOk) console.log("\n(벡터 모드는 임베딩 설정이 없어 생략됨 — EMBED_* 환경변수 또는 EVAL_BASE_URL 사용)");
if (!process.env.EVAL_NO_SAVE) fs.mkdirSync("eval/results", { recursive: true });
if (!process.env.EVAL_NO_SAVE) fs.writeFileSync(`eval/results/${BASE ? "remote" : "local"}-${new Date().toISOString().slice(0, 10)}.json`, JSON.stringify({ report }, null, 2));
