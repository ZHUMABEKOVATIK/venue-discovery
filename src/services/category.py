from src.repositories.category import CategoryRepo, SubCategoryRepo
from src.models.category import Category
from src.core import NotFoundException, BadRequestException

class CategoryService:
    def __init__(self, repo: CategoryRepo):
        self.repo = repo

    async def get_all(self) -> list[Category]:
        return await self.repo.get_all()

    async def create(self, name: str) -> Category:
        return await self.repo.create(
            Category(name = name.strip())
        )
    
    async def update(self, id: int, name: str) -> Category:
        data = await self.repo.update(id, name=name)
        if data is None:
            raise NotFoundException(f"Category with id {id} not found")
        return data
    
    async def delete(self, id: int) -> None:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise NotFoundException(f"Category with id {id} not found")
        await self.repo.delete(obj)

class SubCategoryService:
    def __init__(self, repo: SubCategoryRepo):
        self.repo = repo

    async def get_all(self, parent_id: int) -> list[Category]:
        return await self.repo.get_all(parent_id)

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
    
    async def update(self, category_id, id: int, name: str) -> Category:
        data = await self.repo.update(id, name=name)
        if data is None:
            raise NotFoundException(f"Category with id {id} not found")
        
        if data.parent_id is None:
            raise BadRequestException("It isn't Subcategory")
        
        if data.parent_id != category_id:
            raise BadRequestException("Wrong category id")

        return data
    
    async def delete(self, id: int) -> None:
        obj = await self.repo.get_by_id(id)
        if obj is None:
            raise NotFoundException(f"Subcategory with id {id} not found")
        await self.repo.delete(obj)