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

async function post(url, body, key, tries = 4) {
  let last;
  for (let a = 0; a < tries; a++) {
    try {
      const r = await fetch(url, {
        method: "POST",
        headers: { "content-type": "application/json", authorization: `Bearer ${key}` },
        body: JSON.stringify(body),
        signal: AbortSignal.timeout(25000),
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
  const data = await post(`${c.base}/chat/completions`, body, c.key);
  const text = data.choices?.[0]?.message?.content ?? "";
  return { text: text.replace(/<think>[\s\S]*?<\/think>/g, "").trim(), model: c.model };
}
