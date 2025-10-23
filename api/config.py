from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str

    # This tells Pydantic to read settings from a .env.local file
    model_config = SettingsConfigDict(
        env_file=".env.local", 
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra fields that aren't defined
    )

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    This function returns a cached instance of the Settings object.
    Caching is used to prevent reading the .env file multiple times.
    """
    return Settings()