from src.db.sessions import async_session
from src.repositories.user import UserRepository
from src.models.user import User
from src.models.model_enums import UserRole
from src.core.security import hash_password

async def auto_create_admin() -> None: 
    async with async_session() as session:
        repo = UserRepository(session)
        exists = await repo.is_exists("admin@example.com")
        if not exists:
            admin = User(
                email="admin@example.com",
                hashed_pw=hash_password("admin123"),
                first_name="Admin",
                role=UserRole.admin,
            )
            session.add(admin)
            await session.commit()