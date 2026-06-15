from dataclasses import dataclass

@dataclass
class DecisionInput:
    risk_level: str
    supported: bool
    confidence_level: str
    contradiction_detected: bool
    confidence_score: float
    policy_blocked: bool
    audit_persisted: bool

@dataclass
class DecisionResult:
    status: str
    decision_reason: str

def validate_decision_input (decision_input: DecisionInput) -> None:
    if not decision_input.risk_level.strip():
        raise ValueError("Risk level cannot be empty.")
    
    if not decision_input.confidence_level.strip():
        raise ValueError("Confidence level cannot be empty.")

def requires_human_review (decision_input: DecisionInput) -> DecisionResult | None:
    if decision_input.contradiction_detected:
        return DecisionResult(
            status="human_review_required",
            decision_reason="contradictory_evidence"
        )
    
    if not decision_input.supported:
        return DecisionResult(
            status="human_review_required",
            decision_reason="insufficient_evidence"
        )
    
    if decision_input.risk_level == "high" and decision_input.confidence_level != "high":
        return DecisionResult(
            status="human_review_required",
            decision_reason="high_risk_insufficient_confidence"
        )
    
    return None

def decide_outcome (decision_input: DecisionInput) -> DecisionResult:
    if not decision_input.audit_persisted:
        return DecisionResult(
            status="failed_safe",
            decision_reason="audit_persistence_failed"
        )
    
    if decision_input.policy_blocked:
        return DecisionResult(
            status="blocked",
            decision_reason="policy_blocked"
        )
    
    validate_decision_input(decision_input)

    review_result = requires_human_review(decision_input)

    if review_result is not None:
        return review_result
    
    if decision_input.confidence_score < 0.80:
        return DecisionResult(
            status="answered_with_warning",
            decision_reason="partial_evidence_allowed"
        )

    return DecisionResult(
        status="answered",
        decision_reason="sufficient_evidence"
    )