from src.repositories.user import UserRepository
from src.models.user import User
from src.core.exceptions import NotFoundException


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_by_id(self, _id: int) -> User:
        user = await self.repo.get_one(_id=_id)
        if user is None:
            raise NotFoundException("пользователь не найден")
        return user

    async def delete(self, _id: int) -> None:
        deleted = await self.repo.delete(_id)
        if not deleted:
            raise NotFoundException("пользователь не найден")