from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.race_model import Race
from schemas.race_schema import RaceCreate, RaceResponse
from core.deps import get_session

router = APIRouter()

# POST - Criar corrida
@router.post('/', response_model=RaceResponse, status_code=status.HTTP_201_CREATED)
async def create_race(race: RaceCreate, db: AsyncSession = Depends(get_session)):
    new_race = Race(
        name=race.name,
        date=race.date,
        location=race.location,
        distance=race.distance,
        description=race.description,
        organizer_id=race.organizer_id
    )
    db.add(new_race)
    await db.commit()
    await db.refresh(new_race)
    return new_race

# GET - Listar todas as corridas
@router.get('/', response_model=List[RaceResponse])
async def get_races(db: AsyncSession = Depends(get_session)):
    query = select(Race)
    result = await db.execute(query)
    races = result.scalars().all()
    return races

# GET - Obter corrida específica
@router.get('/{race_id}', response_model=RaceResponse, status_code=status.HTTP_200_OK)
async def get_race(race_id: int, db: AsyncSession = Depends(get_session)):
    query = select(Race).filter(Race.id == race_id)
    result = await db.execute(query)
    race = result.scalar_one_or_none()
    
    if race is None:
        raise HTTPException(
            detail='Corrida não encontrada',
            status_code=status.HTTP_404_NOT_FOUND
        )
    return race

# PUT - Atualizar corrida
@router.put('/{race_id}', response_model=RaceResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_race(race_id: int, race: RaceCreate, db: AsyncSession = Depends(get_session)):
    query = select(Race).filter(Race.id == race_id)
    result = await db.execute(query)
    race_up = result.scalar_one_or_none()
    
    if race_up is None:
        raise HTTPException(
            detail='Corrida não encontrada',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    race_up.name = race.name
    race_up.date = race.date
    race_up.location = race.location
    race_up.distance = race.distance
    race_up.description = race.description
    race_up.organizer_id = race.organizer_id
    
    await db.commit()
    await db.refresh(race_up)
    return race_up

# DELETE - Remover corrida
@router.delete('/{race_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_race(race_id: int, db: AsyncSession = Depends(get_session)):
    query = select(Race).filter(Race.id == race_id)
    result = await db.execute(query)
    race_del = result.scalar_one_or_none()
    
    if race_del is None:
        raise HTTPException(
            detail='Corrida não encontrada',
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    await db.delete(race_del)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
