from pydantic import BaseModel, Field


class CreateCategory(BaseModel):
    category_name: str = Field(max_length=255)


class UpdateCategory(CreateCategory):
    pass
