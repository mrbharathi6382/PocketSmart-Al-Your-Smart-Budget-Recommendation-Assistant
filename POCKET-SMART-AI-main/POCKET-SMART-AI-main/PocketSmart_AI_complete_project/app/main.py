from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import init_db
from .routes.api import router as api_router
from .routes.pages import router as page_router
settings=get_settings()
@asynccontextmanager
async def lifespan(app):
    init_db(); yield
app=FastAPI(title=settings.app_name,version="1.0.0",description="Budget-aware recommendation assistant",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory="app/static"),name="static")
app.include_router(page_router); app.include_router(api_router)
if __name__=="__main__":
    import uvicorn; uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
