from dataclasses import dataclass

@dataclass
class ReviewTaskPayload:
    ticket_id: str
    attempt_number: int

@dataclass
class ReviewTaskExecutionResult:
    task_id: str
    ticket_id: str
    status: str
    attempt_number: int