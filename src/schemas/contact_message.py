from pydantic import BaseModel, EmailStr

class ContactMessageIn(BaseModel):
    email: EmailStr
    name: str
    message: str

class ContactMessageOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    message: str
    is_read: bool