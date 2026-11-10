// 위키 → RAG 코퍼스(청크) 빌더.
// 대상: 게임 요소 라이브러리(게임요소-*, 게임-*) + AI 주간 소식(AI-주간-소식-*)
// 출력: index/chunks.json, index/meta.json  (특정 위키 커밋에 고정된 스냅샷)
import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REPO = path.resolve(ROOT, "..");
const WIKI = path.join(REPO, "wiki");
const OUT = path.join(ROOT, "index");
const MAX_CHARS = 900; // 청크 최대 길이(한글 기준)
const MIN_CHARS = 60;
const GH = "https://github.com/qtw9723/sj-wiki";

const CORPUS = [
  { category: "game", test: (n) => n.startsWith("게임요소-") || n.startsWith("게임-") },
  { category: "ai-news", test: (n) => n.startsWith("AI-주간-소식-") },
];

const sha = (() => {
  try { return execSync("git rev-parse HEAD", { cwd: REPO }).toString().trim(); } catch { return "unknown"; }
})();

function parseFrontmatter(raw) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) return { fm: {}, body: raw };
  const fm = {};
  for (const line of m[1].split("\n")) {
    const kv = line.match(/^([A-Za-z_]+):\s*(.*)$/);
    if (!kv) continue;
    let v = kv[2].trim();
    if (v.startsWith("[") && v.endsWith("]")) v = v.slice(1, -1).split(",").map((s) => s.trim()).filter(Boolean);
    fm[kv[1]] = v;
  }
  return { fm, body: raw.slice(m[0].length) };
}

// [[링크|표시]] → 표시, [[링크]] → 링크, 콜아웃/굵게 등 마크업 정리
function clean(text) {
  return text
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, "$2")
    .replace(/\[\[([^\]]+)\]\]/g, "$1")
    .replace(/^>\s*\[!\w+\][^\n]*\n?/gm, "")
    .replace(/^>\s?/gm, "")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/[ \t]+/g, " ")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

// 헤딩 경로를 유지한 채 섹션 단위로 나눈 뒤, 길면 문단/문장 경계에서 다시 자른다.
function sections(body) {
  const lines = body.split("\n");
  const out = [];
  let stack = [];
  let buf = [];
  const flush = () => {
    const text = clean(buf.join("\n"));
    if (text.length >= MIN_CHARS) out.push({ heading: stack.filter(Boolean).join(" > "), text });
    buf = [];
  };
  for (const line of lines) {
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      flush();
      const level = h[1].length;
      stack = stack.slice(0, level - 1);
      stack[level - 1] = clean(h[2]).slice(0, 80);
    } else buf.push(line);
  }
  flush();
  return out;
}

function split(text) {
  if (text.length <= MAX_CHARS) return [text];
  const units = text.split(/\n(?=[-*•\d])|\n\n|(?<=[.!?。다요음함])\s+(?=[가-힣A-Z0-9\[(])/).map((s) => s.trim()).filter(Boolean);
  const chunks = [];
  let cur = "";
  for (const u of units) {
    if (u.length > MAX_CHARS) {
      if (cur) { chunks.push(cur); cur = ""; }
      for (let i = 0; i < u.length; i += MAX_CHARS) chunks.push(u.slice(i, i + MAX_CHARS));
      continue;
    }
    if ((cur + "\n" + u).length > MAX_CHARS && cur) { chunks.push(cur); cur = u; }
    else cur = cur ? cur + "\n" + u : u;
  }
  if (cur) chunks.push(cur);
  return chunks.filter((c) => c.length >= MIN_CHARS);
}

fs.mkdirSync(OUT, { recursive: true });
const files = fs.readdirSync(WIKI).filter((f) => f.endsWith(".md")).sort();
const chunks = [];
const pages = {};

for (const file of files) {
  const name = file.replace(/\.md$/, "");
  const rule = CORPUS.find((c) => c.test(name));
  if (!rule) continue;
  const raw = fs.readFileSync(path.join(WIKI, file), "utf8");
  const { fm, body } = parseFrontmatter(raw);
  const title = (fm.title || name).replace(/^["']|["']$/g, "");
  let n = 0;
  for (const sec of sections(body)) {
    for (const piece of split(sec.text)) {
      chunks.push({
        id: `${name}#${n++}`,
        page: name,
        title,
        heading: sec.heading,
        category: rule.category,
        meta: rule.category === "game"
          ? { type: fm.gl_type || null, domain: fm.gl_domain || null, genre: fm.gl_genre || null }
          : { period: fm.period || null },
        text: piece,
        url: `${GH}/blob/${sha}/wiki/${encodeURIComponent(file)}`,
      });
    }
  }
  pages[name] = { category: rule.category, chunks: n };
}

fs.writeFileSync(path.join(OUT, "chunks.json"), JSON.stringify(chunks));
const meta = {
  wikiCommit: sha,
  builtAt: new Date().toISOString(),
  chunkMaxChars: MAX_CHARS,
  pages: Object.keys(pages).length,
  chunks: chunks.length,
  byCategory: Object.fromEntries(
    ["game", "ai-news"].map((c) => [c, { pages: Object.values(pages).filter((p) => p.category === c).length, chunks: chunks.filter((x) => x.category === c).length }])
  ),
};
fs.writeFileSync(path.join(OUT, "meta.json"), JSON.stringify(meta, null, 2));
console.log(JSON.stringify(meta, null, 2));
