from trustops_rag.domain.human_review import (
    HumanReviewTask,
    HumanReviewTicket,
    create_review_task,
)
from trustops_rag.workers.review_validation import validate_ticket
from trustops_rag.workers.review_payloads import ReviewTaskPayload, ReviewTaskExecutionResult




def process_review_ticket(ticket: HumanReviewTicket) -> HumanReviewTask:
    validate_ticket(ticket)

    return create_review_task(ticket)


def run_review_task(payload: ReviewTaskPayload, ticket: HumanReviewTicket) -> ReviewTaskExecutionResult:
    task = process_review_ticket(ticket)
    return ReviewTaskExecutionResult(
        task_id=task.task_id,
        ticket_id=task.ticket_id,
        status=task.status,
        attempt_number=payload.attempt_number,
    )