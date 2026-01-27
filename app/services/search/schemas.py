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