from collections.abc import AsyncIterator

import anthropic

from app.ai.base import LLMProvider
from app.config import settings


class ClaudeProvider(LLMProvider):
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=settings.claude_api_key)

    async def chat_stream(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> AsyncIterator[str]:
        async with self.client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
            temperature=temperature,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def chat(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> str:
        response = await self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
            temperature=temperature,
        )
        return response.content[0].text
