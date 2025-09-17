from app.core.auth_utils import get_password_hash
from app.core.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select


def get_users(db: Session):
    """
    Get all users from the database

    Args:
        db: Database session

    Returns:
        List of all users in the database
    """
    return db.exec(select(User)).all()


def get_user_by_username(db: Session, username) -> User:
    statement = select(User).where(User.username == username)
    return db.exec(statement).first()


def get_user_by_email(db: Session, email) -> User:
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, user: UserCreate):
    user_exist = get_user_by_email(db, user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists!"
        )
    new_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email,
        role=user.role,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists!111"
        )
