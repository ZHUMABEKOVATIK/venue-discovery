from pydantic import BaseModel, EmailStr, ConfigDict
from src.models.model_enums import UserRole


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str | None
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
