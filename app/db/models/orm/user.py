from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.orm.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(255), unique=True, primary_key=True)
    password: Mapped[str] = mapped_column(String(255))
