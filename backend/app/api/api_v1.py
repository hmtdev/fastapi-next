from .v1 import user, auth, genmini, youtube, upload, dashbboard
from fastapi import APIRouter

router = APIRouter(prefix="/v1")


router.include_router(user.router)
router.include_router(auth.router)
router.include_router(genmini.router)
router.include_router(youtube.router)
router.include_router(upload.router)
router.include_router(dashbboard.router)
