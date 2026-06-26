from trustops_rag.domain.human_review import HumanReviewTicket
from trustops_rag.workers.review_payloads import ReviewTaskPayload
from trustops_rag.workers.review_worker import process_review_ticket, run_review_task


def test_process_review_ticket_returns_human_review_task() -> None:
    ticket = HumanReviewTicket(
        ticket_id="review-q-1",
        query_id="q-1",
        status="pending_review",
        reason="needs_review:high:v1",
        worker_action="queue_for_review",
    )

    task = process_review_ticket(ticket)

    assert task.ticket_id == "review-q-1"
    assert task.action == "queue_for_review"
    assert task.status == "queued"


def test_process_review_ticket_raises_error_for_blank_worker_action() -> None:
    ticket = HumanReviewTicket(
        ticket_id="review-q-1",
        query_id="q-1",
        status="pending_review",
        reason="needs_review:high:v1",
        worker_action="   ",
    )

    try:
        process_review_ticket(ticket)
    except ValueError as error:
        assert str(error) == "worker_action cannot be empty."
        return

    raise AssertionError("Expected ValueError for blank worker_action.")


def test_run_review_task_returns_execution_result() -> None:
    payload = ReviewTaskPayload(
        ticket_id="review-q-1",
        attempt_number=1,
    )
    ticket = HumanReviewTicket(
        ticket_id="review-q-1",
        query_id="q-1",
        status="pending_review",
        reason="needs_review:high:v1",
        worker_action="queue_for_review",
    )

    result = run_review_task(payload, ticket)

    assert result.task_id == "task-review-q-1"
    assert result.ticket_id == ticket.ticket_id
    assert result.status == "queued"
    assert result.attempt_number == 1
