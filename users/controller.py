from fastapi import APIRouter, HTTPException, Request, Response
from models.models import User
from schemas.user import CreateUser, LoginUser
from database import SessionDep
from sqlalchemy.sql import select

from utilities.cookieManager import CookieManager
from .service import UsersService

router = APIRouter(tags=["Users"])
service = UsersService()


@router.post("/register")
async def register(user_data: CreateUser, session: SessionDep, response: Response):
    access_token, refresh_token = await service.registration(
        user_data.model_dump(), session
    )
    CookieManager.set_refresh_token(response, refresh_token)
    return {"status": True, "access_token": access_token}


@router.post("/login")
async def login(user_data: LoginUser, session: SessionDep, response: Response):
    data = user_data.model_dump()
    email = data["email"]
    password = data["password"]
    hashed_password = service.hash_password(password)
    result = await session.execute(
        select(User).filter(User.email == email, User.password == hashed_password)
    )
    user = result.scalar()
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"Can't find user with email {email}"
        )
    payload = {"user": user.id}
    access_token = service.generate_access_token(payload)
    refresh_token = service.generate_refresh_token(payload)
    CookieManager.set_refresh_token(response, refresh_token)
    return {"status": True, "access_token": access_token}


@router.get("/logout")
async def logout(request: Request, response: Response):
    refresh_token = request.cookies.get("inventory_app_refresh")
    if not refresh_token:
        raise HTTPException(status_code=404, detail="You've been already logout")
    CookieManager.delete_refresh_token(response)
    response.delete_cookie(key="inventory_app_refresh")
    return {"status": True}


@router.get("/refresh")
async def refresh(request: Request):
    refresh_token = CookieManager.get_refresh_token(request)
    if not refresh_token:
        raise HTTPException(status_code=404, detail="Empty refresh token")
    try:
        user_id = service.verify_token(refresh_token)
        if user_id:
            new_access_token = service.generate_access_token({"user": int(user_id)})
            return {"status": True, "access_token": new_access_token}
        raise HTTPException(404, detail="Not valid access token")
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"can't refresh access token.Error text:{str(e)}"
        )
