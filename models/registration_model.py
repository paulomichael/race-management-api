from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Enum, Time, ForeignKey
from core.configs import DBBaseModel
import enum
from typing import Optional
from datetime import time as TimeType


class StatusEnum(str, enum.Enum):
    inscrito = "inscrito"
    cancelado = "cancelado"


class Registration(DBBaseModel):
    __tablename__ = 'registrations'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    race_id: Mapped[int] = mapped_column(ForeignKey('races.id'), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False, default=StatusEnum.inscrito)
    time: Mapped[Optional[TimeType]] = mapped_column(Time, nullable=True)
