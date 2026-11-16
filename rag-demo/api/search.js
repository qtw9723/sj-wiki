import { forward } from "./_proxy.js";
export default async function handler(req, res) {
  const q = String(req.query.q || "").slice(0, 200);
  if (!q.trim()) return res.status(400).json({ error: "q required" });
  const k = Math.min(Math.max(parseInt(req.query.k) || 20, 1), 30);
  const cat = ["game", "ai-news"].includes(req.query.category) ? req.query.category : "";
  const qs = new URLSearchParams({ q, k: String(k), mode: "hybrid", ...(cat ? { category: cat } : {}) });
  return forward(req, res, "/api/search?" + qs);
}
