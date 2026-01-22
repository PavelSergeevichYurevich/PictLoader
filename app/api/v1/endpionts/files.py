import asyncio
from pathlib import Path
from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.settings import settings
from app.models.image import Image
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
async def download_by_url(urls: List[str], user_id: int, db:AsyncSession = Depends(get_db)):
   try:
        tasks:list = []
        for u in urls:
            url_path = Path(u)
            ext = url_path.suffix if len(url_path.suffix) <= 5 else '.jpg'
            random_name = f'{uuid.uuid4()}{ext}'
            tasks.append(download_image(u, random_name))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
           
        fls:dict = {}
        for i, path in enumerate(results):
            if isinstance(path, Path):
                new_img = Image(
                    filename = path.name,
                    source_url = urls[i],
                    path = str(path),
                    user_id = user_id
                )
                db.add(new_img)
                fls[path.name] = str(path)
            else:
                fls[urls[i]] = f'Error: {str(path)}'
        await db.commit()

        return {
            'status': 'success',
            'files': fls
        }
   except Exception as e:
       raise HTTPException(status_code=400, detail=f"Критическая ошибка: {str(e)}")
           
