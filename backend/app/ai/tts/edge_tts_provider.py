from collections.abc import AsyncIterator
from io import BytesIO

import edge_tts

from app.ai.base import TTSProvider


class EdgeTTSProvider(TTSProvider):
    """Microsoft Edge TTS - free fallback provider with good English voices."""

    VOICE_MAP = {
        "default": "en-US-AnaNeural",
        "boy": "en-US-GuyNeural",
        "girl": "en-US-AnaNeural",
        "british": "en-GB-SoniaNeural",
    }

    async def synthesize_stream(self, text: str, voice_id: str) -> AsyncIterator[bytes]:
        voice = self.VOICE_MAP.get(voice_id, voice_id)
        communicate = edge_tts.Communicate(text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    async def synthesize(self, text: str, voice_id: str) -> bytes:
        buf = BytesIO()
        async for chunk in self.synthesize_stream(text, voice_id):
            buf.write(chunk)
        return buf.getvalue()
