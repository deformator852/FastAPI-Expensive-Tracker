from fastapi import APIRouter, Depends, HTTPException
from categories.service import CategoriesService
from database import SessionDep
from schemas.user import CreateCategory
from users.service import UsersService
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(tags=["Routers"])
service = CategoriesService()
user_service = UsersService()
security = HTTPBearer()


def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    user_id = user_service.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return user_id


@router.get("/categories")
async def get_categories(
    session: SessionDep, current_user: int = Depends(get_current_user)
):
    try:
        categories = await service.get_categories(current_user, session)
        return {"status": True, "categories": categories}
    except Exception as e:
        return HTTPException(404, f"Can't get categories.{e}")


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
    except Exception as e:
        raise HTTPException(404, f"Can't create category.E{str(e)}")


@router.put("/categories/{cat_id}")
async def update_category(cat_id: int, session: SessionDep):
    pass


@router.delete("/categories/{cat_id}")
async def delete_category(cat_id: int, session: SessionDep):
    pass
