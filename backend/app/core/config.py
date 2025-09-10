from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "FastAPI with Next.js"
    admin_email: str = "huynhtoan30@gmail.com"
    database_url: str
    secret_key: str
    default_username: str
    default_password: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


@lru_cache
def get_settings():
    return Settings()
