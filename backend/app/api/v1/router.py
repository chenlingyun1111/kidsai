from fastapi import APIRouter

from app.api.v1 import auth, characters, children, conversations, courseware, goals, voice

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(children.router, prefix="/children", tags=["children"])
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(courseware.router, prefix="/courseware", tags=["courseware"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
