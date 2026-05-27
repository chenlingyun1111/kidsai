import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class LearningProgress(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "learning_progress"
    __table_args__ = (
        UniqueConstraint("child_id", "item_type", "item_key", name="uq_child_item"),
    )

    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE")
    )
    courseware_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courseware.id"), nullable=True
    )
    item_type: Mapped[str] = mapped_column(String(30))
    item_key: Mapped[str] = mapped_column(String(255))
    times_practiced: Mapped[int] = mapped_column(SmallInteger, default=0)
    times_correct: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_practiced: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    mastery_level: Mapped[int] = mapped_column(SmallInteger, default=0)
    notes: Mapped[str | None] = mapped_column(Text)

    child = relationship("Child", back_populates="progress")
