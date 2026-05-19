from dataclasses import dataclass

@dataclass
class RawQuestionInput:
    question: str

@dataclass
class QuestionAnalysis:
    intent: str
    risk_level: str
    complexity: str
    normalized_question: str
    should_retrieve: bool
    policy_scope: str
    risk_reason: str
    retrieval_reason: str


"""
tá hardcoded pra integração futura com os outros módulos
"""

def normalize_question(question: str) -> str:
    normalized_question = question.strip().lower()
    return normalized_question

def detect_question_complexity(normalized_question: str) -> str:
    if len(normalized_question) <= 80:
        complexity="simple"
    else:
        complexity="medium"
    return complexity

def detect_question_risk(normalized_question: str) -> str:
    if "salary" in normalized_question or "medical" in normalized_question or "termination" in normalized_question or "disciplinary" in normalized_question:
        risk_level="high"
    else:
        risk_level="low"
    return risk_level
    
def detect_question_intent(normalized_question: str) -> str:
    if "how" in normalized_question or "what" in normalized_question:
        intent="information_request"
    elif "can i" in normalized_question or "am i allowed" in normalized_question:
        intent="permission_check"
    else:
        intent="general_question"
    return intent

def detect_should_retrieve(normalized_question: str) -> bool:
    if len(normalized_question) < 3:
        should_retrieve = False
    else:
        should_retrieve=True

    return should_retrieve

def detect_policy_scope(normalized_question: str) -> str:
    if "salary" in normalized_question or "medical" in normalized_question or "termination" in normalized_question or "disciplinary" in normalized_question:
        policy_scope="sensitive"
    else:
        policy_scope="default"
    return policy_scope

def analyze_question(raw_input: RawQuestionInput) -> QuestionAnalysis:
    normalized_question = normalize_question(raw_input.question)

    if normalized_question == "":
        raise ValueError("Question cannot be empty.")
    
    complexity = detect_question_complexity(normalized_question)

    risk_level = detect_question_risk(normalized_question)

    if risk_level == "high":
        risk_reason = "sensitive_keyword_detected"
    else:
        risk_reason="no_sensitive_keyword_detected"

    intent = detect_question_intent(normalized_question)

    should_retrieve = detect_should_retrieve(normalized_question)

    if should_retrieve:
        retrieval_reason="question_length_allows_retrieval"
    else:
        retrieval_reason="question_too_short_for_retrieval"
    
    policy_scope = detect_policy_scope(normalized_question)
    
    return QuestionAnalysis(
        intent=intent,
        risk_level=risk_level,
        complexity=complexity,
        normalized_question=normalized_question,
        should_retrieve=should_retrieve,
        policy_scope=policy_scope,
        risk_reason=risk_reason,
        retrieval_reason=retrieval_reason
    )