// GET /api/health — 인덱스 스냅샷/설정 상태(키 값은 노출하지 않음)
import { loadIndex, vectorsAvailable } from "../lib/search.mjs";
import { chatConfig, embedConfig } from "../lib/llm.mjs";
import { cors, json } from "../lib/http.mjs";

export default function handler(req, res) {
  cors(res);
  const S = loadIndex();
  json(res, 200, {
    ok: true,
    wikiCommit: S.meta.wikiCommit,
    builtAt: S.meta.builtAt,
    chunks: S.meta.chunks,
    byCategory: S.meta.byCategory,
    vectors: !!S.vec,
    vectorSearchActive: vectorsAvailable(),
    embeddingModel: S.vmeta?.model || null,
    answerModelConfigured: !!chatConfig(),
    embeddingConfigured: !!embedConfig(),
    tokenProtectedAsk: !!process.env.RAG_API_TOKEN,
  });
}
