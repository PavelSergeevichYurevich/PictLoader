from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.models.image import Image
from app.models.user import User
from app.schemas.user import ImageHistory, UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, create_access_token, verify_password
from app.services.search.pexels import search_pexels
from app.services.search.base import SearchAuthError, SearchRateLimitError, SearchUpstreamError

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

@router.get('/{user_id}/images', response_model=List[ImageHistory])
async def get_history(user_id: int, db:AsyncSession = Depends(get_db)):
    stmnt = select(Image).where(Image.user_id == user_id).order_by(desc(Image.created_at))
    result = await db.execute(stmnt)
    images = result.scalars().all()
    return images

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    access_token = create_access_token(data={'sub': str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get('/test/pexels')
async def test_pexels(q: str = 'cat'):
    try:
        results = await search_pexels(q, limit = 5, page = 1)
    except SearchAuthError:
        raise HTTPException(status_code=502, detail='Pexels authentication error')
    except SearchRateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Pexels rate limit exceeded"
        )
    except SearchUpstreamError:
        raise HTTPException(
            status_code=503,
            detail="Pexels service unavailable"
        ) 
        
    return {'count': len(results), 'first': results[0].model_dump() if results else None}
        
    



    
    
    