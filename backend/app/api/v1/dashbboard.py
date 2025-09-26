import select
from fastapi import APIRouter, Depends

from app.services.auth_service import get_current_user
from app.core.database import get_session
from app.models.user import User
from app.schemas.user import UserStats
from sqlmodel import select

router = APIRouter(tags=["Dashboard"], prefix="/dashboard")


@router.get("/stats", response_model=UserStats)
async def users_stats(user=Depends(get_current_user), db=Depends(get_session)):
    print(user)
    return UserStats.model_validate(user)
