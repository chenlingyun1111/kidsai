import asyncio
import json
import uuid

from fastapi import WebSocket

from app.ai.llm import get_llm_provider
from app.ai.stt import get_stt_provider
from app.ai.tts import get_tts_provider
from app.services.prompt_engine import PromptEngine


class VoiceSession:
    """Orchestrates real-time voice conversation over WebSocket.

    Flow: Audio In -> STT -> LLM -> TTS -> Audio Out
    All stages are streaming for minimum latency.
    """

    def __init__(self, websocket: WebSocket, child_id: uuid.UUID, character_id: uuid.UUID):
        self.ws = websocket
        self.child_id = child_id
        self.character_id = character_id
        self.llm = get_llm_provider()
        self.stt = get_stt_provider()
        self.tts = get_tts_provider()
        self.prompt_engine = PromptEngine()
        self.messages: list[dict] = []
        self.character: dict = {}
        self.system_prompt: str = ""

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
                if msg.get("type") == "session_end":
                    break
                elif msg.get("type") == "interrupt":
                    pass  # TODO: cancel current TTS playback

        await self.cleanup()

    async def _load_session_context(self):
        # TODO: load character, courseware context, and learning state from DB
        self.character = {
            "name": "Spark",
            "catchphrases": ["Super sparkly!", "Roar-some job!"],
            "world_rules": {
                "character_meta": {"name": "Spark", "species": "Baby Dragon", "world": "Letter Land"},
                "personality": {"traits": ["cheerful", "curious", "encouraging"]},
                "speaking_style": {
                    "vocabulary_level": "simple, age-appropriate",
                    "sentence_length": "5-10 words max",
                    "tone": "warm and enthusiastic",
                    "forbidden_patterns": ["Never say 'wrong'", "No sarcasm"],
                },
                "teaching_behavior": {
                    "correction_style": "gentle_redirect",
                    "singing_enabled": True,
                    "game_types": ["rhyming", "word_chain"],
                },
                "safety_rules": {
                    "never_discuss": ["violence", "scary topics"],
                    "redirect_to": "Let's talk about something fun instead!",
                },
                "interaction_rules": [
                    "Keep responses under 3 sentences",
                    "Celebrate every attempt",
                ],
            },
        }
        self.system_prompt = self.prompt_engine.build_system_prompt(self.character)

    async def _send_greeting(self):
        greeting = "Hi there! I'm Spark the Dragon! Ready to play and learn together?"
        self.messages.append({"role": "assistant", "content": greeting})

        await self.ws.send_json({
            "type": "ai_text_partial",
            "text": greeting,
        })

        # Stream greeting audio
        async for chunk in self.tts.synthesize_stream(greeting, "girl"):
            await self.ws.send_bytes(chunk)

        await self.ws.send_json({
            "type": "ai_turn_complete",
            "character_emotion": "happy",
        })

    async def _handle_audio(self, audio_data: bytes):
        transcript = await self.stt.transcribe(audio_data)

        await self.ws.send_json({
            "type": "transcript_final",
            "text": transcript,
        })

        self.messages.append({"role": "user", "content": transcript})

        # Stream LLM response, collect for TTS
        full_response = ""
        sentence_buffer = ""

        async for token in self.llm.chat_stream(self.system_prompt, self.messages):
            full_response += token
            sentence_buffer += token

            await self.ws.send_json({
                "type": "ai_text_partial",
                "text": token,
            })

            # When we hit a sentence boundary, send to TTS
            if any(sentence_buffer.endswith(p) for p in [".", "!", "?", "。", "！", "？"]):
                asyncio.create_task(self._stream_tts(sentence_buffer.strip()))
                sentence_buffer = ""

        # Flush remaining text
        if sentence_buffer.strip():
            asyncio.create_task(self._stream_tts(sentence_buffer.strip()))

        self.messages.append({"role": "assistant", "content": full_response})

        await self.ws.send_json({
            "type": "ai_turn_complete",
            "character_emotion": "happy",
        })

    async def _stream_tts(self, text: str):
        voice_id = self.character.get("voice_id", "girl")
        async for chunk in self.tts.synthesize_stream(text, voice_id):
            await self.ws.send_bytes(chunk)

    async def cleanup(self):
        # TODO: save conversation to DB, update learning progress
        pass
