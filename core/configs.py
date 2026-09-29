from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Settings(BaseSettings):
    # 1. Dados de conexão (lê do .env automaticamente)
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/corrida"
    
    # 2. Classe base para os models
    class Config:
        env_file = ".env"

# Instância única (singleton)
settings = Settings()

# 3. A DBBaseModel propriamente dita
class DBBaseModel(AsyncAttrs, DeclarativeBase):
    pass
