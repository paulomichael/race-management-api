from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Time, ForeignKey
from core.configs import DBBaseModel
from typing import Optional
from datetime import time as TimeType

class Result(DBBaseModel):
    __tablename__ = 'results'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    race_id: Mapped[int] = mapped_column(ForeignKey('races.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    finish_time: Mapped[Optional[TimeType]] = mapped_column(Time, nullable=True)
