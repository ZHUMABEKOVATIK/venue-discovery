from pydantic import BaseModel, EmailStr, field_validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("En' keminde 6 belgi kiritin'")
        if len(v) > 128:
            raise ValueError("En' ko'bi 128 belgi")
        return v

class GuestRegisterRequest(RegisterRequest):
    pass

class OwnerRegisterRequest(RegisterRequest):
    pass


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str