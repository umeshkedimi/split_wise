from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: UUID
    created_at: datetime
    members: List[UserResponse]

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    description: str
    amount: float
    date: Optional[datetime] = None

class ExpenseCreate(ExpenseBase):
    group_id: UUID
    splits: List[dict]  # List of user_id and amount pairs

class ExpenseResponse(ExpenseBase):
    id: UUID
    user_id: UUID
    group_id: UUID
    splits: List[dict]

    class Config:
        from_attributes = True

class ExpenseSplitBase(BaseModel):
    user_id: UUID
    amount: float

class ExpenseSplitCreate(ExpenseSplitBase):
    expense_id: UUID

class ExpenseSplitResponse(ExpenseSplitBase):
    id: UUID
    expense_id: UUID

    class Config:
        from_attributes = True 