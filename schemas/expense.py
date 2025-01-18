import datetime
from pydantic import BaseModel, Field


class CreateExpense(BaseModel):
    amount: float
    name: str = Field(max_length=255)
    date_expense: datetime.datetime
    category_id: int


class UpdateExpense(BaseModel):
    name: str | None = Field(max_length=255)
    amount: float | None = None
    date_expense: datetime.datetime | None = None
