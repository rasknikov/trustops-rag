from trustops_rag.domain.human_review import HumanReviewTicket


def validate_ticket(ticket: HumanReviewTicket) -> None:
    if not ticket.ticket_id.strip():
        raise ValueError("ticket_id cannot be empty.")

    if not ticket.query_id.strip():
        raise ValueError("query_id cannot be empty.")

    if not ticket.worker_action.strip():
        raise ValueError("worker_action cannot be empty.")
