from src.repositories.feedback import FeedbackRepo
from src.models.feedback import Feedback
from src.core.exceptions import BadRequestException, NotFoundException

class FeedbackService:
    def __init__(self, repo: FeedbackRepo):
        self.repo = repo

    async def create(self, venue_id: int, user_id: int, rating: int, review: str) -> Feedback:
        obj = Feedback(
            venue_id=venue_id,
            user_id=user_id,
            rating=rating,
            review=review
        )
        return await self.repo.create(obj)
    
    async def get_all(self, *, venue_id: int | None = None, offset: int | None = None, limit: int | None = None) -> list[Feedback]:
        return await self.repo.get_all(
            venue_id=venue_id,
            offset=offset,
            limit=limit
        )
    
    async def update(self, *, id: int, user_id: int | None = None, rating: int, review: str) -> Feedback:
        data = await self.repo.get_by_id(id)

        if data is None:
            raise NotFoundException("Feedback not found")
        
        if user_id is not None and data.user_id != user_id:
            raise BadRequestException("Bul sizge tiyisli emes")
        
        updates = {}
        if rating is not None:
            updates["rating"] = rating
        if review is not None:
            updates["review"] = review
        
        return await self.repo.update(id, **updates)

    async def delete(self, *, id: int, user_id: int | None = None) -> None:
        data = await self.repo.get_by_id(id)

        if data is None:
            raise NotFoundException("Feedback not found")
        
        if user_id is not None and data.user_id != user_id:
            raise BadRequestException("Bul sizge tiyisli emes")
        
        await self.repo.delete(data)
        
