from collections.abc import AsyncIterator

import dashscope
from dashscope import Generation

from app.ai.base import LLMProvider
from app.config import settings


class QwenProvider(LLMProvider):
    def __init__(self):
        dashscope.api_key = settings.dashscope_api_key

    async def chat_stream(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> AsyncIterator[str]:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        responses = Generation.call(
            model="qwen-max",
            messages=full_messages,
            temperature=temperature,
            result_format="message",
            stream=True,
            incremental_output=True,
        )
        for response in responses:
            if response.output and response.output.choices:
                content = response.output.choices[0].message.content
                if content:
                    yield content

    async def chat(
        self, system_prompt: str, messages: list[dict], temperature: float = 0.7
    ) -> str:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = Generation.call(
            model="qwen-max",
            messages=full_messages,
            temperature=temperature,
            result_format="message",
        )
        return response.output.choices[0].message.content
