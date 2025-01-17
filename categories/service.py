from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Category


class CategoriesService:
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
