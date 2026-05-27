import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Character(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "characters"

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("parents.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    personality: Mapped[str] = mapped_column(Text)
    backstory: Mapped[str | None] = mapped_column(Text)
    speaking_style: Mapped[str] = mapped_column(Text)
    catchphrases: Mapped[dict] = mapped_column(JSONB, default=list)
    voice_id: Mapped[str | None] = mapped_column(String(100))
    rive_asset_url: Mapped[str | None] = mapped_column(String(500))
    world_rules: Mapped[dict] = mapped_column(JSONB)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    parent = relationship("Parent", back_populates="characters")
