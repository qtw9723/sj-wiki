// 하이브리드 검색: BM25(한글 bigram) + 벡터(코사인) → RRF 융합.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { embed, embedConfig } from "./llm.mjs";

// Vercel에서는 cwd가 /var/task, 소스는 /var/task/rag 에 놓이므로 모듈 위치 기준으로 찾는다.
const INDEX_DIR = [
  fileURLToPath(new URL("../index", import.meta.url)),
  path.join(process.cwd(), "index"),
  path.join(process.cwd(), "rag", "index"),
].find((d) => fs.existsSync(path.join(d, "chunks.json"))) || path.join(process.cwd(), "index");
let STATE = null;

export function tokenize(s) {
  const out = [];
  const re = /[a-z0-9]+(?:[._-][a-z0-9]+)*|[가-힣]+|[぀-ヿ一-鿿]+/g;
  for (const m of s.toLowerCase().matchAll(re)) {
    const t = m[0];
    if (/^[a-z0-9]/.test(t)) {
      out.push(t);
      if (/[._-]/.test(t)) for (const p of t.split(/[._-]/)) if (p) out.push(p);
    } else if (t.length === 1) out.push(t);
    else for (let i = 0; i < t.length - 1; i++) out.push(t.slice(i, i + 2));
  }
  return out;
}

export function loadIndex() {
  if (STATE) return STATE;
  const chunks = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, "chunks.json"), "utf8"));
  const meta = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, "meta.json"), "utf8"));
  const inv = new Map();
  const lens = new Array(chunks.length);
  let total = 0;
  chunks.forEach((c, i) => {
    const toks = tokenize(`${c.title} ${c.title} ${c.heading} ${c.text}`);
    lens[i] = toks.length;
    total += toks.length;
    const tf = new Map();
    for (const t of toks) tf.set(t, (tf.get(t) || 0) + 1);
    for (const [t, n] of tf) {
      let a = inv.get(t);
      if (!a) inv.set(t, (a = []));
      a.push([i, n]);
    }
  });
  let vec = null;
  let vmeta = null;
  try {
    vmeta = JSON.parse(fs.readFileSync(path.join(INDEX_DIR, "embedding-meta.json"), "utf8"));
    const buf = fs.readFileSync(path.join(INDEX_DIR, "vectors.bin"));
    const f = new Float32Array(buf.buffer, buf.byteOffset, buf.byteLength / 4);
    if (vmeta.count === chunks.length && f.length === chunks.length * vmeta.dims) vec = f;
  } catch {}
  STATE = { chunks, meta, inv, lens, avg: total / chunks.length, vec, vmeta };
  return STATE;
}

function bm25(S, query, allow) {
  const N = S.chunks.length;
  const scores = new Map();
  const k1 = 1.2, b = 0.75;
  for (const t of new Set(tokenize(query))) {
    const posting = S.inv.get(t);
    if (!posting) continue;
    const idf = Math.log(1 + (N - posting.length + 0.5) / (posting.length + 0.5));
    for (const [i, tf] of posting) {
      if (!allow(i)) continue;
      const s = (idf * tf * (k1 + 1)) / (tf + k1 * (1 - b + (b * S.lens[i]) / S.avg));
      scores.set(i, (scores.get(i) || 0) + s);
    }
  }
  return [...scores].sort((a, b) => b[1] - a[1]);
}

function dense(S, qv, allow) {
  const { dims } = S.vmeta;
  const out = [];
  for (let i = 0; i < S.chunks.length; i++) {
    if (!allow(i)) continue;
    let dot = 0;
    const off = i * dims;
    for (let d = 0; d < dims; d++) dot += S.vec[off + d] * qv[d];
    out.push([i, dot]);
  }
  return out.sort((a, b) => b[1] - a[1]);
}

export function vectorsAvailable() {
  return !!loadIndex().vec && !!embedConfig();
}

export async function search({ q, k = 8, category = null, mode = "hybrid" }) {
  const S = loadIndex();
  const allow = (i) => !category || S.chunks[i].category === category;
  const t0 = Date.now();
  const pool = Math.max(k * 5, 30);

  let lex = [];
  let den = [];
  let used = "lexical";
  if (mode !== "vector") lex = bm25(S, q, allow).slice(0, pool);
  if (mode !== "lexical" && vectorsAvailable()) {
    const [qv] = await embed([q]);
    if (qv && qv.length === S.vmeta.dims) {
      den = dense(S, qv, allow).slice(0, pool);
      used = mode === "vector" ? "vector" : "hybrid";
    }
  }

  const fused = new Map();
  const add = (list, key) =>
    list.forEach(([i, s], r) => {
      const e = fused.get(i) || { i, rrf: 0 };
      e.rrf += 1 / (60 + r + 1);
      e[key] = { rank: r + 1, score: +s.toFixed(4) };
      fused.set(i, e);
    });
  add(lex, "lexical");
  add(den, "vector");

  const results = [...fused.values()]
    .sort((a, b) => b.rrf - a.rrf)
    .slice(0, k)
    .map((e) => {
      const c = S.chunks[e.i];
      return {
        id: c.id, page: c.page, title: c.title, heading: c.heading, category: c.category,
        meta: c.meta, text: c.text, url: c.url,
        score: +e.rrf.toFixed(5), lexical: e.lexical || null, vector: e.vector || null,
      };
    });
  return {
    query: q, mode: used, took_ms: Date.now() - t0, results,
    index: {
      wikiCommit: S.meta.wikiCommit, chunks: S.meta.chunks, pages: S.meta.pages,
      vectors: !!S.vec, embeddingModel: S.vmeta?.model || null,
    },
  };
}
