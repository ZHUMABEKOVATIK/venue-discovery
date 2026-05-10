from fastapi import APIRouter, status
from src.dependencies import AdminDep
from src.schemas.category import CategoryIn, CategoryOut 
from src.dependencies import CategoryServiceDep, SubCategoryServiceDep

router = APIRouter(prefix="/categories", tags=["Categories"])

# ── Категории ──
@router.get("/", response_model=list[CategoryOut])
async def get_categories(service: CategoryServiceDep):
    return await service.get_all()

@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryIn, user: AdminDep, service: CategoryServiceDep):
    return await service.create(payload.name)

@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, payload: CategoryIn, user: AdminDep, service: CategoryServiceDep):
    return await service.update(category_id, payload.name)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, user: AdminDep, service: CategoryServiceDep):
    await service.delete(category_id)

# ── Подкатегории ──
@router.get("/{category_id}/subcategories", response_model=list[CategoryOut])
async def get_subcategories(category_id: int, service: SubCategoryServiceDep):
    return await service.get_all(category_id)

@router.post("/{category_id}/subcategories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_subcategory(category_id: int, payload: CategoryIn, user: AdminDep, service: SubCategoryServiceDep):
    return await service.create(payload.name, category_id)

@router.patch("/{category_id}/subcategories/{subcategory_id}", response_model=CategoryOut)
async def update_subcategory(category_id: int, subcategory_id: int, payload: CategoryIn, user: AdminDep, service: SubCategoryServiceDep):
    return await service.update(category_id, subcategory_id, payload.name)

@router.delete("/{category_id}/subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subcategory(category_id: int, subcategory_id: int, user: AdminDep, service: SubCategoryServiceDep):
    await service.delete(subcategory_id)