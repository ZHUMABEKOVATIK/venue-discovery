from pydantic import BaseModel, Field

class RegionIn(BaseModel):
    name: str

class RegionOut(BaseModel):
    id: int
    name: str