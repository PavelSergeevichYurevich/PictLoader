import asyncio
import os
from pathlib import Path
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.settings import settings
from app.models.image import Image
from app.models.user import User
from app.services.downloader import download_image

router = APIRouter()

@router.get('/files')
async def lisf_files():
    files = []
    if settings.STORAGE_DIR.exists():
        files = [f.name for f in settings.STORAGE_DIR.iterdir() if f.is_file()]
        
    return {
        'storage_path': str(settings.STORAGE_DIR),
        'files': files
    }
    
@router.post('/download')
async def download_by_url(urls: List[str], 
                          current_user: User = Depends(get_current_user),
                          db:AsyncSession = Depends(get_db)):
   try:
        user_folder = settings.STORAGE_DIR / f'user{current_user.id}'
        user_folder.mkdir(parents=True, exist_ok=True)
        tasks:list = []
        for u in urls:
            url_path = Path(u)
            ext = url_path.suffix if len(url_path.suffix) <= 5 else '.jpg'
            random_name = f'{uuid.uuid4()}{ext}'
            full_path = user_folder / random_name
            tasks.append(download_image(u, full_path))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
           
        fls:dict = {}
        for i, res_path in enumerate(results):
            if isinstance(res_path, Path):
                new_img = Image(
                    filename = res_path.name,
                    source_url = urls[i],
                    path = str(res_path),
                    user_id = current_user.id
                )
                db.add(new_img)
                fls[res_path.name] = str(res_path)
            else:
                fls[urls[i]] = f'Error: {str(res_path)}'
        await db.commit()

        return {
            'status': 'success',
            'files': fls
        }
   except Exception as e:
       raise HTTPException(status_code=400, detail=f"Критическая ошибка: {str(e)}")
   
@router.delete('/{image_id}')
async def delete_image(image_id:int, 
                       current_user: User = Depends(get_current_user), 
                       db: AsyncSession = Depends(get_db)):
    
    stmnt = select(Image).where(Image.id == image_id)
    result = await db.execute(stmnt)
    img = result.scalar_one_or_none()
    
    if not img:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Image does not exists'
        )
        
    if img.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can only delete your own images'
        )
    try: 
        file_path = Path(img.path)
        file_path.unlink(missing_ok=True)
        
        await db.delete(img)
        await db.commit()
        
        return {"detail": "Image and file deleted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during deletion: {str(e)}"
        )

    
   

           
