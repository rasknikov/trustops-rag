from dataclasses import dataclass

from trustops_rag.domain.context_building import BuiltContext


@dataclass
class ReliabilityInput:
    question: str
    answer_text: str
    built_context: BuiltContext


@dataclass
class ReliabilityAssessment:
    supported: bool
    confidence_level: str
    confidence_score: float
    evidence_score: float
    contradiction_detected: bool
    matched_context_items: int
    unsupported_claims_count: int
    reliability_reason: str


def validate_reliability_input(reliability_input: ReliabilityInput) -> None:
    if not reliability_input.question.strip():
        raise ValueError("Question cannot be empty.")

    if not reliability_input.answer_text.strip():
        raise ValueError("Answer text cannot be empty.")

    if not reliability_input.built_context.items:
        raise ValueError("Built context must contain at least one item.")

    if not reliability_input.built_context.rendered_context.strip():
        raise ValueError("Built context rendered text cannot be empty.")


def normalize_reliability_text(text: str) -> str:
    return text.strip().lower()


def extract_answer_terms(answer_text: str) -> list[str]:
    normalized_answer = normalize_reliability_text(answer_text)
    answer_terms: list[str] = []

    for term in normalized_answer.split():
        cleaned_term = term.strip(".,:;!?()[]{}\"'")
        if len(cleaned_term) >= 3:
            answer_terms.append(cleaned_term)

    return answer_terms


def count_matched_context_items(answer_terms: list[str], built_context: BuiltContext) -> int:
    matched_items = 0

    for item in built_context.items:
        normalized_content = normalize_reliability_text(item.content)

        for term in answer_terms:
            if term in normalized_content:
                matched_items += 1
                break

    return matched_items


def calculate_evidence_score(answer_terms: list[str], built_context: BuiltContext) -> float:
    if not answer_terms:
        return 0.0

    normalized_context = normalize_reliability_text(built_context.rendered_context)
    matched_terms = 0

    for term in set(answer_terms):
        if term in normalized_context:
            matched_terms += 1

    evidence_score = matched_terms / len(set(answer_terms))

    return round(evidence_score, 2)


def detect_contradiction(answer_text: str, built_context: BuiltContext) -> bool:
    normalized_answer = normalize_reliability_text(answer_text)
    normalized_context = normalize_reliability_text(built_context.rendered_context)

    contradiction_pairs = [
        ("allowed", "not allowed"),
        ("not allowed", "allowed"),
        ("required", "not required"),
        ("not required", "required"),
    ]

    for answer_phrase, context_phrase in contradiction_pairs:
        if answer_phrase in normalized_answer and context_phrase in normalized_context:
            return True

    return False


def calculate_confidence_score(
    evidence_score: float,
    contradiction_detected: bool,
    matched_context_items: int,
) -> float:
    confidence_score = evidence_score

    if matched_context_items >= 2:
        confidence_score += 0.1

    if contradiction_detected:
        confidence_score -= 0.4
        confidence_score = min(confidence_score, 0.4)

    confidence_score = max(0.0, min(confidence_score, 1.0))

    return round(confidence_score, 2)


def classify_confidence_level(confidence_score: float) -> str:
    if confidence_score >= 0.8:
        return "high"

    if confidence_score >= 0.6:
        return "medium"

    return "low"


def determine_reliability_reason(
    supported: bool,
    contradiction_detected: bool,
    evidence_score: float,
) -> str:
    if contradiction_detected:
        return "contradictory_context"

    if supported and evidence_score >= 0.8:
        return "supported_by_context"

    if supported:
        return "partial_context_support"

    return "insufficient_context_support"


def assess_reliability(reliability_input: ReliabilityInput) -> ReliabilityAssessment:
    validate_reliability_input(reliability_input)

    answer_terms = extract_answer_terms(reliability_input.answer_text)
    matched_context_items = count_matched_context_items(
        answer_terms,
        reliability_input.built_context,
    )
    evidence_score = calculate_evidence_score(
        answer_terms,
        reliability_input.built_context,
    )
    contradiction_detected = detect_contradiction(
        reliability_input.answer_text,
        reliability_input.built_context,
    )
    confidence_score = calculate_confidence_score(
        evidence_score,
        contradiction_detected,
        matched_context_items,
    )
    confidence_level = classify_confidence_level(confidence_score)
    supported = evidence_score >= 0.5 and not contradiction_detected

    if supported:
        unsupported_claims_count = 0
    else:
        unsupported_claims_count = 1

    reliability_reason = determine_reliability_reason(
        supported,
        contradiction_detected,
        evidence_score,
    )

    return ReliabilityAssessment(
        supported=supported,
        confidence_level=confidence_level,
        confidence_score=confidence_score,
        evidence_score=evidence_score,
        contradiction_detected=contradiction_detected,
        matched_context_items=matched_context_items,
        unsupported_claims_count=unsupported_claims_count,
        reliability_reason=reliability_reason,
    )
