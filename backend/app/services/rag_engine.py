"""RAG engine for retrieving relevant courseware chunks during conversation."""

import uuid

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings import get_embedding_provider
from app.models.courseware import CoursewareChunk


async def retrieve_relevant_chunks(
    db: AsyncSession,
    query: str,
    parent_id: uuid.UUID,
    top_k: int = 5,
) -> list[str]:
    embedder = get_embedding_provider()
    [query_embedding] = await embedder.embed([query])

    result = await db.execute(
        select(CoursewareChunk.content)
        .join(CoursewareChunk.courseware)
        .where(text("courseware.parent_id = :pid"))
        .order_by(CoursewareChunk.embedding.cosine_distance(query_embedding))
        .limit(top_k),
        {"pid": parent_id},
    )

    chunks = result.scalars().all()
    return list(chunks)


def format_context(chunks: list[str]) -> str:
    if not chunks:
        return ""
    return "\n".join(f"- {chunk}" for chunk in chunks)
