from typing import Protocol
from trustops_rag.domain.repositories import QueryRepository, AnswerRepository, AuditEventRepository

class UnitOfWork(Protocol):
    queries: QueryRepository
    answers: AnswerRepository
    audit_events: AuditEventRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...