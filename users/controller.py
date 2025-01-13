from fastapi import APIRouter, HTTPException, Request, Response
from models.models import User
from schemas.user import CreateUser, LoginUser
from database import SessionDep
from sqlalchemy.sql import select
from .service import UsersService

router = APIRouter(tags=["Users"])
service = UsersService()


@router.post("/register/")
async def register(
    request: Request, user_data: CreateUser, session: SessionDep, response: Response
):
    access_token, refresh_token, user_id = await service.registration(
        user_data.model_dump(), session
    )
    response.set_cookie(
        key="inventory_app_refresh", value=refresh_token, httponly=True, max_age=900
    )
    request.session["user"] = user_id
    return {"status": True, "access_token": access_token}


@router.post("/login/")
async def login(
    request: Request, user_data: LoginUser, session: SessionDep, response: Response
):
    data = user_data.model_dump()
    result = await session.execute(select(User).filter(User.email == data["email"]))
    user = result.scalar()
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"Can't find user with email {data['email']}"
        )
    payload = {"user": user.id}
    request.session["user"] = user.id
    access_token = service.generate_access_token(payload)
    refresh_token = service.generate_refresh_token(payload)
    response.set_cookie(
        key="inventory_app_refresh", value=refresh_token, httponly=True, max_age=900
    )
    return {"status": True, "access_token": access_token}


@router.get("/logout/")
async def logout(request: Request, response: Response):
    refresh_token = request.cookies.get("inventory_app_refresh")
    if not refresh_token:
        raise HTTPException(status_code=404, detail="You've been already logout")
    response.delete_cookie(key="inventory_app_refresh")
    return {"status": True}


@router.get("/refresh/")
async def refresh(request: Request):
    refresh_token: str | None = request.cookies.get("inventory_app_refresh")
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Empty refresh token")
    try:
        service.verify_token(refresh_token)
        return {"status": True}
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"can't refresh access token.Error text:{str(e)}"
        )
