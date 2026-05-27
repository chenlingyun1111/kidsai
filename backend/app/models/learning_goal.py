import uuid

from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class LearningGoal(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "learning_goals"

    child_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("children.id", ondelete="CASCADE")
    )
    goal_type: Mapped[str] = mapped_column(String(30))
    target: Mapped[str] = mapped_column(String(255))
    priority: Mapped[int] = mapped_column(SmallInteger, default=5)
    status: Mapped[str] = mapped_column(String(20), default="active")
    progress_pct: Mapped[int] = mapped_column(SmallInteger, default=0)

    child = relationship("Child", back_populates="goals")
