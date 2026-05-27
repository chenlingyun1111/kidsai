from collections.abc import AsyncIterator

import httpx

from app.ai.base import STTProvider


class WhisperSTT(STTProvider):
    """OpenAI Whisper API provider (fallback)."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    async def transcribe_stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        raise NotImplementedError("Whisper does not support streaming STT")

    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": ("audio.wav", audio_data, "audio/wav")},
                data={"model": "whisper-1", "language": language},
            )
            response.raise_for_status()
            return response.json()["text"]
