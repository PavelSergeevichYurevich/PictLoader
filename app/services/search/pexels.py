from app.services.search.schemas import SearchResult
from app.services.search.base import SearchAuthError, SearchRateLimitError, SearchUpstreamError
import httpx
from app.core.settings import settings

async def search_pexels(query: str, limit: int = 20, page: int = 1) -> list[SearchResult]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('https://api.pexels.com/v1/search', 
                params = {
                    'query': query,
                    'page': page,
                    'per_page': limit
                },
                headers = {
                    'Authorization': settings.PEXELS_API_KEY
                },
                timeout=10
            )
        except httpx.TimeoutException:  
            raise SearchUpstreamError()
            
        if response.status_code != 200:
            if response.status_code == 401 or response.status_code == 403:
                raise SearchAuthError("Pexels returned 401/403")
            elif response.status_code == 429:
                raise SearchRateLimitError("Pexels returned 429")
            elif response.status_code >= 500:
                raise SearchUpstreamError("Pexels timeout")
            else:
                raise SearchUpstreamError()
       
         
        data = response.json()
        photos = data.get('photos',[])
        return_list:list[SearchResult] = []
        
        for photo in photos:
            return_list.append(SearchResult(
                source = "pexels",
                image_url = photo["src"]["original"],
                preview_url = photo["src"].get("medium"), 
                width = photo.get("width"),
                height = photo.get("height"),
                author = photo.get("photographer"),
                provider_id = str(photo.get("id")),
                page_url = photo.get("url")
                )
            )
            
    return return_list
    