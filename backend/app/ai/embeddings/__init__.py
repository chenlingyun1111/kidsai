from app.ai.base import EmbeddingProvider


def get_embedding_provider() -> EmbeddingProvider:
    from app.ai.embeddings.qwen_embeddings import QwenEmbeddingProvider
    return QwenEmbeddingProvider()
