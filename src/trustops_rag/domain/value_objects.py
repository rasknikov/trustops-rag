from enum import StrEnum

class QueryStatus(StrEnum):
    ANSWERED = "answered"
    ANSWERED_WITH_WARNING = "answered_with_warning"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    BLOCKED = "blocked"
    FAILED_SAFE = "failed_safe"

class TicketStatus(StrEnum):
    PENDING_REVIEW = "pending_review"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELED = "canceled"