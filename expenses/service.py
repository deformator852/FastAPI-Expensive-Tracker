from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Expense


class ExpensesService:
    async def get_expenses(self, user_id, session: AsyncSession):
        query = select(Expense).where(Expense.user_id == user_id)
        result = await session.execute(query)
        result = result.scalars().all()
        return result

    async def create_expense(self, data, user_id: int, session: AsyncSession) -> None:
        query = Expense(
            category_id=data["category_id"],
            name=data["name"],
            user_id=user_id,
            amount=data["amount"],
            date_expense=data["date_expense"],
        )
        session.add(query)
        await session.commit()
