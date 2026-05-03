from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class UserShortOut(BaseModel):
    id: int
    first_name: str
    last_name: str | None

    model_config = ConfigDict(from_attributes=True)

class FeedbackIn(BaseModel):
    venue_id: int
    rating: int = Field(..., examples=[1, 2, 3, 4, 5])
    review: str

class FeedbackOut(BaseModel):
    id: int
    user: UserShortOut
    rating: int
    review: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FeedbackUpdateIn(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    review: str | None = None