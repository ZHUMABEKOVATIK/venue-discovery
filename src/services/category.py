from src.repositories.category import CategoryRepo, SubCategoryRepo
from src.models.category import Category
from src.core.exceptions import NotFoundException

class CategoryService:
    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def create(self, name: str) -> Category:
        return await self.repo.create(
            Category(name = name.strip())
        )
    
    async def delete(self, id: int) -> None:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise NotFoundException(f"Category with id {id} not found")
        await self.repo.delete(obj)

class SubCategoryService:
    def __init__(self, repo: SubCategoryRepo):
        self.repo = repo

    async def create(self, name: str, parent_id: int) -> Category:
        parent = await self.repo.parent_exists(parent_id)

        if not parent:
            raise NotFoundException(f"Category with id {parent_id} not found")
        
        return await self.repo.create(
            Category(
                name = name.strip(), 
                parent_id = parent_id
            )
        )
    
    async def delete(self, id: int) -> None:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise NotFoundException(f"Subcategory with id {id} not found")
        await self.repo.delete(obj)