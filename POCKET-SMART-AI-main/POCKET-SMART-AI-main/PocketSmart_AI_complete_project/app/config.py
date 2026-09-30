from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    app_env: str = "development"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    access_token_expire_minutes: int = 1440
    max_upload_mb: int = 5
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    cookie_secure: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    @property
    def cors_origin_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
