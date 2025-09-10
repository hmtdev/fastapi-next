from .v1 import user
from fastapi import APIRouter

router = APIRouter(prefix="/v1")


router.include_router(user.router)
