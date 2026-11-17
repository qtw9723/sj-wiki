// 데모용 프록시: 키는 서버 환경변수(RAG_DEMO_KEY)에만 존재. 브라우저·레포에는 없다.
const UPSTREAM = process.env.RAG_API_BASE || "https://sj-wiki-rag.vercel.app";
export async function forward(req, res, path, body) {
  const key = process.env.RAG_DEMO_KEY;
  if (!key) return res.status(503).json({ error: "not_configured" });
  try {
    const r = await fetch(UPSTREAM + path, {
      method: body ? "POST" : "GET",
      headers: { "x-api-key": key, ...(body ? { "content-type": "application/json" } : {}) },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(Number(process.env.RAG_PROXY_TIMEOUT_MS) || 50000),
    });
    const text = await r.text();
    res.status(r.status).setHeader("content-type", "application/json").send(text);
  } catch (e) {
    const timeout = e && (e.name === "TimeoutError" || e.name === "AbortError");
    res.status(timeout ? 504 : 502).json({ error: timeout ? "upstream_timeout" : "upstream_unreachable" });
  }
}
