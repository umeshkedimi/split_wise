from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.models import Group, GroupMember
from app.repositories.base import BaseRepository
from app.schemas.schemas import GroupCreate

class GroupRepository(BaseRepository[Group]):
    def __init__(self, session: AsyncSession):
        super().__init__(Group, session)

    async def create_group_with_members(self, group_in: GroupCreate, member_ids: List[str]) -> Group:
        # Create the group
        db_group = Group(
            name=group_in.name,
            description=group_in.description
        )
        self.session.add(db_group)
        await self.session.commit()
        await self.session.refresh(db_group)

        # Add members
        for member_id in member_ids:
            group_member = GroupMember(
                group_id=db_group.id,
                user_id=member_id
            )
            self.session.add(group_member)

        await self.session.commit()
        return db_group

    async def get_group_members(self, group_id: str) -> List[dict]:
        query = select(GroupMember).where(GroupMember.group_id == group_id)
        result = await self.session.execute(query)
        members = result.scalars().all()
        return [{"id": member.user_id} for member in members]

    async def add_member(self, group_id: str, user_id: str) -> bool:
        # Check if member already exists
        query = select(GroupMember).where(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        )
        result = await self.session.execute(query)
        if result.scalar_one_or_none():
            return False

        group_member = GroupMember(
            group_id=group_id,
            user_id=user_id
        )
        self.session.add(group_member)
        await self.session.commit()
        return True 