from sqlmodel import select, Session
from app.models.user import User


def get_users(db: Session):
    """
    Get all users from the database

    Args:
        db: Database session

    Returns:
        List of all users in the database
    """
    return db.exec(select(User)).all()
