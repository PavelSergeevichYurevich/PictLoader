from fastapi import FastAPI, Request, requests
from fastapi.responses import JSONResponse
from app.api.v1.endpionts.files import router as files
from app.core.settings import settings
from contextlib import asynccontextmanager
from app.api.v1.endpionts.user import router as reg
from app.api.v1.endpionts.image import router as img
from app.services.search.base import SearchAuthError, SearchRateLimitError, SearchUpstreamError
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Starting server...')
    
    # При старте сервера проверяем, создана ли папка для картинок
    settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Storage initialized at {settings.STORAGE_DIR}")
    
    yield
    print('Server stopped')

app = FastAPI(
    title='PictLoader',
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None
)


app.include_router(reg)
app.include_router(files)
app.include_router(img)

@app.exception_handler(SearchAuthError)
async def err_502(request: Request, exc: SearchAuthError):
    return JSONResponse(
        status_code=502, 
        content={"detail": "Upstream authentication error",
                 "error_type": "search_auth_error"},
        )
@app.exception_handler(SearchRateLimitError)
async def err_429(request: Request, exc: SearchRateLimitError):
    return JSONResponse(
        status_code=429, 
        content={"detail": "Rate limit exceeded",
                 "error_type": "search_rate_limit_error"},
        )
@app.exception_handler(SearchUpstreamError)
async def err_503(request: Request, exc: SearchUpstreamError):
    return JSONResponse(
        status_code=503, 
        content={"detail": "Upstream service unavailable",
                 "error_type": "search_upstream_error"},
        )
        
