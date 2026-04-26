from sqlalchemy.exc import NoResultFound
from .base_repository import BaseRepository
from sqlalchemy import select

from src.models.category import Category

class CategoryRepo(BaseRepository[Category]):
    model = Category