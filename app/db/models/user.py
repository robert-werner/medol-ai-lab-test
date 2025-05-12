from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base


class User(Base):
    __tablename__ = 'user'


    id: Mapped[str] = mapped_column(primary_key=True)
    uri: Mapped[str] = mapped_column()
