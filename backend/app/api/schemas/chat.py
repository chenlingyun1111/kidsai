import uuid

from pydantic import BaseModel


class ChatRequest(BaseModel):
    child_id: uuid.UUID
    character_id: uuid.UUID
    message: str


class ChatResponse(BaseModel):
    reply: str
    character_emotion: str
    audio_url: str | None = None
