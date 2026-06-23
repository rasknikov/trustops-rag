from trustops_rag.domain.repositories import QueryRepository
from trustops_rag.infrastructure.errors import ConfigurationError
from trustops_rag.infrastructure.query_repository import InMemoryQueryRepository
from trustops_rag.infrastructure.settings import InfrastructureSettings


def build_query_repository(
    settings: InfrastructureSettings | None = None,
) -> QueryRepository:
    resolved_settings = settings or InfrastructureSettings()

    if resolved_settings.query_repository_backend == "memory":
        return InMemoryQueryRepository()

    if not resolved_settings.database_url:
        raise ConfigurationError(
            "database_url is required when query_repository_backend is postgresql."
        )

    raise ConfigurationError(
        "PostgreSQL query repository is not implemented yet."
    )
