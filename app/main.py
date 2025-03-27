from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_session
from app.repositories.user import UserRepository
from app.repositories.group import GroupRepository
from app.repositories.expense import ExpenseRepository
from app.schemas.schemas import (
    UserCreate, UserResponse,
    GroupCreate, GroupResponse,
    ExpenseCreate, ExpenseResponse
)
from typing import List
from uuid import UUID

app = FastAPI(title="SplitWise API")

# User endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    db_user = await repo.get_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await repo.create(user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = UserRepository(session)
    user = await repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Group endpoints
@app.post("/groups/", response_model=GroupResponse)
async def create_group(
    group: GroupCreate,
    member_ids: List[UUID],
    session: AsyncSession = Depends(get_session)
):
    repo = GroupRepository(session)
    return await repo.create_group_with_members(group, member_ids)

@app.get("/groups/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = GroupRepository(session)
    group = await repo.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

# Expense endpoints
@app.post("/expenses/", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = ExpenseRepository(session)
    return await repo.create_expense_with_splits(expense, user_id)

@app.get("/expenses/group/{group_id}", response_model=List[ExpenseResponse])
async def get_group_expenses(
    group_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = ExpenseRepository(session)
    return await repo.get_group_expenses(group_id)

@app.get("/expenses/user/{user_id}", response_model=List[ExpenseResponse])
async def get_user_expenses(
    user_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = ExpenseRepository(session)
    return await repo.get_user_expenses(user_id)

@app.get("/balance/{user_id}/{group_id}")
async def get_user_balance(
    user_id: UUID,
    group_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    repo = ExpenseRepository(session)
    balance = await repo.get_user_balance(user_id, group_id)
    return {"balance": balance} 