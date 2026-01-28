from app.services.search.pexels import search_pexels
from app.services.search.schemas import SearchResult

provider_list:list = ['pexels', 'auto']

async def search_images(provider:str, q:str, page:int, limit:int) -> list[SearchResult]:
    results = await search_pexels(query = q, limit = limit, page = page)
    return results