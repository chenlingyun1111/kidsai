import uuid

from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Child(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "children"

    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("parents.id", ondelete="CASCADE")
    )
    display_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int | None] = mapped_column(SmallInteger)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    english_level: Mapped[str] = mapped_column(String(20), default="beginner")
    daily_time_limit_minutes: Mapped[int] = mapped_column(SmallInteger, default=30)

    parent = relationship("Parent", back_populates="children")
    conversations = relationship("Conversation", back_populates="child", cascade="all, delete-orphan")
    progress = relationship("LearningProgress", back_populates="child", cascade="all, delete-orphan")
    goals = relationship("LearningGoal", back_populates="child", cascade="all, delete-orphan")
