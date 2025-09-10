from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.user_services import get_users
from app.core.config import get_settings
from app.models.user import User, Role

router = APIRouter(prefix="/users", tags=["user"])
settings = get_settings()


@router.get("", include_in_schema=True)
def get_all_users(db: Session = Depends(get_session)):
    """
    Get all users from the database
    """
    users = get_users(db)
    if not users:
        new_user = User(
            username=settings.default_username,
            hashed_password=settings.default_password,
            email=settings.admin_email,
            is_active=True,
            role=Role.ADMIN,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return {"status": "ok", "data": users}


@router.get("/drop-table")
def drop_user_table(db: Session = Depends(get_session)):
    """
    Drop the User table - WARNING: This will delete all user data!
    This endpoint should be disabled in production.
    """
    # Import necessary SQLAlchemy components
    from sqlalchemy import text
    from app.models.user import User

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
