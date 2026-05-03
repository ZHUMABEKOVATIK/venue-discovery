from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.feedback import FeedbackRepo
from src.services.feedback import FeedbackService

def get_feedback_repo(session: AsyncSession = Depends(get_async_session)) -> FeedbackRepo:
    return FeedbackRepo(session)

def get_feedback_service(repo: FeedbackRepo = Depends(get_feedback_repo)) -> FeedbackService:
    return FeedbackService(repo)