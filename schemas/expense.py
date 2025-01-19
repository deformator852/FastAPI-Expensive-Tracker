import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CreateExpense(BaseModel):
    amount: float
    name: str = Field(max_length=255)
    date_expense: datetime.datetime
    category_id: int


class UpdateExpense(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    amount: Optional[float] = None
    date_expense: Optional[datetime.datetime] = None
