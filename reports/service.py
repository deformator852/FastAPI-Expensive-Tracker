import csv
from datetime import datetime, timedelta
from io import StringIO
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Category, Expense


class ReportsService:
    def write_report_in_csv(self, report: list):
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=list(report[0].keys()),
        )
        writer.writeheader()
        writer.writerows(report)
        output.seek(0)
        return output

    async def get_report(self, session: AsyncSession, user_id: int, **time_period):
        categories_query = (
            select(Expense.category_id)
            .where(Expense.user_id == user_id)
            .group_by(Expense.category_id)
        )
        result = await session.execute(categories_query)
        categories = result.fetchall()
        data_for_user = []
        current_date = datetime.now().replace(tzinfo=None)
        date = current_date - timedelta(**time_period)
        date = date.replace(tzinfo=None)
        for category in categories:
            query = (
                select(
                    Category.category_name.label("category_name"),
                    func.max(Expense.amount),
                    func.min(Expense.amount),
                    func.sum(Expense.amount),
                    func.count(Expense.id),
                )
                .filter(
                    Expense.user_id == user_id,
                    Expense.category_id == category[0],
                    Expense.date_expense.between(date, current_date),
                )
                .group_by(Category.category_name)
                .join(Category, Category.id == Expense.category_id)
            )
            result = await session.execute(query)
            expensies_by_category = result.fetchall()
            for expense in expensies_by_category:
                data_for_user.append(
                    {
                        "category_name": expense[0],
                        "max_expense": expense[1],
                        "min_expense": expense[2],
                        "summary": expense[3],
                        "expenses_count": expense[4],
                    }
                )
        return data_for_user

    async def get_report_by_category(
        self, session: AsyncSession, user_id: int, category_id: int
    ):
        query = (
            select(
                Category.category_name.label("category_name"),
                func.sum(Expense.amount).label("summary"),
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
        summary_report = {}
        if not report:
            return {}
        report = report.tuple()
        summary_report["category_name"] = report[0]
        summary_report["summary"] = report[1]
        summary_report["expenses_count"] = report[2]
        summary_report["max_expense"] = report[3]
        summary_report["max_expense_id"] = report[4]
        summary_report["min_expense"] = report[5]
        summary_report["min_expense_id"] = report[6]
        return summary_report
