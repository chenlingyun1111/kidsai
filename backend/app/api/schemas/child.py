import uuid

from pydantic import BaseModel


class ChildCreate(BaseModel):
    display_name: str
    age: int | None = None
    english_level: str = "beginner"
    daily_time_limit_minutes: int = 30


class ChildUpdate(BaseModel):
    display_name: str | None = None
    age: int | None = None
    english_level: str | None = None
    daily_time_limit_minutes: int | None = None


class ChildResponse(BaseModel):
    id: uuid.UUID
    display_name: str
    age: int | None
    english_level: str
    daily_time_limit_minutes: int

    model_config = {"from_attributes": True}
