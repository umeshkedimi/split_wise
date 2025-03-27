from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True)
    password: str

class User(UserBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expenses: List["Expense"] = Relationship(back_populates="user")
    groups: List["GroupMember"] = Relationship(back_populates="user")

class GroupBase(SQLModel):
    name: str
    description: Optional[str] = None

class Group(GroupBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    members: List["GroupMember"] = Relationship(back_populates="group")
    expenses: List["Expense"] = Relationship(back_populates="group")

class GroupMember(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    group_id: UUID = Field(foreign_key="group.id")
    user: User = Relationship(back_populates="groups")
    group: Group = Relationship(back_populates="members")

class ExpenseBase(SQLModel):
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)

class Expense(ExpenseBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    group_id: UUID = Field(foreign_key="group.id")
    user: User = Relationship(back_populates="expenses")
    group: Group = Relationship(back_populates="expenses")
    splits: List["ExpenseSplit"] = Relationship(back_populates="expense")

class ExpenseSplit(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    expense_id: UUID = Field(foreign_key="expense.id")
    user_id: UUID = Field(foreign_key="user.id")
    amount: float
    expense: Expense = Relationship(back_populates="splits") 