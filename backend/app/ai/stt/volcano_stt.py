from collections.abc import AsyncIterator

from app.ai.base import STTProvider


class VolcanoSTT(STTProvider):
    """Volcano Engine (Doubao) ASR provider.

    TODO: Implement using Volcano Engine Speech SDK.
    Docs: https://www.volcengine.com/docs/6561
    """

    async def transcribe_stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        raise NotImplementedError("Volcano STT streaming not yet implemented")

    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        raise NotImplementedError("Volcano STT not yet implemented")
