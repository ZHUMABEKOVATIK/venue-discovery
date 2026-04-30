from fastapi import APIRouter, status
from src.dependencies import AdminDep
from src.schemas.region import RegionIn, RegionOut
from src.dependencies import RegionServiceDep

router = APIRouter(prefix="/region", tags=["Regions"])

@router.get("/", response_model=list[RegionOut])
async def get_regions(service: RegionServiceDep):
    return await service.get_all()

@router.post("/", response_model=RegionOut)
async def create_region(payload: RegionIn, user: AdminDep, service: RegionServiceDep):
    return await service.create(payload.name)

@router.patch("/{region_id}", response_model=RegionOut)
async def update_region(region_id: int, payload: RegionIn, user: AdminDep, service: RegionServiceDep):
    return await service.update(region_id, payload.name)

@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(region_id: int, service: RegionServiceDep, user: AdminDep):
    await service.delete(region_id)