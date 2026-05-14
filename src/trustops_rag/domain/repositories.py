from typing import Protocol
from trustops_rag.domain.entities import Document, Query, Answer, ReviewTicket, AuditEvent

class DocumentRepository(Protocol):
    def save(self, document: Document) -> None:
        ...

    def get_by_id(self, document_id: str) -> Document | None:
        ...

class QueryRepository(Protocol):
    def save(self, query: Query) -> None:
        ...

    def get_by_id(self, query_id: str) -> Query | None:
        ...

    def get_by_idempotency_key(self, idempotency_key: str) -> Query | None:
        ...

class AnswerRepository(Protocol):
    def save(self, answer: Answer) -> None:
        ...

    def get_by_id(self, answer_id: str) -> Answer | None:
        ...

    def get_by_query_id(self, query_id: str) -> Answer | None:
        ...

class ReviewTicketRepository(Protocol):
    def save(self, ticket: ReviewTicket) -> None:
        ...

    def get_by_id(self, ticket_id: str) -> ReviewTicket | None:
        ...

class AuditEventRepository(Protocol):
    def append(self, event: AuditEvent) -> None:
        ...

    def get_by_id(self, event_id: str) -> AuditEvent | None:
        ...

    def list_by_query_id(self, query_id: str) -> list[AuditEvent]:
        ...