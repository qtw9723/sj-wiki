// 로컬 개발 서버: Vercel 없이 public/ + api/*.mjs 를 그대로 띄운다. (npm run dev → http://localhost:3000)
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
process.chdir(ROOT);
const PORT = +(process.env.PORT || 3000);
const MIME = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".json": "application/json", ".css": "text/css" };

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname.startsWith("/api/")) {
    const name = url.pathname.slice(5).replace(/[^a-z0-9-]/gi, "");
    const file = path.join(ROOT, "api", `${name}.mjs`);
    if (!fs.existsSync(file)) { res.statusCode = 404; return res.end("not found"); }
    const mod = await import(pathToFileURL(file).href);
    return mod.default(req, res);
  }
  const f = path.join(ROOT, "public", url.pathname === "/" ? "index.html" : url.pathname);
  if (!f.startsWith(path.join(ROOT, "public")) || !fs.existsSync(f)) { res.statusCode = 404; return res.end("not found"); }
  res.setHeader("content-type", MIME[path.extname(f)] || "application/octet-stream");
  res.end(fs.readFileSync(f));
}).listen(PORT, () => console.log(`http://localhost:${PORT}`));
