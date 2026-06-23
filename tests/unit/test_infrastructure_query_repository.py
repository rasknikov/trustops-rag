from datetime import datetime

from trustops_rag.domain.entities import Query
from trustops_rag.infrastructure.errors import RepositoryConflictError
from trustops_rag.infrastructure.query_repository import InMemoryQueryRepository


def test_save_and_get_by_id() -> None:
    repository = InMemoryQueryRepository()

    query = Query(
        id="q-1",
        tenant_id="acme",
        question="Como funciona?",
        policy_version="v1",
        created_at=datetime.now(),
        idempotency_key="idem-123",
    )

    repository.save(query)

    saved_query = repository.get_by_id("q-1")

    assert saved_query == query


def test_save_and_get_by_idempotency_key() -> None:
    repository = InMemoryQueryRepository()

    query = Query(
        id="q-1",
        tenant_id="acme",
        question="Como funciona?",
        policy_version="v1",
        created_at=datetime.now(),
        idempotency_key="idem-123",
    )

    repository.save(query)

    saved_query = repository.get_by_idempotency_key("idem-123")

    assert saved_query == query


def test_get_by_id_returns_none_when_query_is_missing() -> None:
    repository = InMemoryQueryRepository()

    saved_query = repository.get_by_id("missing-query")

    assert saved_query is None


def test_get_by_id_raises_error_for_blank_identifier() -> None:
    repository = InMemoryQueryRepository()

    try:
        repository.get_by_id("   ")
    except ValueError as error:
        assert str(error) == "query_id cannot be blank."
        return

    raise AssertionError("Expected ValueError for blank query_id.")


def test_get_by_idempotency_key_raises_error_for_blank_identifier() -> None:
    repository = InMemoryQueryRepository()

    try:
        repository.get_by_idempotency_key("   ")
    except ValueError as error:
        assert str(error) == "idempotency_key cannot be blank."
        return

    raise AssertionError("Expected ValueError for blank idempotency_key.")


def test_save_raises_conflict_for_reused_idempotency_key() -> None:
    repository = InMemoryQueryRepository()

    first_query = Query(
        id="q-1",
        tenant_id="acme",
        question="Como funciona?",
        policy_version="v1",
        created_at=datetime.now(),
        idempotency_key="idem-123",
    )
    second_query = Query(
        id="q-2",
        tenant_id="acme",
        question="Qual e o status?",
        policy_version="v1",
        created_at=datetime.now(),
        idempotency_key="idem-123",
    )

    repository.save(first_query)

    try:
        repository.save(second_query)
    except RepositoryConflictError as error:
        assert str(error) == "Idempotency key is already associated with another query."
        return

    raise AssertionError("Expected RepositoryConflictError for duplicated idempotency key.")
