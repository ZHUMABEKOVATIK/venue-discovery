from fastapi import APIRouter, UploadFile, status, File, Form
from src.dependencies import AdminDep, AdvertisingServiceDep

router = APIRouter(prefix="/advertising", tags=["Advertising"])

@router.get("/")
async def get_all(
        service: AdvertisingServiceDep
    ):
    return await service.get_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
        user: AdminDep,
        service: AdvertisingServiceDep,
        photo: UploadFile = File(...),
        category_id: int = Form(...),
        title: str = Form(...),
        description: str = Form(...),
    ):
    return await service.create(category_id=category_id, description=description, photo=photo, title=title)

@router.patch("/photo/{advert_id}")
async def update_photo(
        advert_id: int,
        user: AdminDep,
        service: AdvertisingServiceDep,
        photo: UploadFile = File(...),
    ):
    return await service.update_photo(ad_id=advert_id, photo=photo)

@router.put("/body/{advert_id}")
async def update_body(
        advert_id: int,
        user: AdminDep,
        service: AdvertisingServiceDep,
        category_id: int = Form(...),
        title: str = Form(...),
        description: str = Form(...),
    ):
    return await service.update_body(ad_id=advert_id, title=title, description=description,category_id=category_id)

@router.delete("/{advert_id}")
async def delete(
        advert_id: int,
        user: AdminDep,
        service: AdvertisingServiceDep,
    ):
    await service.delete(advert_id)