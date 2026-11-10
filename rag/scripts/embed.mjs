// 청크 임베딩 생성(무료 OpenAI 호환 임베딩 API). Vercel 빌드(vercel-build) 또는 로컬에서 실행.
// 설정이 없거나 실패하면 벡터 없이(=BM25 전용) 계속 진행한다 — 배포를 막지 않는다.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { embed, embedConfig } from "../lib/llm.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIR = path.join(ROOT, "index");
const VEC = path.join(DIR, "vectors.bin");
const META = path.join(DIR, "embedding-meta.json");

const cfg = embedConfig();
if (!cfg) {
  console.log("[embed] EMBED_MODEL(및 키) 미설정 → 벡터 생략, BM25 전용으로 배포");
  process.exit(0);
}

const chunks = JSON.parse(fs.readFileSync(path.join(DIR, "chunks.json"), "utf8"));
const hash = crypto.createHash("sha256").update(JSON.stringify(chunks.map((c) => c.id + c.text)) + cfg.model).digest("hex").slice(0, 16);
if (fs.existsSync(META) && fs.existsSync(VEC)) {
  const m = JSON.parse(fs.readFileSync(META, "utf8"));
  if (m.hash === hash) { console.log("[embed] 기존 벡터 재사용"); process.exit(0); }
}

const BATCH = +(process.env.EMBED_BATCH || 32);
const DELAY = +(process.env.EMBED_DELAY_MS || 0);
const input = (c) => `${c.title}\n${c.heading}\n${c.text}`.slice(0, 2000);
let dims = 0, out = null;
try {
  for (let i = 0; i < chunks.length; i += BATCH) {
    const vs = await embed(chunks.slice(i, i + BATCH).map(input));
    if (!out) { dims = vs[0].length; out = new Float32Array(chunks.length * dims); }
    vs.forEach((v, j) => out.set(v, (i + j) * dims));
    if ((i / BATCH) % 10 === 0) console.log(`[embed] ${Math.min(i + BATCH, chunks.length)}/${chunks.length}`);
    if (DELAY) await new Promise((r) => setTimeout(r, DELAY));
  }
  fs.writeFileSync(VEC, Buffer.from(out.buffer));
  fs.writeFileSync(META, JSON.stringify({ model: cfg.model, dims, count: chunks.length, hash, builtAt: new Date().toISOString() }, null, 2));
  console.log(`[embed] 완료: ${chunks.length}개 × ${dims}차원 (${cfg.model})`);
} catch (e) {
  console.error("[embed] 실패 → 벡터 없이 진행:", String(e.message).slice(0, 300));
  for (const f of [VEC, META]) fs.rmSync(f, { force: true });
}
process.exit(0);
