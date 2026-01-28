from fastapi import APIRouter, Depends
from app.services.search.images import search_images
from app.schemas.images import ImageSearchScema

router = APIRouter(prefix='/images', tags=['Images'])

@router.get('/search')
async def search(image_search:ImageSearchScema = Depends()):

    result = await search_images(
        provider = image_search.provider, 
        q = image_search.q, 
        page = image_search.page ,
        limit = image_search.limit
        )
    return {'result': result}