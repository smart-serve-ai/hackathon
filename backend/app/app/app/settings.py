from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "smartserve"
    anthropic_api_key: str
    tg_api_id: str
    tg_api_hash: str
    base_db_dsn: PostgresDsn = "postgresql+psycopg://postgres:postgres@db:5432"
    db_dsn: PostgresDsn = f"{base_db_dsn}/{app_name}"
    service_provider_phone: str


settings = Settings()
