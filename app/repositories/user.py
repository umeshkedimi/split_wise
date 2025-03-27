from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.models import User
from app.repositories.base import BaseRepository
from app.schemas.schemas import UserCreate

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_in: UserCreate) -> User:
        db_obj = User(
            name=user_in.name,
            email=user_in.email,
            password=user_in.password  # In production, hash the password
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_user_groups(self, user_id: str) -> List[dict]:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            return [{"id": group.id, "name": group.name} for group in user.groups]
        return [] 