from fastapi import APIRouter

from trustops_rag.application.ask import AskInput, handle_ask
from trustops_rag.api.schemas import AskRequest, AskResponse


router = APIRouter()


@router.post(
            "/ask",
             response_model=AskResponse,
             status_code=200, 
             summary="Process an ask request",
             tags=["ask"]
)
def ask(request: AskRequest) -> AskResponse:
    ask_input = AskInput(
        question=request.question,
        tenant_id=request.tenant_id,
        user_id=request.user_id
    )

    result = handle_ask(ask_input)

    return AskResponse(
        status=result.status,
        decision_reason=result.decision_reason,
        risk_level=result.risk_level,
        complexity=result.complexity,
    )