from typing import Annotated

from app.core.auth_utils import get_password_hash
from app.core.config import get_settings
from app.core.database import get_session
from app.models.user import Role, User
from app.schemas.user import UserBase, UserCreate
from app.services.auth_service import get_admin_user, get_current_user
from app.services.user_services import create_user, get_users
from fastapi import APIRouter, Depends
from sqlmodel import Session

router = APIRouter(prefix="/users", tags=["User"])
settings = get_settings()


@router.get("", include_in_schema=True, response_model=list[UserBase])
def get_all_users(db: Session = Depends(get_session)):
    """
    Get all users from the database
    """
    users = get_users(db)
    if not users:
        new_user = User(
            username=settings.default_username,
            hashed_password=get_password_hash(settings.default_password),
            email=settings.admin_email,
            is_active=True,
            role=Role.ADMIN,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return [UserBase.model_validate(u) for u in users]


@router.get("/drop-table")
def drop_user_table(db: Session = Depends(get_session)):
    """
    Drop the User table - WARNING: This will delete all user data!
    This endpoint should be disabled in production.
    """
    # Import necessary SQLAlchemy components
    from app.models.user import User
    from sqlalchemy import text

    try:
        # Drop the table using raw SQL for force drop
        db.exec(text(f'DROP TABLE IF EXISTS "{User.__tablename__}" CASCADE'))
        db.commit()

        # Alternative approach using SQLAlchemy metadata
        # User.__table__.drop(db.get_bind())
        # db.commit()

        return {"status": "success", "message": "User table has been dropped"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}


@router.post("/register", response_model=UserBase)
async def create_user_by_email(user: UserCreate, db: Session = Depends(get_session)):
    new_user = create_user(db, user)
    return UserBase.model_validate(new_user)


@router.get("/me", response_model=UserBase)
async def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return UserBase.model_validate(current_user)
