import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from core.configs import settings, DBBaseModel

# IMPORTANTE: importar TODOS os models antes do create_all
from models.user_model import User
from models.race_model import Race
from models.registration_model import Registration
from models.result_model import Result

async def create_tables():
    engine = create_async_engine(settings.DB_URL, echo=True)
    async with engine.begin() as conn:
        # Opcional: drop_all() apaga tudo antes (cuidado em produção!)
        await conn.run_sync(DBBaseModel.metadata.drop_all)
        await conn.run_sync(DBBaseModel.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
