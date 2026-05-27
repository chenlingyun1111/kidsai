import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Conversation(Base, UUIDMixin):
    __tablename__ = "conversations"

    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE")
    )
    character_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters.id")
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    turn_count: Mapped[int] = mapped_column(SmallInteger, default=0)
    topics_covered: Mapped[dict] = mapped_column(JSONB, default=list)
    vocabulary_used: Mapped[dict] = mapped_column(JSONB, default=list)
    summary: Mapped[str | None] = mapped_column(Text)

    child = relationship("Child", back_populates="conversations")
    turns = relationship("ConversationTurn", back_populates="conversation", cascade="all, delete-orphan")


class ConversationTurn(Base, UUIDMixin):
    __tablename__ = "conversation_turns"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE")
    )
    turn_number: Mapped[int] = mapped_column(SmallInteger)
    role: Mapped[str] = mapped_column(String(10))
    transcript: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String(500))
    detected_items: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    conversation = relationship("Conversation", back_populates="turns")
