import { streamForward } from "./_proxy.js";
export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  const b = req.body || {};
  const question = String(b.question || "").slice(0, 300);
  if (!question.trim()) return res.status(400).json({ error: "question required" });
  const cat = ["game", "ai-news"].includes(b.category) ? b.category : undefined;
  return streamForward(req, res, "/api/ask", { question, k: 4, stream: true, ...(cat ? { category: cat } : {}) });
}
