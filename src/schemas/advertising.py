from pydantic import BaseModel, ConfigDict

class CategoryShortOut(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class AdvertisingOut(BaseModel):
    category: CategoryShortOut
    photo_url: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)