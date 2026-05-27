import uuid
from typing import Any

from pydantic import BaseModel


class CharacterCreate(BaseModel):
    name: str
    description: str | None = None
    personality: str
    backstory: str | None = None
    speaking_style: str
    catchphrases: list[str] = []
    voice_id: str | None = None
    rive_asset_url: str | None = None
    world_rules: dict[str, Any]


class CharacterUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    personality: str | None = None
    backstory: str | None = None
    speaking_style: str | None = None
    catchphrases: list[str] | None = None
    voice_id: str | None = None
    rive_asset_url: str | None = None
    world_rules: dict[str, Any] | None = None
    is_active: bool | None = None


class CharacterResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    personality: str
    backstory: str | None
    speaking_style: str
    catchphrases: list
    voice_id: str | None
    rive_asset_url: str | None
    world_rules: dict
    is_active: bool

    model_config = {"from_attributes": True}
