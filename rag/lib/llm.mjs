// OpenAI 호환 임베딩/채팅 클라이언트. 키는 환경변수로만 읽는다(코드·저장소에 두지 않음).
//  채팅: WIKI_LLM_BASE_URL / WIKI_LLM_API_KEY / WIKI_LLM_MODEL  (sj-wiki 위키 정리와 동일한 이름)
//  임베딩: EMBED_BASE_URL / EMBED_API_KEY / EMBED_MODEL  (미지정 시 위 채팅 설정의 BASE_URL·KEY 재사용)

export function chatConfig() {
  const base = process.env.WIKI_LLM_BASE_URL, key = process.env.WIKI_LLM_API_KEY, model = process.env.WIKI_LLM_MODEL;
  return base && key && model ? { base: base.replace(/\/$/, ""), key, model } : null;
}

export function embedConfig() {
  const base = process.env.EMBED_BASE_URL || process.env.WIKI_LLM_BASE_URL;
  const key = process.env.EMBED_API_KEY || process.env.WIKI_LLM_API_KEY;
  const model = process.env.EMBED_MODEL;
  return base && key && model ? { base: base.replace(/\/$/, ""), key, model, dims: process.env.EMBED_DIMENSIONS ? +process.env.EMBED_DIMENSIONS : null } : null;
}

async function post(url, body, key, tries = 4, timeoutMs = 25000) {
  let last;
  for (let a = 0; a < tries; a++) {
    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${key}` },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(timeoutMs),
      });
      if (r.ok) return await r.json();
      last = new Error(`HTTP ${r.status}: ${(await r.text()).slice(0, 200)}`);
      if (![408, 429, 500, 502, 503, 504].includes(r.status)) throw last;
    } catch (e) {
      last = e;
      if (/^HTTP 4(?!08|29)/.test(String(e.message))) throw e;
    }
    await new Promise((res) => setTimeout(res, 800 * 2 ** a));
  }
  throw last;
}

function normalize(v) {
  let n = 0;
  for (const x of v) n += x * x;
  n = Math.sqrt(n) || 1;
  return v.map((x) => x / n);
}

export async function embed(texts) {
  const c = embedConfig();
  if (!c) throw new Error("embedding not configured");
  const body = { model: c.model, input: texts };
  if (c.dims) body.dimensions = c.dims;
  const data = await post(`${c.base}/embeddings`, body, c.key);
  return data.data.sort((a, b) => a.index - b.index).map((d) => normalize(d.embedding));
}

export async function chat(messages, { maxTokens = 900, temperature = 0.2 } = {}) {
  const c = chatConfig();
  if (!c) throw new Error("chat model not configured");
  const body = { model: c.model, messages, max_tokens: maxTokens, temperature };
  if (process.env.WIKI_LLM_REASONING_EFFORT) body.reasoning_effort = process.env.WIKI_LLM_REASONING_EFFORT;
  const data = await post(`${c.base}/chat/completions`, body, c.key, 1, 50000);
  const text = data.choices?.[0]?.message?.content ?? "";
  return { text: text.replace(/<think>[\s\S]*?<\/think>/g, "").trim(), model: c.model };
}

// 스트리밍 채팅: delta.content 조각을 순서대로 yield. (reasoning_content·<think>는 버린다)
export async function* chatStream(messages, { maxTokens = 600, temperature = 0.2, timeoutMs = 55000 } = {}) {
  const c = chatConfig();
  if (!c) throw new Error("chat model not configured");
  const body = { model: c.model, messages, max_tokens: maxTokens, temperature, stream: true };
  if (process.env.WIKI_LLM_REASONING_EFFORT) body.reasoning_effort = process.env.WIKI_LLM_REASONING_EFFORT;
  const r = await fetch(`${c.base}/chat/completions`, {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${c.key}` },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${(await r.text()).slice(0, 200)}`);

  // <think>…</think> 제거용 상태 (태그가 조각 경계에 걸쳐도 안전하게)
  let inThink = false, pending = "";
  const OPEN = "<think>", CLOSE = "</think>";
  const keepTail = (str, tag) => { for (let n = Math.min(tag.length - 1, str.length); n > 0; n--) if (tag.startsWith(str.slice(-n))) return n; return 0; };
  function* filter(piece) {
    pending += piece;
    for (;;) {
      if (!inThink) {
        const i = pending.indexOf(OPEN);
        if (i >= 0) { if (i) yield pending.slice(0, i); pending = pending.slice(i + OPEN.length); inThink = true; continue; }
        const k = keepTail(pending, OPEN);
        if (pending.length - k) yield pending.slice(0, pending.length - k);
        pending = pending.slice(pending.length - k);
        return;
      }
      const i = pending.indexOf(CLOSE);
      if (i >= 0) { pending = pending.slice(i + CLOSE.length); inThink = false; continue; }
      pending = pending.slice(pending.length - keepTail(pending, CLOSE));
      return;
    }
  }

  const ct = r.headers.get("content-type") || "";
  if (!ct.includes("event-stream")) { // 스트리밍 미지원 응답 → 한 번에 도착한 것으로 처리
    const data = await r.json();
    const text = String(data.choices?.[0]?.message?.content ?? "");
    for (const t of filter(text)) yield t;
    if (!inThink && pending) yield pending;
    return;
  }
  const dec = new TextDecoder();
  let buf = "";
  for await (const chunk of r.body) {
    buf += dec.decode(chunk, { stream: true });
    let nl;
    while ((nl = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, nl).trim();
      buf = buf.slice(nl + 1);
      if (!line.startsWith("data:")) continue;
      const payload = line.slice(5).trim();
      if (!payload || payload === "[DONE]") continue;
      let j; try { j = JSON.parse(payload); } catch { continue; } // 조각난 JSON은 건너뜀
      const t = j.choices?.[0]?.delta?.content;
      if (t) for (const o of filter(t)) yield o;
    }
  }
  if (!inThink && pending) yield pending;
}
