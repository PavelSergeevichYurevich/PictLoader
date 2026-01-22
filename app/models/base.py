from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created_at:Mapped[datetime] = mapped_column(server_default=func.now(), comment='Дата и время создания записи')