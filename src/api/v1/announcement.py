from fastapi import APIRouter, UploadFile, File, Form, status, Query
from src.dependencies import CurrentUserDep, AnnouncementServiceDep, AdminDep
from src.schemas.announcement import AnnouncementOut, AnnouncementGet
from src.models.model_enums import UserRole
from src.core.exceptions import BadRequestException

router = APIRouter(prefix="/announcement", tags=["Announcements"])

@router.post("/", response_model=AnnouncementOut, status_code=201)
async def create(
    user: CurrentUserDep,
    service: AnnouncementServiceDep,
    photo: UploadFile = File(...),
    value: str = Form(...),
    description: str | None = Form(None),
):
    if user.role not in (UserRole.owner, UserRole.admin):
        raise BadRequestException("Tek owner anons qosa aladi")

    return await service.create(
        user_id=user.id,
        photo=photo,
        value=value,
        description=description,
    )

@router.get("/filter", response_model=list[AnnouncementOut], description="Only for guests!")
async def get_all_guests(
        service: AnnouncementServiceDep,
        offset: int | None = Query(None), 
        limit: int | None = Query(None)
    ):
    return await service.get_all(
        only_approved=True, 
        offset=offset, 
        limit=limit
    )

@router.post("/filter", response_model=list[AnnouncementOut], description="For owners or admins")
async def get_all_owners(
        payload: AnnouncementGet,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
    ):
    user_id = None

    if user.role == UserRole.guest:
        raise BadRequestException("This request can only be sent by admins or owners.")
    
    if user.role == UserRole.owner:
        user_id = user.id
    
    return await service.get_all(
        user_id=user_id,
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
        value: str | None = Form(None),
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

@router.delete("/{annons_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        annons_id: int,
        user: CurrentUserDep,
        service: AnnouncementServiceDep,
    ):
    is_admin = user.role == UserRole.admin
    await service.delete(id=annons_id, user_id=user.id, is_admin=is_admin)