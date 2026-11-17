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

// 스트리밍 패스스루: 업스트림이 JSON 오류를 주면 그대로, NDJSON이면 조각마다 즉시 흘려보낸다.
export async function streamForward(req, res, path, body) {
  const key = process.env.RAG_DEMO_KEY;
  if (!key) return res.status(503).json({ error: "not_configured" });
  try {
    const r = await fetch(UPSTREAM + path, {
      method: "POST",
      headers: { "x-api-key": key, "content-type": "application/json" },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(Number(process.env.RAG_PROXY_TIMEOUT_MS) || 55000),
    });
    const ct = r.headers.get("content-type") || "application/json";
    res.status(r.status);
    res.setHeader("content-type", ct);
    res.setHeader("cache-control", "no-store, no-transform");
    if (!ct.includes("ndjson")) return res.send(await r.text());
    for await (const chunk of r.body) res.write(chunk);
    return res.end();
  } catch (e) {
    const timeout = e && (e.name === "TimeoutError" || e.name === "AbortError");
    const err = { error: timeout ? "upstream_timeout" : "upstream_unreachable" };
    if (res.headersSent) { res.write(JSON.stringify({ type: "error", ...err }) + "\n"); return res.end(); }
    return res.status(timeout ? 504 : 502).json(err);
  }
}
