from fastapi import APIRouter, UploadFile, File, Form, status
from src.dependencies import CurrentUserDep, AnnouncementServiceDep, AdminDep
from src.schemas.announcement import AnnouncementOut, AnnouncementGet
from src.models.model_enums import UserRole

router = APIRouter(prefix="/announcement")

@router.post("/", response_model=AnnouncementOut, status_code=201)
async def create(
    user: CurrentUserDep,
    service: AnnouncementServiceDep,
    photo: UploadFile = File(...),
    value: str = Form(...),
    description: str | None = Form(None),
):
    return await service.create(
        user_id=user.id,
        photo=photo,
        value=value,
        description=description,
    )

@router.post("/filter", response_model=list[AnnouncementOut], description="Userlerdi o'zi filterleydi, admin bolsa ba'ri, user bolsa tek o'ziniki")
async def get_all(
        payload: AnnouncementGet,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
    ):
    if user.role == UserRole.guest:
        return await service.get_all(
            user_id=user.id, 
            only_approved=payload.only_approved, 
            offset=payload.offset, 
            limit=payload.limit
        )
    else:
        return await service.get_all(
            only_approved=payload.only_approved, 
            offset=payload.offset, 
            limit=payload.limit
        )
    
@router.patch("/photo/{annons_id}", description="Fotosin o'zgertiw", response_model=AnnouncementOut)
async def update_photo(
        annons_id: int,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
        photo: UploadFile = File(...)
):
    return await service.update_photo(id=annons_id, user_id=user.id, photo=photo)
    
@router.put("/body/{annons_id}", description="Value ha'm description o'zgertiw", response_model=AnnouncementOut)
async def update(
        annons_id: int,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
        value: str | None = Form(...),
        description: str | None = Form(None),
    ):
    return await service.update_body(id=annons_id, user_id=user.id, value=value, description=description)

@router.patch("/approve/{annons_id}", response_model=AnnouncementOut)
async def approve_announcement(
        annons_id: int,
        user: AdminDep,
        service: AnnouncementServiceDep,
):
    return await service.approve_announcement(annons_id)

@router.patch("/reject/{annons_id}", response_model=AnnouncementOut)
async def reject_announcement(
        annons_id: int,
        user: AdminDep,
        service: AnnouncementServiceDep,
        comment: str = Form(...)
):
    return await service.rejected_announcement(annons_id=annons_id, comment=comment)

@router.patch("/revision/{annons_id}", response_model=AnnouncementOut)
async def revision_announcement(
        annons_id: int,
        user: AdminDep,
        service: AnnouncementServiceDep,
        comment: str = Form(...)
):
    return await service.revision_announcement(annons_id=annons_id, comment=comment)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        annons_id: int,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
    ):
    await service.delete(annons_id)