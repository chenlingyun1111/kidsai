from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select

from app.api.deps import CurrentParent, DbSession
from app.api.schemas.auth import LoginRequest, PinVerifyRequest, RegisterRequest, TokenResponse
from app.config import settings
from app.models.parent import Parent

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(parent_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub": parent_id, "exp": expire}, settings.jwt_secret, settings.jwt_algorithm)


@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, db: DbSession):
    existing = await db.execute(select(Parent).where(Parent.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    parent = Parent(
        email=req.email,
        password_hash=pwd_context.hash(req.password),
        pin_hash=pwd_context.hash(req.pin),
        display_name=req.display_name,
    )
    db.add(parent)
    await db.commit()
    await db.refresh(parent)
    return TokenResponse(access_token=create_token(str(parent.id)))


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: DbSession):
    result = await db.execute(select(Parent).where(Parent.email == req.email))
    parent = result.scalar_one_or_none()
    if not parent or not pwd_context.verify(req.password, parent.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_token(str(parent.id)))


@router.post("/verify-pin")
async def verify_pin(req: PinVerifyRequest, parent: CurrentParent):
    if not pwd_context.verify(req.pin, parent.pin_hash):
        raise HTTPException(status_code=403, detail="Invalid PIN")
    return {"verified": True}
