from .v1 import user, auth
from fastapi import APIRouter

router = APIRouter(prefix="/v1")


router.include_router(user.router)
router.include_router(auth.router)
