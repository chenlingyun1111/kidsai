from app.ai.base import LLMProvider
from app.config import settings


def get_llm_provider() -> LLMProvider:
    match settings.llm_provider:
        case "deepseek":
            from app.ai.llm.deepseek_provider import DeepSeekProvider
            return DeepSeekProvider()
        case "qwen":
            from app.ai.llm.qwen_provider import QwenProvider
            return QwenProvider()
        case "claude":
            from app.ai.llm.claude_provider import ClaudeProvider
            return ClaudeProvider()
        case _:
            raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
