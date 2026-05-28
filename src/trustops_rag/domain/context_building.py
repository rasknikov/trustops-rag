from dataclasses import dataclass

@dataclass
class ContextBuildInput:
    normalized_question: str
    max_chunks: int

@dataclass
class ContextItem:
    chunk_id: str
    document_version_id: str
    content: str
    position: int
    citation_label: str

@dataclass
class BuiltContext:
    question: str
    items: list[ContextItem]
    rendered_context: str

def validate_context_build_input(context_input: ContextBuildInput, available_chunks: list[ContextItem]) -> None:
    if not context_input.normalized_question.strip():
        raise ValueError("Normalized question cannot be empty.")
    
    if context_input.max_chunks <= 0:
        raise ValueError("max_chunks must be greater than zero.")
    
    if not available_chunks:
        raise ValueError("Available chunks cannot be empty.")
    
def select_context_items(context_input: ContextBuildInput, available_chunks: list[ContextItem]) -> list[ContextItem]:
    selected_items = available_chunks[:context_input.max_chunks]
    positioned_items = []

    for index, item in enumerate(selected_items, start=1):
        positioned_items.append(
            ContextItem(
                chunk_id=item.chunk_id,
                document_version_id=item.document_version_id,
                content=item.content,
                position=index,
                citation_label=f"[{index}]"
            )
        )

    return positioned_items

def build_context(context_input: ContextBuildInput, available_chunks: list[ContextItem]) -> BuiltContext:
    validate_context_build_input(context_input, available_chunks)
        
    selected_items = select_context_items(context_input, available_chunks)
    rendered_parts = []

    for item in selected_items:
        rendered_parts.append(f"{item.citation_label} {item.content}")

    rendered_context = "\n\n".join(rendered_parts)

    return BuiltContext(
        question=context_input.normalized_question,
        items=selected_items,
        rendered_context=rendered_context,
    )
