from sqlmodel import SQLModel, create_engine, Session
from .config import get_settings
from typing import Annotated
from functools import lru_cache

from fastapi import Depends

settings = get_settings()

engine = create_engine(settings.database_url)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDeps = Annotated[Session, Depends(get_session)]
