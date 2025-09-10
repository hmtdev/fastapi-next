from contextlib import asynccontextmanager
import json
from app.core.config import get_settings
from app.core.database import init_db
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.logger import logger
from app.api import api_v1

settings = get_settings()


@asynccontextmanager
async def life_span(app: FastAPI):
    logger.info("Start App")
    init_db()
    logger.info("Create Database Successfully !!")
    yield


app = FastAPI(app=settings.app_name, lifespan=life_span)


app.include_router(api_v1.router, prefix="/api")


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
