from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from fastapi import Depends


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


async def setup_database():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost/inventory"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)
SessionDep = Annotated[AsyncSession, Depends(get_session)]
