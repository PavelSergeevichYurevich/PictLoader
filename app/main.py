from fastapi import FastAPI
from app.api.route import router
from app.core.settings import settings
from contextlib import asynccontextmanager

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


app.include_router(router)
