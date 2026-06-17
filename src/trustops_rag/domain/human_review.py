from dataclasses import dataclass

@dataclass
class HumanReviewInput:
    query_id: str
    decision_reason: str
    risk_level: str
    policy_version: str

@dataclass
class HumanReviewTicket:
    ticket_id: str
    query_id: str
    status: str
    reason: str
    worker_action: str

@dataclass
class HumanReviewTask:
    task_id: str
    ticket_id: str
    action: str
    status: str

def create_review_task(ticket: HumanReviewTicket) -> HumanReviewTask:
    return HumanReviewTask(
        task_id=f"task-{ticket.ticket_id}",
        ticket_id=ticket.ticket_id,
        action=ticket.worker_action,
        status="queued"
    )

def validate_human_review_input(review_input: HumanReviewInput) -> None:
    if not review_input.query_id.strip():
        raise ValueError("Query id cannot be empty.")
    
    if not review_input.decision_reason.strip():
        raise ValueError("Decision reason cannot be empty.")
    
    if not review_input.risk_level.strip():
        raise ValueError("Risk level cannot be empty.")
    
    if not review_input.policy_version.strip():
        raise ValueError("Policy version cannot be empty.")
    
def build_review_reason(review_input: HumanReviewInput) -> str:
    return f"{review_input.decision_reason}:{review_input.risk_level}:{review_input.policy_version}"

def open_review_ticket(review_input: HumanReviewInput) -> HumanReviewTicket:
    
    validate_human_review_input(review_input)

    reason = build_review_reason(review_input)
    
    return HumanReviewTicket(
        ticket_id=f"review-{review_input.query_id}",
        query_id=review_input.query_id,
        status="pending_review",
        reason=reason,
        worker_action="queue_for_review"
    )