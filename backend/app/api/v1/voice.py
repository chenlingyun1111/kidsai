import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.voice_session import VoiceSession

router = APIRouter()


@router.websocket("/session")
async def voice_session(ws: WebSocket, child_id: uuid.UUID, character_id: uuid.UUID):
    await ws.accept()

    session = VoiceSession(
        websocket=ws,
        child_id=child_id,
        character_id=character_id,
    )

    try:
        await session.run()
    except WebSocketDisconnect:
        await session.cleanup()
