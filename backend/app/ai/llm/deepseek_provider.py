from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.ai.base import LLMProvider
from app.config import settings


class DeepSeekProvider(LLMProvider):
    """DeepSeek provider using OpenAI-compatible API."""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url="https://api.deepseek.com",
        )

    async def chat_stream(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> AsyncIterator[str]:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        stream = await self.client.chat.completions.create(
            model=settings.deepseek_model,
            messages=full_messages,
            temperature=temperature,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def chat(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> str:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = await self.client.chat.completions.create(
            model=settings.deepseek_model,
            messages=full_messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
