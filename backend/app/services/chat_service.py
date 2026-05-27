"""Text chat service - manages conversation state and orchestrates LLM calls."""

import uuid
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.llm import get_llm_provider
from app.ai.tts import get_tts_provider
from app.models.character import Character
from app.models.child import Child
from app.services.prompt_engine import PromptEngine
from app.services.safety_filter import is_safe, sanitize_output

_sessions: dict[str, list[dict]] = defaultdict(list)

prompt_engine = PromptEngine()


def _session_key(child_id: uuid.UUID, character_id: uuid.UUID) -> str:
    return f"{child_id}:{character_id}"


async def chat(
    db: AsyncSession,
    child_id: uuid.UUID,
    character_id: uuid.UUID,
    user_message: str,
) -> dict:
    character = await db.get(Character, character_id)
    if not character:
        raise ValueError("Character not found")

    child = await db.get(Child, child_id)
    if not child:
        raise ValueError("Child not found")

    char_dict = {
        "name": character.name,
        "catchphrases": character.catchphrases or [],
        "voice_id": character.voice_id or "girl",
        "world_rules": character.world_rules or {},
    }

    system_prompt = prompt_engine.build_system_prompt(char_dict)

    key = _session_key(child_id, character_id)
    messages = _sessions[key]

    if not is_safe(user_message):
        reply = char_dict["world_rules"].get("safety_rules", {}).get(
            "redirect_to", "Let's talk about something fun instead!"
        )
        return {"reply": reply, "character_emotion": "neutral"}

    messages.append({"role": "user", "content": user_message})

    # Keep conversation history manageable
    if len(messages) > 40:
        messages[:] = messages[-30:]

    llm = get_llm_provider()
    full_response = ""
    async for token in llm.chat_stream(system_prompt, messages):
        full_response += token

    full_response = sanitize_output(full_response)
    messages.append({"role": "assistant", "content": full_response})

    return {
        "reply": full_response,
        "character_emotion": "happy",
    }


async def synthesize_reply(text: str, voice_id: str = "girl") -> bytes:
    tts = get_tts_provider()
    return await tts.synthesize(text, voice_id)


def clear_session(child_id: uuid.UUID, character_id: uuid.UUID):
    key = _session_key(child_id, character_id)
    _sessions.pop(key, None)
