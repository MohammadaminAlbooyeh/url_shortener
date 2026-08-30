from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./url_shortener.db"
    base_url: str = "http://localhost:8000"
    api_key: str | None = None
    rate_limit: str = "10/minute"
    max_long_url_length: int = 2048

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
