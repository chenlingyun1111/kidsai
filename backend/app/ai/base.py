from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMProvider(ABC):
    @abstractmethod
    async def chat_stream(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> AsyncIterator[str]:
        """Stream LLM response tokens."""
        ...

    @abstractmethod
    async def chat(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> str:
        """Single-shot LLM response."""
        ...


class STTProvider(ABC):
    @abstractmethod
    async def transcribe_stream(self, audio_chunks: AsyncIterator[bytes]) -> AsyncIterator[str]:
        """Stream audio chunks, yield partial transcripts."""
        ...

    @abstractmethod
    async def transcribe(self, audio_data: bytes, language: str = "en") -> str:
        """Transcribe a complete audio buffer."""
        ...


class TTSProvider(ABC):
    @abstractmethod
    async def synthesize_stream(self, text: str, voice_id: str) -> AsyncIterator[bytes]:
        """Stream synthesized audio chunks for the given text."""
        ...

    @abstractmethod
    async def synthesize(self, text: str, voice_id: str) -> bytes:
        """Synthesize complete audio for the given text."""
        ...


class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        ...
