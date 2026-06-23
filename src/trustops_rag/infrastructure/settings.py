from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class InfrastructureSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TRUSTOPS_",
        extra="ignore",
    )

    query_repository_backend: str = "memory"
    database_url: str | None = None
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    @field_validator("query_repository_backend")
    @classmethod
    def validate_query_repository_backend(cls, value: str) -> str:
        normalized_value = value.strip().lower()

        if normalized_value not in {"memory", "postgresql"}:
            raise ValueError("Unsupported query repository backend.")

        return normalized_value
