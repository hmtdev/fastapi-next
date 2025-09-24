from fastapi import APIRouter, Depends, UploadFile
from app.core.supabase import get_supabase_client
from app.services.upload_service import upload_avatar

router = APIRouter(tags=["Upload"], prefix="/upload")


@router.post("/avatar")
async def upload_avatar_endpoint(
    file: UploadFile, supabase=Depends(get_supabase_client)
):
    return await upload_avatar(file, supabase)
