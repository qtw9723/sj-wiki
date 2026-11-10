// GET /api/search?q=...&k=8&category=game|ai-news&mode=hybrid|lexical|vector
import { search } from "../lib/search.mjs";
import { cors, json, rateLimit, body } from "../lib/http.mjs";

export default async function handler(req, res) {
  cors(res);
  if (req.method === "OPTIONS") return res.end();
  const params = req.method === "POST" ? await body(req) : Object.fromEntries(new URL(req.url, "http://x").searchParams);
  const q = String(params.q || "").trim();
  if (!q) return json(res, 400, { error: "q(검색어)가 필요해요" });
  if (q.length > 300) return json(res, 400, { error: "q는 300자 이하" });
  if (!rateLimit(req, "search", 30)) return json(res, 429, { error: "요청이 너무 많아요. 잠시 후 다시 시도하세요" });
  const k = Math.min(Math.max(parseInt(params.k) || 8, 1), 20);
  const category = ["game", "ai-news"].includes(params.category) ? params.category : null;
  const mode = ["hybrid", "lexical", "vector"].includes(params.mode) ? params.mode : "hybrid";
  try {
    return json(res, 200, await search({ q, k, category, mode }));
  } catch (e) {
    return json(res, 500, { error: "search failed", detail: String(e.message).slice(0, 200) });
  }
}
