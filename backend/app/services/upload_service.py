from fastapi import File, HTTPException, status
from supabase import Client
from datetime import datetime


async def upload_avatar(
    file: File, supabase: Client, custom_filename: str | None = None
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload an image."
        )

    # Tạo timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Lấy phần mở rộng của file (nếu có)
    file_extension = file.filename.split(".")[-1] if "." in file.filename else ""

    # Tạo tên file với định dạng avatar_timestamp.extension
    file_name = f"avatars/{custom_filename or f'avatar_{timestamp}'}"
    if file_extension:
        file_name += f".{file_extension}"

    try:
        # Upload file lên Supabase
        response = supabase.storage.from_("avatars").upload(
            file_name, await file.read()
        )

        # Lấy URL công khai của file
        public_url = supabase.storage.from_("avatars").get_public_url(file_name)
        return {"url": public_url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}",
        )
