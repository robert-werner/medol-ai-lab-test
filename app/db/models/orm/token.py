from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.db.models.orm.base import Base

class Token(Base):
    __tablename__ = "tokens"

    access_token: Mapped[str] = mapped_column(String(255), unique=True, primary_key=True)
    token_type: Mapped[str] = mapped_column(String(255))
