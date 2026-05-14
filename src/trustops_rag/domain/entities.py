from dataclasses import dataclass, field
from datetime import datetime
from trustops_rag.domain.value_objects import QueryStatus, TicketStatus

@dataclass
class Document:
    id: str
    tenant_id: str
    title: str
    source_type: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Document id cannot be empty.")
        
        if not self.tenant_id.strip():
            raise ValueError("Document tenant_id cannot be empty.")
        
        if not self.title.strip():
            raise ValueError("Document title cannot be empty.")
        
        if not self.source_type.strip():
            raise ValueError("Document source_type cannot be empty.")

@dataclass
class DocumentVersion:
    id: str
    document_id: str
    version_label: str
    storage_uri: str
    checksum: str
    is_active: bool
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("DocumentVersion id cannot be empty.")
        
        if not self.document_id.strip():
            raise ValueError("DocumentVersion document_id cannot be empty.")
        
        if not self.version_label.strip():
            raise ValueError("DocumentVersion version_label cannot be empty.")
        
        if not self.storage_uri.strip():
            raise ValueError("DocumentVersion storage_uri cannot be empty.")
        
        if not self.checksum.strip():
            raise ValueError("DocumentVersion checksum cannot be empty.")

@dataclass
class DocumentChunk:
    id: str
    document_version_id: str
    chunk_index: int
    content: str
    token_count: int
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("DocumentChunk id cannot be empty.")
        
        if not self.document_version_id.strip():
            raise ValueError("DocumentChunk document_version_id cannot be empty.")
        
        if self.chunk_index < 0:
            raise ValueError("DocumentChunk chunk_index cannot be negative.")
        
        if not self.content.strip():
            raise ValueError("DocumentChunk content cannot be empty.")
        
        if self.token_count < 0:
            raise ValueError("DocumentChunk token_count cannot be negative.")


@dataclass
class Query:
    id: str
    tenant_id: str
    question: str
    policy_version: str
    created_at: datetime
    idempotency_key: str | None = None

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Query id cannot be empty.")
        
        if not self.tenant_id.strip():
            raise ValueError("Query tenant_id cannot be empty.")
        
        if not self.question.strip():
            raise ValueError("Query question cannot be empty.")
        
        if not self.policy_version.strip():
            raise ValueError("Query policy_version cannot be empty.")
        
@dataclass
class Answer:
    id: str
    query_id: str
    status: QueryStatus
    policy_version: str
    system_state: str
    decision_reason: str
    created_at: datetime
    answer_text: str | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        has_message = False
        has_answer_text = False

        if not self.id.strip():
            raise ValueError("Answer id cannot be empty.")
        
        if not self.query_id.strip():
            raise ValueError("Answer query_id cannot be empty.")
        
        if self.status is None:
            raise ValueError("Answer status cannot be empty.")
        
        if not self.policy_version.strip():
            raise ValueError("Answer policy_version cannot be empty.")
        
        if not self.system_state.strip():
            raise ValueError("Answer system_state cannot be empty.")
        
        if not self.decision_reason.strip():
            raise ValueError("Answer decision_reason cannot be empty.")
            
        if self.answer_text is not None and self.answer_text.strip():
            has_answer_text = True

        if self.message is not None and self.message.strip():
            has_message = True

        if not has_answer_text and not has_message:
            raise ValueError("Answer answer_text and message cannot be empty.")

@dataclass
class ReviewTicket:
    id: str
    query_id: str
    status: TicketStatus
    policy_version: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("ReviewTicket id cannot be empty.")
        
        if not self.query_id.strip():
            raise ValueError("ReviewTicket query_id cannot be empty.")
        
        if self.status is None:
            raise ValueError("ReviewTicket status cannot be empty.")
        
        if not self.policy_version.strip():
            raise ValueError("ReviewTicket policy_version cannot be empty.")

@dataclass
class AuditEvent:
    id: str
    query_id: str
    event_type: str
    policy_version: str
    created_at: datetime
    payload: dict[str, str | int | float | bool| None] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("AuditEvent id cannot be empty.")
        
        if not self.query_id.strip():
            raise ValueError("AuditEvent query_id cannot be empty.")
        
        if not self.event_type.strip():
            raise ValueError("AuditEvent event_type cannot be empty.")
        
        if not self.policy_version.strip():
            raise ValueError("AuditEvent policy_version cannot be empty.")