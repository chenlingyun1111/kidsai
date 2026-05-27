from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Parent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "parents"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    pin_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str | None] = mapped_column(String(100))
    locale: Mapped[str] = mapped_column(String(10), default="zh-CN")

    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="parent")
