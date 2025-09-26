from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
import uuid
from pydantic import EmailStr
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserLevel(str, Enum):
    BEGINER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class LevelType(str, Enum):
    TOEIC = "TOEIC"
    IELTS = "IELTS"
    TOEFL = "TOEFL"
    PTE = "PTE"
    DUOLINGO = "Duolingo"
    CAMBRIDGE_FCE = "Cambridge FCE"
    CAMBRIDGE_CAE = "Cambridge CAE"
    CAMBRIDGE_CPE = "Cambridge CPE"
    CEFR_A1 = "CEFR A1"
    CEFR_A2 = "CEFR A2"
    CEFR_B1 = "CEFR B1"
    CEFR_B2 = "CEFR B2"
    CEFR_C1 = "CEFR C1"
    CEFR_C2 = "CEFR C2"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    hashed_password: str
    is_active: bool = True
    role: Role = Field(default=Role.USER, nullable=False)
    avatar: str = Field(nullable=True)
    ## other user infor
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    date_of_birth: Optional[str] = Field(default=None, nullable=True)
    ##
    total_lession_completed: int = Field(default=0)
    total_study_time: int = Field(default=0)
    level: Optional[UserLevel] = Field(default=UserLevel.BEGINER, nullable=False)
    level_type: Optional[LevelType] = Field(default=LevelType.DUOLINGO, nullable=False)
    current_level_id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    level_details: list = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False)
    )
    current_level: dict = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=True)
    )


class UserLevelDetail(SQLModel, table=True):
    __tablename__ = "user_level_details"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # remove foreign_key(...) here to avoid FK constraint
    user_id: uuid.UUID = Field(nullable=False, index=True)
    exam: LevelType
    score: float
    cefr: Optional[str] = None
    mapped_level: Optional[UserLevel] = None
    date_taken: Optional[datetime] = None
    details: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=True))
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
