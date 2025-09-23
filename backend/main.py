from contextlib import asynccontextmanager
import json
from app.core.config import get_settings
from app.core.database import init_db, init_admin
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.logger import logger
from app.api import api_v1
from fastapi.middleware.cors import CORSMiddleware
from app.services.genmini_service import gemini_service

settings = get_settings()


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Start App")
    init_db()
    init_admin()
    gemini_service.initialize()
    logger.info("Create Database Successfully !!")
    yield


app = FastAPI(app=settings.app_name, lifespan=life_span)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1.router, prefix="/api")


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
