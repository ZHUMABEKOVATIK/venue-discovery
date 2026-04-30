from pydantic import BaseModel

class RegionIn(BaseModel):
    name: str

class RegionOut(BaseModel):
    id: int
    name: str