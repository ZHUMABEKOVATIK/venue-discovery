from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SessionOut(BaseModel):
    id: int
    user_agent: str | None
    ip_address: str | None
    created_at: datetime
    expires_at: datetime
    is_current: bool = False

    model_config = ConfigDict(from_attributes=True)


class RevokeSessionIn(BaseModel):
    refresh_token: str