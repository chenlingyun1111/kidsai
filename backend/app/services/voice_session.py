import asyncio
import json
import uuid

from fastapi import WebSocket

from app.ai.llm import get_llm_provider
from app.ai.tts import get_tts_provider
from app.db.session import async_session
from app.models.character import Character
from app.models.child import Child
from app.services.prompt_engine import PromptEngine
from app.services.safety_filter import is_safe, sanitize_output


class VoiceSession:
    """Orchestrates real-time voice conversation over WebSocket.

    MVP flow: Text In -> LLM -> TTS -> Audio Out
    Full flow (Phase 2): Audio In -> STT -> LLM -> TTS -> Audio Out
    """

    def __init__(self, websocket: WebSocket, child_id: uuid.UUID, character_id: uuid.UUID):
        self.ws = websocket
        self.child_id = child_id
        self.character_id = character_id
        self.llm = get_llm_provider()
        self.tts = get_tts_provider()
        self.prompt_engine = PromptEngine()
        self.messages: list[dict] = []
        self.character: dict = {}
        self.system_prompt: str = ""
        self._cancelled = False

    async def run(self):
        await self._load_session_context()
        await self._send_greeting()

        while True:
            data = await self.ws.receive()

            if data.get("type") == "websocket.disconnect":
                break

            if "bytes" in data:
                await self._handle_audio(data["bytes"])
            elif "text" in data:
                msg = json.loads(data["text"])
                match msg.get("type"):
                    case "session_end":
                        break
                    case "interrupt":
                        self._cancelled = True
                    case "text_message":
                        await self._handle_text(msg.get("text", ""))

        await self.cleanup()

    async def _load_session_context(self):
        async with async_session() as db:
            character = await db.get(Character, self.character_id)
            child = await db.get(Child, self.child_id)

        if character:
            self.character = {
                "name": character.name,
                "catchphrases": character.catchphrases or [],
                "voice_id": character.voice_id or "girl",
                "world_rules": character.world_rules or {},
            }
        else:
            self.character = {
                "name": "Spark",
                "catchphrases": ["Super sparkly!"],
                "voice_id": "girl",
                "world_rules": {
                    "character_meta": {"name": "Spark", "species": "Baby Dragon", "world": "Letter Land"},
                    "personality": {"traits": ["cheerful", "curious"]},
                    "speaking_style": {"vocabulary_level": "simple", "sentence_length": "5-10 words"},
                    "safety_rules": {"never_discuss": ["violence"], "redirect_to": "Let's talk about something fun!"},
                },
            }

        self.system_prompt = self.prompt_engine.build_system_prompt(self.character)

    async def _send_greeting(self):
        name = self.character.get("name", "Spark")
        greeting = f"Hi there! I'm {name}! Ready to play and learn together?"
        self.messages.append({"role": "assistant", "content": greeting})

        await self.ws.send_json({
            "type": "ai_text",
            "text": greeting,
            "character_emotion": "happy",
        })

        await self._stream_tts(greeting)

        await self.ws.send_json({"type": "ai_turn_complete", "character_emotion": "happy"})

    async def _handle_text(self, text: str):
        if not text.strip():
            return

        await self.ws.send_json({"type": "transcript_final", "text": text})

        if not is_safe(text):
            redirect = self.character.get("world_rules", {}).get(
                "safety_rules", {}
            ).get("redirect_to", "Let's talk about something fun!")
            await self._send_ai_response(redirect)
            return

        self.messages.append({"role": "user", "content": text})

        if len(self.messages) > 40:
            self.messages[:] = self.messages[-30:]

        self._cancelled = False
        full_response = ""
        sentence_buffer = ""

        async for token in self.llm.chat_stream(self.system_prompt, self.messages):
            if self._cancelled:
                break

            full_response += token
            sentence_buffer += token

            await self.ws.send_json({"type": "ai_text_partial", "text": token})

            if any(sentence_buffer.rstrip().endswith(p) for p in ".!?。！？"):
                sentence = sentence_buffer.strip()
                sentence_buffer = ""
                asyncio.create_task(self._stream_tts(sentence))

        if sentence_buffer.strip() and not self._cancelled:
            await self._stream_tts(sentence_buffer.strip())

        full_response = sanitize_output(full_response)
        self.messages.append({"role": "assistant", "content": full_response})

        await self.ws.send_json({
            "type": "ai_turn_complete",
            "text": full_response,
            "character_emotion": "happy",
        })

    async def _handle_audio(self, audio_data: bytes):
        # Phase 2: STT integration
        # For now, send a message asking to use text mode
        await self.ws.send_json({
            "type": "error",
            "message": "Audio STT not yet available. Send text_message instead.",
        })

    async def _send_ai_response(self, text: str):
        self.messages.append({"role": "assistant", "content": text})
        await self.ws.send_json({"type": "ai_text", "text": text, "character_emotion": "neutral"})
        await self._stream_tts(text)
        await self.ws.send_json({"type": "ai_turn_complete", "character_emotion": "neutral"})

    async def _stream_tts(self, text: str):
        voice_id = self.character.get("voice_id", "girl")
        try:
            async for chunk in self.tts.synthesize_stream(text, voice_id):
                if self._cancelled:
                    break
                await self.ws.send_bytes(chunk)
        except Exception:
            pass

    async def cleanup(self):
        pass
