from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse
from core.deps import get_session

router = APIRouter()

# Configuração do Hash (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    query = select(User).filter(User.email == user.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(detail="Email já cadastrado", status_code=status.HTTP_400_BAD_REQUEST)
    
    # HASH DA SENHA AQUI (Requisito do PDF)
    hashed_password = pwd_context.hash(user.password)
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,  # Salva o hash, não a senha pura
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get('/', response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get('/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    return user
