"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-27
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "parents",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("pin_hash", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100)),
        sa.Column("locale", sa.String(10), server_default="zh-CN"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "children",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("parent_id", sa.UUID(), sa.ForeignKey("parents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("age", sa.SmallInteger()),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("english_level", sa.String(20), server_default="beginner"),
        sa.Column("daily_time_limit_minutes", sa.SmallInteger(), server_default="30"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "characters",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("parent_id", sa.UUID(), sa.ForeignKey("parents.id"), nullable=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("personality", sa.Text(), nullable=False),
        sa.Column("backstory", sa.Text()),
        sa.Column("speaking_style", sa.Text(), nullable=False),
        sa.Column("catchphrases", sa.JSON(), server_default="[]"),
        sa.Column("voice_id", sa.String(100)),
        sa.Column("rive_asset_url", sa.String(500)),
        sa.Column("world_rules", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "courseware",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("parent_id", sa.UUID(), sa.ForeignKey("parents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("file_type", sa.String(20), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger()),
        sa.Column("status", sa.String(20), server_default="processing"),
        sa.Column("metadata", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "courseware_chunks",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("courseware_id", sa.UUID(), sa.ForeignKey("courseware.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_type", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), server_default="{}"),
        sa.Column("embedding", Vector(1536)),
    )

    op.create_table(
        "learning_progress",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("child_id", sa.UUID(), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("courseware_id", sa.UUID(), sa.ForeignKey("courseware.id"), nullable=True),
        sa.Column("item_type", sa.String(30), nullable=False),
        sa.Column("item_key", sa.String(255), nullable=False),
        sa.Column("times_practiced", sa.SmallInteger(), server_default="0"),
        sa.Column("times_correct", sa.SmallInteger(), server_default="0"),
        sa.Column("last_practiced", sa.DateTime(timezone=True)),
        sa.Column("mastery_level", sa.SmallInteger(), server_default="0"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("child_id", "item_type", "item_key", name="uq_child_item"),
    )

    op.create_table(
        "conversations",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("child_id", sa.UUID(), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("character_id", sa.UUID(), sa.ForeignKey("characters.id"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.Column("duration_seconds", sa.Integer()),
        sa.Column("turn_count", sa.SmallInteger(), server_default="0"),
        sa.Column("topics_covered", sa.JSON(), server_default="[]"),
        sa.Column("vocabulary_used", sa.JSON(), server_default="[]"),
        sa.Column("summary", sa.Text()),
    )

    op.create_table(
        "conversation_turns",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("conversation_id", sa.UUID(), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("turn_number", sa.SmallInteger(), nullable=False),
        sa.Column("role", sa.String(10), nullable=False),
        sa.Column("transcript", sa.Text(), nullable=False),
        sa.Column("audio_url", sa.String(500)),
        sa.Column("detected_items", sa.JSON(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "learning_goals",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("child_id", sa.UUID(), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("goal_type", sa.String(30), nullable=False),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("priority", sa.SmallInteger(), server_default="5"),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("progress_pct", sa.SmallInteger(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index(
        "idx_courseware_chunks_embedding",
        "courseware_chunks",
        ["embedding"],
        postgresql_using="ivfflat",
        postgresql_with={"lists": 100},
        postgresql_ops={"embedding": "vector_cosine_ops"},
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_table("learning_goals")
    op.drop_table("conversation_turns")
    op.drop_table("conversations")
    op.drop_table("learning_progress")
    op.drop_table("courseware_chunks")
    op.drop_table("courseware")
    op.drop_table("characters")
    op.drop_table("children")
    op.drop_table("parents")
