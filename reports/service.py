from sqlalchemy import func, label, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Category, Expense


class ReportsService:
    async def get_expenses_by_category(
        self, session: AsyncSession, user_id: int, category_id: int
    ):
        query = (
            select(
                Category.category_name.label("category_name"),
                func.sum(Expense.amount).label("total_amount"),
                func.count(Expense.id).label("expenses_count"),
                func.max(Expense.amount).label("max_expense"),
                select(Expense.id)
                .where(
                    Expense.user_id == user_id,
                    Expense.category_id == category_id,
                )
                .order_by(Expense.amount.desc())
                .limit(1)
                .label("max_expense_id"),
                func.min(Expense.amount).label("min_expense"),
                select(Expense.id)
                .where(
                    Expense.user_id == user_id,
                    Expense.category_id == category_id,
                )
                .order_by(Expense.amount)
                .limit(1)
                .label("min_expense_id"),
            )
            .join(Category, Category.id == Expense.category_id)
            .where(Expense.user_id == user_id, Expense.category_id == category_id)
            .group_by(Category.category_name)
        )
        result = await session.execute(query)
        report = result.fetchone()
        summary_report = {
            "category_name": "",
            "total_amount": 0,
            "expenses_count": 0,
            "max_expense": 0,
            "max_expense_id": 0,
            "min_expense": 0,
            "min_expense_id": 0,
        }
        if not report:
            return summary_report
        report = report.tuple()
        summary_report["category_name"] = report[0]
        summary_report["total_amount"] = report[1]
        summary_report["expenses_count"] = report[2]
        summary_report["max_expense"] = report[3]
        summary_report["max_expense_id"] = report[4]
        summary_report["min_expense"] = report[5]
        summary_report["min_expense_id"] = report[6]
        return summary_report
