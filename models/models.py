from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
