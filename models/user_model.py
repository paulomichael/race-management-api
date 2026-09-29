from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
from core.configs import settings, DBBaseModel
import enum

# 1. Definimos o ENUM como uma classe Python nativa (melhor que string solta)
class RoleEnum(str, enum.Enum):
    corredor = "corredor"
    organizador = "organizador"

class User(DBBaseModel):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, default=RoleEnum.corredor)
