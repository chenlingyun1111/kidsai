import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Courseware(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "courseware"

    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("parents.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    file_type: Mapped[str] = mapped_column(String(20))
    file_url: Mapped[str] = mapped_column(String(500))
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column(String(20), default="processing")
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    chunks = relationship("CoursewareChunk", back_populates="courseware", cascade="all, delete-orphan")


class CoursewareChunk(Base, UUIDMixin):
    __tablename__ = "courseware_chunks"

    courseware_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courseware.id", ondelete="CASCADE")
    )
    chunk_type: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    embedding = mapped_column(Vector(1536), nullable=True)

    courseware = relationship("Courseware", back_populates="chunks")
