from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.models import Expense, ExpenseSplit
from app.repositories.base import BaseRepository
from app.schemas.schemas import ExpenseCreate

class ExpenseRepository(BaseRepository[Expense]):
    def __init__(self, session: AsyncSession):
        super().__init__(Expense, session)

    async def create_expense_with_splits(self, expense_in: ExpenseCreate, user_id: str) -> Expense:
        # Create the expense
        db_expense = Expense(
            description=expense_in.description,
            amount=expense_in.amount,
            date=expense_in.date,
            user_id=user_id,
            group_id=expense_in.group_id
        )
        self.session.add(db_expense)
        await self.session.commit()
        await self.session.refresh(db_expense)

        # Create splits
        for split in expense_in.splits:
            expense_split = ExpenseSplit(
                expense_id=db_expense.id,
                user_id=split["user_id"],
                amount=split["amount"]
            )
            self.session.add(expense_split)

        await self.session.commit()
        return db_expense

    async def get_group_expenses(self, group_id: str) -> List[Expense]:
        query = select(Expense).where(Expense.group_id == group_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_expenses(self, user_id: str) -> List[Expense]:
        query = select(Expense).where(Expense.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_user_balance(self, user_id: str, group_id: str) -> float:
        # Get all expenses where user is the payer
        query = select(Expense).where(
            Expense.user_id == user_id,
            Expense.group_id == group_id
        )
        result = await self.session.execute(query)
        paid_expenses = result.scalars().all()

        # Get all splits where user is involved
        query = select(ExpenseSplit).join(Expense).where(
            Expense.group_id == group_id,
            ExpenseSplit.user_id == user_id
        )
        result = await self.session.execute(query)
        splits = result.scalars().all()

        # Calculate balance
        total_paid = sum(expense.amount for expense in paid_expenses)
        total_share = sum(split.amount for split in splits)
        
        return total_paid - total_share 