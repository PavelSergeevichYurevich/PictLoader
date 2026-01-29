from fastapi import APIRouter, Depends
from app.services.search.images import search_images
from app.schemas.images import ImageSearchScema
from app.services.search.schemas import SearchResponse

router = APIRouter(prefix='/images', tags=['Images'])

@router.get('/search', response_model=SearchResponse)
async def search(image_search:ImageSearchScema = Depends()):
    result = await search_images(
        provider = image_search.provider, 
        q = image_search.q, 
        page = image_search.page ,
        limit = image_search.limit
        )
 
    return SearchResponse(
        items = result,
        count = len(result),
        page = image_search.page,
        limit = image_search.limit,
        provider_used = image_search.provider,
    )