from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Category, Expense


class ExpensesService:
    async def get_expenses_by_amount(
        self,
        user_id: int,
        session: AsyncSession,
        min_amount: float | None = None,
        max_amount: float | None = None,
    ):
        operation = []
        if min_amount is not None:
            query = select(Expense).where(
                Expense.user_id == user_id, Expense.amount >= min_amount
            )
            operation.append(query)
        if max_amount is not None:
            query = select(Expense).where(
                Expense.user_id == user_id, Expense.amount <= max_amount
            )
            operation.append(query)
        result = await session.execute(operation[0])
        return result.scalars().all()

    async def get_expenses_by_category(
        self, user_id: int, cat_id: int, session: AsyncSession
    ):
        query = select(Expense).where(
            Expense.user_id == user_id, Expense.category_id == cat_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_expense_by_id(
        self, user_id: int, expense_id: int, session: AsyncSession
    ):
        query = select(Expense).where(
            Expense.user_id == user_id, Expense.id == expense_id
        )
        result = await session.execute(query)
        expense = result.scalar_one_or_none()
        if expense is None:
            raise HTTPException(404, "can't find expense")
        return expense

    async def delete_expense(
        self, user_id: int, expense_id: int, session: AsyncSession
    ):
        query = delete(Expense).where(
            Expense.user_id == user_id, Expense.id == expense_id
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(404, "can't delete expense")
        await session.commit()

    async def update_expense(
        self, user_id: int, expense_id: int, data, session: AsyncSession
    ):
        query = (
            update(Expense)
            .where(Expense.user_id == user_id, Expense.id == expense_id)
            .values(data)
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(404, "can't update expense")
        await session.commit()

    async def get_expenses_by_date(
        self,
        user_id: int,
        session: AsyncSession,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        operation = []
        if date_to is not None:
            query = select(Expense).filter(
                Expense.user_id == user_id, Expense.date_expense <= date_to
            )
            operation.append(query)
        if date_from is not None:
            query = select(Expense).filter(
                Expense.user_id == user_id, Expense.date_expense >= date_from
            )
            operation.append(query)

        result = await session.execute(operation[0])
        return result.scalars().all()

    async def get_expenses(self, user_id, session: AsyncSession):
        query = select(Expense).where(Expense.user_id == user_id)
        result = await session.execute(query)
        result = result.scalars().all()
        return result

    async def create_expense(self, data, user_id: int, session: AsyncSession) -> None:
        result = await session.execute(
            select(Category).filter_by(id=data["category_id"], user_id=user_id)
        )
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                404,
                f"User with ID {user_id} does not have category with ID {data['category_id']}",
            )
        query = Expense(
            category_id=data["category_id"],
            name=data["name"],
            user_id=user_id,
            amount=data["amount"],
            date_expense=data["date_expense"],
        )
        session.add(query)
        await session.commit()
