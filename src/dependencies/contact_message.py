from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.contact_message import ContactMessageRepo
from src.services.contact_message import ContactMessageService

def get_contact_message_repo(session: AsyncSession = Depends(get_async_session)) -> ContactMessageRepo:
    return ContactMessageRepo(session)

def get_contact_message_service(repo: ContactMessageRepo = Depends(get_contact_message_repo)) -> ContactMessageService:
    return ContactMessageService(repo)
