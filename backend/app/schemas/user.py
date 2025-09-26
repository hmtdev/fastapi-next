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
    level: str = None
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: Optional[str]
    role: Optional[Role] = Role.USER


class UserStats(UserBase):
    last_name: Optional[str] = None
    total_lession_completed: int = 0
    level_type: Optional[str] = None
    level_details: list = []
    current_level: dict = {}
    first_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    total_study_time: int = 0
    total_words_learned: Optional[int] = 999
    model_config = ConfigDict(from_attributes=True)
