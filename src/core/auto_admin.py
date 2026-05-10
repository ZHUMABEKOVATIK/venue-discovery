from src.db.sessions import async_session
from src.repositories.user import UserRepository
from src.models.user import User
from src.models.model_enums import UserRole
from src.core.security import hash_password
from .config import settings

async def auto_create_admin() -> None: 
    async with async_session() as session:
        repo = UserRepository(session)
        exists = await repo.is_exists(settings.DEFAULT_ADMIN_EMAIL)
        if not exists:
            admin = User(
                email=settings.DEFAULT_ADMIN_EMAIL,
                hashed_pw=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
                first_name="Admin",
                role=UserRole.admin,
            )
            session.add(admin)
            await session.commit()