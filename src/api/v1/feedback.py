from fastapi import APIRouter, status, Query
from src.dependencies import CurrentUserDep
from src.schemas.feedback import FeedbackIn, FeedbackOut, FeedbackUpdateIn
from src.dependencies import FeedbackServiceDep

router = APIRouter(prefix="/feedback", tags=["Feedbacks"])

@router.get("/", response_model=list[FeedbackOut])
async def get_all(
        user: CurrentUserDep, 
        service: FeedbackServiceDep,
        venue_id: int | None = Query(None),
        limit: int | None = Query(None),
        offset: int | None = Query(None)
    ):
    return await service.get_all(venue_id=venue_id, limit=limit, offset=offset)

@router.post("/", response_model=FeedbackOut)
async def create(
        payload: FeedbackIn, 
        user: CurrentUserDep, 
        service: FeedbackServiceDep
    ):
    return await service.create(
        venue_id=payload.venue_id,
        user_id=user.id,
        rating=payload.rating,
        review=payload.review
    )

@router.patch("/{feedback_id}", response_model=FeedbackOut)
async def update(
        feedback_id: int,
        payload: FeedbackUpdateIn,
        user: CurrentUserDep,
        service: FeedbackServiceDep
    ):
    return await service.update(
        id=feedback_id,
        user_id=user.id,
        rating=payload.rating,
        review=payload.review
    )

@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        feedback_id: int,
        user: CurrentUserDep,
        service: FeedbackServiceDep
    ):
    await service.delete(id=feedback_id, user_id=user.id)