from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, DECIMAL, Text, ForeignKey
from core.configs import settings, DBBaseModel
from typing import Optional
from datetime import date

class Race(DBBaseModel):
    __tablename__ = 'races'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    distance: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    # Relacionamento (vamos implementar depois)
    # organizer: Mapped["User"] = relationship(back_populates="races")
