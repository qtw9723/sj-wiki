// 공용 HTTP 유틸: CORS, API 키 검사(fail-closed), 간이 레이트리밋(인스턴스 단위, best-effort).
import crypto from "node:crypto";

const hits = new Map();

export function cors(res) {
  res.setHeader("access-control-allow-origin", "*");
  res.setHeader("access-control-allow-headers", "content-type, authorization, x-api-key");
  res.setHeader("access-control-allow-methods", "GET, POST, OPTIONS");
  res.setHeader("cache-control", "no-store");
}

export function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("content-type", "application/json; charset=utf-8");
  res.end(JSON.stringify(body));
}

export function ip(req) {
  return String(req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "?").split(",")[0].trim();
}

export function rateLimit(req, bucket, max, windowMs = 60000, who = null) {
  const key = `${bucket}:${who || ip(req)}`;
  const now = Date.now();
  const arr = (hits.get(key) || []).filter((t) => now - t < windowMs);
  arr.push(now);
  hits.set(key, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length <= max;
}

// 허용 키: RAG_API_KEYS(쉼표 구분, 여러 개 발급 가능) 또는 RAG_API_TOKEN.
function allowedKeys() {
  return [process.env.RAG_API_KEYS, process.env.RAG_API_TOKEN]
    .filter(Boolean)
    .flatMap((s) => s.split(","))
    .map((s) => s.trim())
    .filter((s) => s.length >= 16);
}

function sha(s) {
  return crypto.createHash("sha256").update(s).digest();
}

// 키는 헤더로만 받는다(URL 쿼리는 로그에 남으므로 불허).
// 반환: { ok, status, error, id } — 키가 하나도 설정되지 않았으면 모두 거부(fail-closed).
export function authenticate(req) {
  const keys = allowedKeys();
  if (!keys.length) return { ok: false, status: 503, error: "API 키가 서버에 설정되지 않았어요(RAG_API_KEYS)" };
  const got = String(req.headers["x-api-key"] || String(req.headers.authorization || "").replace(/^Bearer\s+/i, "")).trim();
  if (!got) return { ok: false, status: 401, error: "API 키가 필요해요: Authorization: Bearer <키> 또는 x-api-key 헤더" };
  const gh = sha(got);
  let match = -1;
  keys.forEach((k, i) => { if (crypto.timingSafeEqual(gh, sha(k))) match = i; });
  if (match < 0) return { ok: false, status: 401, error: "유효하지 않은 API 키" };
  return { ok: true, id: sha(keys[match]).toString("hex").slice(0, 8) };
}

export async function body(req) {
  if (req.body && typeof req.body === "object") return req.body;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  try { return JSON.parse(Buffer.concat(chunks).toString() || "{}"); } catch { return {}; }
}
