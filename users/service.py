from datetime import datetime, timedelta, timezone
from jose import jwt
from sqlalchemy import select
from models.models import User
from database import SessionDep
from fastapi import HTTPException
from dotenv import dotenv_values
import hashlib


class UsersService:
    def __init__(self):
        self.__SECRET: str = dotenv_values(".env")["SECRET"]  # pyright:ignore
        if self.__SECRET is None:
            raise ValueError()
        self.__ALGORITHM = "HS256"

    async def registration(
        self, user_data: dict[str, str], session: SessionDep
    ) -> tuple[str, str, int]:
        password = user_data["password"].encode("utf-8")
        hashed_password = hashlib.sha256(password).hexdigest()
        query = User(
            username=user_data["username"],
            email=user_data["email"],
            password=hashed_password,
        )
        session.add(query)
        await session.commit()
        result = await session.execute(select(User).filter_by(email=user_data["email"]))
        user = result.scalar_one_or_none()
        if user:
            access_token = self.generate_access_token({"user": user.id})
            refresh_token = self.generate_refresh_token({"user": user.id})
            return access_token, refresh_token, user.id
        raise HTTPException(status_code=404, detail="error with registration")

    def generate_access_token(self, payload: dict[str, int]) -> str:
        jwt_payload: dict[str, int | str] = {"user": payload["user"]}
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        jwt_payload.update({"exp": int(expire.timestamp())})
        encoded_jwt: str = jwt.encode(
            jwt_payload, self.__SECRET, algorithm=self.__ALGORITHM
        )
        return encoded_jwt

    def generate_refresh_token(self, payload: dict[str, int]) -> str:
        jwt_payload: dict[str, int | str] = {"user": payload["user"]}
        expire = datetime.now(timezone.utc) + timedelta(days=15)
        jwt_payload.update({"exp": int(expire.timestamp())})
        encoded_jwt: str = jwt.encode(
            jwt_payload, self.__SECRET, algorithm=self.__ALGORITHM
        )
        return encoded_jwt

    def verify_token(self, token: str) -> dict[str, str | int]:
        payload = jwt.decode(token, self.__SECRET, algorithms=[self.__ALGORITHM])
        return payload
