// 공용 HTTP 유틸: CORS, 토큰 검사, 간이 레이트리밋(인스턴스 단위, best-effort).
const hits = new Map();

export function cors(res) {
  res.setHeader("access-control-allow-origin", "*");
  res.setHeader("access-control-allow-headers", "content-type, authorization, x-api-key");
  res.setHeader("access-control-allow-methods", "GET, POST, OPTIONS");
}

export function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.end(JSON.stringify(body));
}

export function ip(req) {
  return String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "?").split(",")[0].trim();
}

export function rateLimit(req, bucket, max, windowMs = 60000) {
  const key = `${bucket}:${ip(req)}`;
  const now = Date.now();
  const arr = (hits.get(key) || []).filter((t) => now - t < windowMs);
  arr.push(now);
  hits.set(key, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length <= max;
}

// RAG_API_TOKEN이 설정돼 있으면 Authorization: Bearer / x-api-key 필요.
export function tokenOk(req) {
  const want = process.env.RAG_API_TOKEN;
  if (!want) return true;
  const got = (req.headers["x-api-key"] || String(req.headers.authorization || "").replace(/^Bearer\s+/i, "")).toString();
  return got === want;
}

export async function body(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString() || "{}"); } catch { return {}; }
}
