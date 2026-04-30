from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.category import CategoryRepo, SubCategoryRepo
from src.services.category import CategoryService, SubCategoryService

def get_category_repo(session: AsyncSession = Depends(get_async_session)) -> CategoryRepo:
    return CategoryRepo(session)

def get_category_service(repo: CategoryRepo = Depends(get_category_repo)) -> CategoryService:
    return CategoryService(repo)

def get_subcategory_repo(session: AsyncSession = Depends(get_async_session)) -> SubCategoryRepo:
    return SubCategoryRepo(session)

def get_subcategory_service(repo: SubCategoryRepo = Depends(get_subcategory_repo)) -> SubCategoryService:
    return SubCategoryService(repo)