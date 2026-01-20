import os
from pathlib import Path
import uuid
from fastapi import APIRouter, HTTPException
from app.core.settings import settings
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
async def download_by_url(url: str):
    try:
        url_path = Path(url)
        file_extension = url_path.suffix 
        if len(file_extension) > 4: file_extension = "jpg"
        random_name = f'{uuid.uuid4()}.{file_extension}'
        path = await download_image(url, random_name)
        return {
            'status': 'success',
            'filename': random_name,
            'absolute_path': str(path)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при скачивании: {str(e)}") 
