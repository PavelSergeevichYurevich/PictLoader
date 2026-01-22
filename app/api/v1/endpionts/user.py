from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('/register', response_model=UserResponse)
async def register_user(user_in: UserCreate, db:AsyncSession = (Depends(get_db))):
    
    query = select(User).where(User.username == user_in.username)
    result = await db.execute(query)
    
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail='User already exists'
        )

    new_user = User(
        username = user_in.username,
        hashed_password = hash_password(user_in.password)
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


    
    
    