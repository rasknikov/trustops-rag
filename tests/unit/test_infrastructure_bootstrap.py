from trustops_rag.infrastructure.bootstrap import build_query_repository
from trustops_rag.infrastructure.errors import ConfigurationError
from trustops_rag.infrastructure.query_repository import InMemoryQueryRepository
from trustops_rag.infrastructure.settings import InfrastructureSettings


def test_build_query_repository_returns_memory_repository() -> None:
    settings = InfrastructureSettings(query_repository_backend="memory")

    repository = build_query_repository(settings)

    assert isinstance(repository, InMemoryQueryRepository)


def test_build_query_repository_requires_database_url_for_postgresql() -> None:
    settings = InfrastructureSettings(
        query_repository_backend="postgresql",
        database_url=None,
    )

    try:
        build_query_repository(settings)
    except ConfigurationError as error:
        assert (
            str(error)
            == "database_url is required when query_repository_backend is postgresql."
        )
        return

    raise AssertionError("Expected ConfigurationError for missing database_url.")
