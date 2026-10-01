from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.registration_model import Registration
from schemas.registration_schema import RegistrationCreate, RegistrationResponse
from core.deps import get_session

router = APIRouter()

@router.post('/', response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def create_registration(reg: RegistrationCreate, db: AsyncSession = Depends(get_session)):
    new_reg = Registration(**reg.model_dump())  # Pydantic V2
    db.add(new_reg)
    await db.commit()
    await db.refresh(new_reg)
    return new_reg

@router.get('/', response_model=List[RegistrationResponse])
async def get_registrations(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Registration))
    return result.scalars().all()
