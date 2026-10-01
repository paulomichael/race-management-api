from typing import List
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.result_model import Result
from schemas.result_schema import ResultCreate, ResultResponse
from core.deps import get_session

router = APIRouter()

@router.post('/', response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(res: ResultCreate, db: AsyncSession = Depends(get_session)):
    new_res = Result(**res.model_dump())
    db.add(new_res)
    await db.commit()
    await db.refresh(new_res)
    return new_res

@router.get('/', response_model=List[ResultResponse])
async def get_results(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Result))
    return result.scalars().all()
