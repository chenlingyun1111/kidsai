import dashscope
from dashscope import TextEmbedding

from app.ai.base import EmbeddingProvider
from app.config import settings


class QwenEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        dashscope.api_key = settings.dashscope_api_key

    async def embed(self, texts: list[str]) -> list[list[float]]:
        response = TextEmbedding.call(
            model="text-embedding-v3",
            input=texts,
        )
        return [item["embedding"] for item in response.output["embeddings"]]
