from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_async_session
from src.repositories.venue import VenueRepo
from src.services.venue import VenueService
from src.repositories.visits import VisitRepo

def get_venue_repo(session: AsyncSession = Depends(get_async_session)) -> VenueRepo:
    return VenueRepo(session)

def get_visit_repo(session: AsyncSession = Depends(get_async_session)) -> VisitRepo:
    return VisitRepo(session)

def get_venue_service(
    venue_repo: VenueRepo = Depends(get_venue_repo),
    visit_repo: VisitRepo = Depends(get_visit_repo),
) -> VenueService:
    return VenueService(venue_repo=venue_repo, visit_repo=visit_repo)