from trustops_rag.domain.entities import Query
from trustops_rag.domain.repositories import QueryRepository
from trustops_rag.infrastructure.errors import RepositoryConflictError


class InMemoryQueryRepository(QueryRepository):
    def __init__(self) -> None:
        self._queries_by_id: dict[str, Query] = {}
        self._query_ids_by_idempotency_key: dict[str, str] = {}

    def save(self, query: Query) -> None:
        self._validate_query(query)
        self._ensure_no_conflict(query)

        self._queries_by_id[query.id] = query

        if query.idempotency_key is not None:
            self._query_ids_by_idempotency_key[query.idempotency_key] = query.id

    def get_by_id(self, query_id: str) -> Query | None:
        self._validate_identifier(query_id, "query_id")

        return self._queries_by_id.get(query_id)

    def get_by_idempotency_key(self, idempotency_key: str) -> Query | None:
        self._validate_identifier(idempotency_key, "idempotency_key")

        query_id = self._query_ids_by_idempotency_key.get(idempotency_key)

        if query_id is None:
            return None

        return self._queries_by_id.get(query_id)

    def _ensure_no_conflict(self, query: Query) -> None:
        existing_query = self._queries_by_id.get(query.id)

        if existing_query is not None:
            existing_key = existing_query.idempotency_key

            if existing_key != query.idempotency_key:
                raise RepositoryConflictError(
                    "Cannot overwrite query with a different idempotency key."
                )

        if query.idempotency_key is None:
            return

        existing_query_id = self._query_ids_by_idempotency_key.get(query.idempotency_key)

        if existing_query_id is not None and existing_query_id != query.id:
            raise RepositoryConflictError(
                "Idempotency key is already associated with another query."
            )

    def _validate_query(self, query: Query) -> None:
        if not query.id.strip():
            raise ValueError("Query id cannot be blank.")

        if query.idempotency_key is None:
            return

        self._validate_identifier(query.idempotency_key, "idempotency_key")

    def _validate_identifier(self, value: str, field_name: str) -> None:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be blank.")
