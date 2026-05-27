from app.ai.base import TTSProvider
from app.config import settings


def get_tts_provider() -> TTSProvider:
    match settings.tts_provider:
        case "volcano":
            from app.ai.tts.volcano_tts import VolcanoTTS
            return VolcanoTTS()
        case "edge":
            from app.ai.tts.edge_tts_provider import EdgeTTSProvider
            return EdgeTTSProvider()
        case _:
            raise ValueError(f"Unknown TTS provider: {settings.tts_provider}")
