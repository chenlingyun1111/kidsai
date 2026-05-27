from app.ai.base import STTProvider
from app.config import settings


def get_stt_provider() -> STTProvider:
    match settings.stt_provider:
        case "volcano":
            from app.ai.stt.volcano_stt import VolcanoSTT
            return VolcanoSTT()
        case "whisper":
            from app.ai.stt.whisper_provider import WhisperSTT
            return WhisperSTT()
        case _:
            raise ValueError(f"Unknown STT provider: {settings.stt_provider}")
