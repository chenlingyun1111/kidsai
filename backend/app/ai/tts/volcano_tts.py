from collections.abc import AsyncIterator

from app.ai.base import TTSProvider


class VolcanoTTS(TTSProvider):
    """Volcano Engine (Doubao) TTS provider.

    TODO: Implement using Volcano Engine Speech SDK.
    Docs: https://www.volcengine.com/docs/6561
    """

    async def synthesize_stream(self, text: str, voice_id: str) -> AsyncIterator[bytes]:
        raise NotImplementedError("Volcano TTS streaming not yet implemented")

    async def synthesize(self, text: str, voice_id: str) -> bytes:
        raise NotImplementedError("Volcano TTS not yet implemented")
