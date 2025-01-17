from pydantic import BaseModel, Field, EmailStr


class CreateUser(BaseModel):
    username: str = Field(max_length=200, min_length=3)
    email: EmailStr
    password: str = Field(max_length=255, min_length=8)


class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(max_length=255, min_length=8)


class CreateCategory(BaseModel):
    category_name: str = Field(max_length=255)
