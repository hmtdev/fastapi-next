from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic import EmailStr
from app.models.user import Role


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    role: Role
    avatar: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str]
    role: Optional[Role] = Role.USER
