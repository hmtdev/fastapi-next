from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
    email: EmailStr | None = None


class TokenRefresh(BaseModel):
    refresh_token: str
