from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.orm.base import Base


class Token(Base):
    __tablename__ = "tokens"

    access_token: Mapped[str] = mapped_column(String(255), unique=True, primary_key=True)
    token_type: Mapped[str] = mapped_column(String(255))
