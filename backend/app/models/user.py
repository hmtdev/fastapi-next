from sqlmodel import SQLModel, Field
from enum import Enum
import uuid
from pydantic import EmailStr


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    hashed_password: str
    is_active: bool = True
    role: Role = Field(default=Role.ADMIN, nullable=False)
