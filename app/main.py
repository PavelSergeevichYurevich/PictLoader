from fastapi import FastAPI
from app.api.v1.endpionts.files import router as files
from app.core.settings import settings
from contextlib import asynccontextmanager
from app.api.v1.endpionts.user import router as reg
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

