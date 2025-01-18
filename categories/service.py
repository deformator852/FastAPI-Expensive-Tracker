from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Category


class CategoriesService:
    async def get_category(self, user_id: int, category_id: int, session: AsyncSession):
        query = select(Category).where(
            Category.user_id == user_id, Category.id == category_id
        )
        result = await session.execute(query)
        category = result.scalar_one_or_none()
        if category is None:
            raise HTTPException(404, "can't find the such category")
        return category

    async def get_categories(self, user_id, session: AsyncSession):
        query = select(Category).where(Category.user_id == user_id)
        result = await session.execute(query)
        categories = result.scalars().all()
        return categories

    async def create_category(
        self, user_id: int, category_name: str, session: AsyncSession
    ) -> None:
        query = Category(category_name=category_name, user_id=user_id)
        session.add(query)
        await session.commit()

    async def update_category(
        self, user_id: int, category_name: str, category_id: int, session: AsyncSession
    ) -> None:
        query = (
            update(Category)
            .where(Category.user_id == user_id, Category.id == category_id)
            .values(category_name=category_name)
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(404, "category not updated")
        await session.commit()

    async def delete_category(
        self, user_id: int, category_id: int, session: AsyncSession
    ) -> None:
        query = delete(Category).where(
            Category.user_id == user_id, Category.id == category_id
        )
        result = await session.execute(query)
        if result.rowcount == 0:
            raise HTTPException(404, "category not found")
        await session.commit()
