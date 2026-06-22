from dataclasses import dataclass

from trustops_rag.domain.query_understanding import RawQuestionInput, analyze_question

@dataclass
class AskInput:
    question: str
    tenant_id: str
    user_id: str

@dataclass
class AskResult:
    status: str
    decision_reason: str
    risk_level: str | None
    complexity: str | None

def is_invalid_ask_input(ask_input: AskInput) -> bool:
    if not ask_input.tenant_id.strip():
        return True
    
    if not ask_input.user_id.strip():
        return True
    
    if not ask_input.question.strip():
        return True
    
    return False

def build_invalid_request_result() -> AskResult:
    return AskResult(
        status="failed_safe",
        decision_reason="invalid_request",
        risk_level=None,
        complexity=None
    )

def build_stub_success_result(risk_level: str, complexity: str) -> AskResult:
    return AskResult(
        status="answered",
        decision_reason="application_stub",
        risk_level=risk_level,
        complexity=complexity
    )

def handle_ask(ask_input: AskInput) -> AskResult:
    if is_invalid_ask_input(ask_input):
        return build_invalid_request_result()

    raw_ask_input = RawQuestionInput(question=ask_input.question)

    analysis = analyze_question(raw_ask_input)

    return build_stub_success_result(risk_level=analysis.risk_level, complexity=analysis.complexity)