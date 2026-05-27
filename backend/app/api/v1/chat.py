import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.api.deps import CurrentParent, DbSession
from app.api.schemas.chat import ChatRequest, ChatResponse
from app.services import chat_service

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, parent: CurrentParent, db: DbSession):
    try:
        result = await chat_service.chat(db, req.child_id, req.character_id, req.message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ChatResponse(**result)


@router.post("/audio")
async def chat_with_audio(req: ChatRequest, parent: CurrentParent, db: DbSession):
    try:
        result = await chat_service.chat(db, req.child_id, req.character_id, req.message)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    audio_data = await chat_service.synthesize_reply(result["reply"])

    return Response(
        content=audio_data,
        media_type="audio/mpeg",
        headers={
            "X-Reply-Text": result["reply"].replace("\n", " "),
            "X-Character-Emotion": result["character_emotion"],
        },
    )


@router.delete("/session")
async def clear_session(
    child_id: uuid.UUID, character_id: uuid.UUID, parent: CurrentParent
):
    chat_service.clear_session(child_id, character_id)
    return {"status": "cleared"}
