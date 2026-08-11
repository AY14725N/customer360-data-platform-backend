from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Customer 360 API"
    app_env: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "customer360"
    postgres_user: str = "customer360"
    postgres_password: str = "customer360"
    kafka_bootstrap_servers: str = "localhost:29092"
    kafka_group_id: str = "customer360"
    raw_storage_path: Path = Path("storage/raw")
    model_path: Path = Path("ml/models/churn_model.joblib")
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
