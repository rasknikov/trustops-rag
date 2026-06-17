from dataclasses import dataclass

@dataclass
class ObservabilityInput:
    query_id: str
    status: str
    cost_usd: float
    system_state: str
    confidence_score: float
    evaluation_label: str


@dataclass
class ObservabilityEvent:
    event_id: str
    query_id: str
    status: str
    cost_usd: float
    system_state: str
    confidence_score: float
    evaluation_label: str

def validate_observability_input(observability_input: ObservabilityInput) -> None:
    if not observability_input.query_id.strip():
        raise ValueError("Query id cannot be empty.")
    
    if not observability_input.status.strip():
        raise ValueError("Status cannot be empty.")
    
    if observability_input.cost_usd < 0:
        raise ValueError("Cost usd cannot be negative.")
    
    if not observability_input.system_state.strip():
        raise ValueError("System state cannot be empty.")
    
    if observability_input.confidence_score < 0:
        raise ValueError("Confidence score cannot be negative.")
    
    if not observability_input.evaluation_label.strip():
        raise ValueError("Evaluation label cannot be empty.")

def build_event_id(observability_input: ObservabilityInput) -> str:
    return f"obs-{observability_input.query_id}"

def build_observability_event(observability_input: ObservabilityInput) -> ObservabilityEvent:

    validate_observability_input(observability_input)

    event_id=build_event_id(observability_input)
    
    return ObservabilityEvent(
        event_id=event_id,
        query_id=observability_input.query_id,
        status=observability_input.status,
        cost_usd=observability_input.cost_usd,
        system_state=observability_input.system_state,
        confidence_score=observability_input.confidence_score,
        evaluation_label=observability_input.evaluation_label
    )