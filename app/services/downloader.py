import aiofiles
import httpx
from pathlib import Path
from app.core.settings import settings

async def download_image(url: str, filename: str) -> Path:
    target_path = settings.STORAGE_DIR/filename
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        
        async with aiofiles.open(target_path, mode='wb') as f:
            await f.write(response.content)
    
    return target_path
        