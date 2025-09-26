from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select
from app.core.logger import logger
from .config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url)


def init_admin():
    from app.models.user import Role, User
    from app.core.auth_utils import get_password_hash

    with Session(engine) as session:
        statement = select(User).where(User.role == "admin")
        exist_admin = session.exec(statement).first()
        if not exist_admin:
            admin = User(
                username=settings.default_username,
                email=settings.admin_email,
                hashed_password=get_password_hash(settings.default_password),
                role=Role.ADMIN,
                is_active=True,
            )
            session.add(admin)
            try:
                session.commit()
                session.refresh(admin)
                logger.info("Init admin default successfully")
            except Exception as e:
                logger.error(str(e))
                logger.error("Failed to init admin default")
                session.rollback()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDeps = Annotated[Session, Depends(get_session)]
