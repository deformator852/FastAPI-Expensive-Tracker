from fastapi import APIRouter, Depends, HTTPException
from categories.service import CategoriesService
from database import SessionDep
from schemas.category import CreateCategory, UpdateCategory
from users.service import UsersService
from utilities.current_user import get_current_user

router = APIRouter(tags=["Routers"])
service = CategoriesService()
user_service = UsersService()


@router.get("/categories/{cat_id}")
async def get_category(
    cat_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        category = await service.get_category(current_user, cat_id, session)
        return {"status": True, "category": category}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.get("/categories")
async def get_categories(
    session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        categories = await service.get_categories(current_user, session)
        return {"status": True, "categories": categories}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.post("/categories")
async def create_category(
    category_data: CreateCategory,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):
    try:
        data = category_data.model_dump()
        category_name = data["category_name"]
        await service.create_category(current_user, category_name, session)
        return {"status": True}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.put("/categories/{cat_id}")
async def update_category(
    cat_id: int,
    update_data: UpdateCategory,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):
    data = update_data.model_dump()
    try:
        await service.update_category(
            current_user, data["category_name"], cat_id, session
        )
        return {"status": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")


@router.delete("/categories/{cat_id}")
async def delete_category(
    cat_id: int, session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        await service.delete_category(current_user, cat_id, session)
        return {"status": True}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"an unexpected error occured.{str(e)}")
