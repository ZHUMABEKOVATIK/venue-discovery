from pydantic import BaseModel, ConfigDict

class RegionIn(BaseModel):
    name: str

class RegionOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)