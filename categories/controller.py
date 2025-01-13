from fastapi import APIRouter, Depends, HTTPException
from categories.service import CategoriesService
from database import SessionDep
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    token = token.split(" ")[1]
    payload = jwt.decode(token, "SADSADADADADDADSADMASDA", algorithms=["HS256"])
    user_id = payload.get("user")
    if user_id is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return user_id


router = APIRouter(tags=["Routers"])
service = CategoriesService()


@router.get("/categories")
async def get_categories(
    session: SessionDep, current_user: str = Depends(get_current_user)
):
    return {"status": "GOOD"}


@router.post("/categories")
async def create_category(session: SessionDep):
    pass


@router.put("/categories/{cat_id}")
async def update_category(cat_id: int, session: SessionDep):
    pass


@router.delete("/categories/{cat_id}")
async def delete_category(cat_id: int, session: SessionDep):
    pass
