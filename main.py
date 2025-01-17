from fastapi import FastAPI
from dotenv import load_dotenv
from database import setup_database
from users.controller import router as users_router
from categories.controller import router as categories_router
import uvicorn
import asyncio

load_dotenv()
app = FastAPI()
PREFIX = "/api"
app.include_router(router=users_router, prefix=PREFIX)
app.include_router(router=categories_router, prefix=PREFIX)


async def main():
    await setup_database()
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    asyncio.run(main())
