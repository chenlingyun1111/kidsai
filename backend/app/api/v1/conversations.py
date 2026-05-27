import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentParent, DbSession
from app.models.conversation import Conversation

router = APIRouter()


@router.get("")
async def list_conversations(parent: CurrentParent, db: DbSession, child_id: uuid.UUID | None = None):
    query = select(Conversation).join(Conversation.child)
    if child_id:
        query = query.where(Conversation.child_id == child_id)
    result = await db.execute(query.order_by(Conversation.started_at.desc()).limit(50))
    return result.scalars().all()


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: uuid.UUID, parent: CurrentParent, db: DbSession):
    result = await db.execute(
        select(Conversation)
        .options(selectinload(Conversation.turns))
        .where(Conversation.id == conversation_id)
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv
