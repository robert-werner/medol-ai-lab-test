from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.orm.base import Base

class FileInfo(Base):
    
    __tablename__ = 'file_info'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    uri: Mapped[str] = mapped_column()
