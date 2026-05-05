from src.repositories.user import UserRepository
from src.models.user import User
from src.schemas.user import UserUpdateRequest
from src.core import NotFoundException


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_me(self, user_id: int) -> User:
        user = await self.repo.get_one(_id=user_id)
        if user is None:
            raise NotFoundException("Foydalanuvchi topilmadi")
        return user

    async def update_me(self, user_id: int, payload: UserUpdateRequest) -> User:
        data = payload.model_dump(exclude_none=True)
        user = await self.repo.update(user_id, **data)
        if user is None:
            raise NotFoundException("Foydalanuvchi topilmadi")
        return user

    async def delete_me(self, user_id: int) -> None:
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise NotFoundException("Foydalanuvchi topilmadi")
