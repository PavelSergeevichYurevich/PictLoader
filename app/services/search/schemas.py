from pydantic import AnyUrl, BaseModel, HttpUrl

class SearchResult(BaseModel): 
    source: str 
    image_url: AnyUrl | HttpUrl 
    preview_url: AnyUrl | HttpUrl | None 
    width: int | None 
    height: int | None 
    author: str | None 
    provider_id: str | None 
    page_url: AnyUrl | HttpUrl | None 
    class Config:
        frozen = True
        
class SearchResponse(BaseModel):
    items: list[SearchResult]
    count: int
    page: int
    limit: int
    provider_used: str
    