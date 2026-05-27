from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    pin: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PinVerifyRequest(BaseModel):
    pin: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
