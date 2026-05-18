from dataclasses import dataclass
from datetime import datetime

@dataclass
class RawDocumentInput:
    source_name: str
    source_type: str
    content: str

@dataclass
class RawDocumentContent:
    source_name: str
    source_type: str
    raw_text: str
    character_count: int
    processed_at: datetime

@dataclass
class IngestionResult:
    ingestion_run_id: str
    document_id: str
    document_version_id: str
    raw_content: RawDocumentContent
    can_be_activated: bool

def is_reprocessing_same_run(previous_run_id: str | None, new_run_id: str) -> bool:
    if new_run_id is None or not new_run_id.strip():
        raise ValueError("New run id cannot be empty.")
    
    if previous_run_id is not None and previous_run_id == new_run_id:
        return True
    return False
    

def build_ingestion_result(ingestion_run_id: str, document_id: str, document_version_id: str, raw_content: RawDocumentContent) -> IngestionResult:
    if raw_content.character_count > 0:
        return IngestionResult(
            ingestion_run_id=ingestion_run_id,
            document_id=document_id,
            document_version_id=document_version_id,
            raw_content=raw_content,
            can_be_activated=True
        )

    return IngestionResult(
            ingestion_run_id=ingestion_run_id,
            document_id=document_id,
            document_version_id=document_version_id,
            raw_content=raw_content,
            can_be_activated=False
        )

def should_invalidate_document_cache(previous_version_id: str| None, new_result: IngestionResult) -> bool:
    if previous_version_id is not None and previous_version_id != new_result.document_version_id and new_result.can_be_activated:
        return True
    return False

def is_duplicate_raw_document(current_input: RawDocumentInput, existing_input: RawDocumentInput) -> bool:
    normalized_current_input = current_input.content.strip()
    normalized_existing_input = existing_input.content.strip()
    
    if current_input.source_name == existing_input.source_name and current_input.source_type == existing_input.source_type and normalized_current_input == normalized_existing_input:
        return True
    return False

def parse_raw_document_input(raw_input: RawDocumentInput) -> str:
    return raw_input.content

def clean_raw_text(raw_text: str) -> str:
    return raw_text.strip()

def build_raw_document_content(raw_input: RawDocumentInput, processed_at: datetime) -> RawDocumentContent:
    raw_text = parse_raw_document_input(raw_input)
    normalized_text = clean_raw_text(raw_text)
    if not normalized_text:
        raise ValueError("Raw document content cannot be empty.")
    
    character_count = len(normalized_text)

    return RawDocumentContent(
        source_name=raw_input.source_name,
        source_type=raw_input.source_type,
        raw_text=normalized_text,
        character_count=character_count,
        processed_at=processed_at
    )