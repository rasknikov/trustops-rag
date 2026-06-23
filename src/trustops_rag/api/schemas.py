from pydantic import BaseModel, field_validator


class AskRequest(BaseModel):
    question: str
    tenant_id: str
    user_id: str

    @field_validator("question", "tenant_id", "user_id")
    @classmethod
    def validate_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field cannot be blank")
        
        return value


class AskResponse(BaseModel):
    status: str
    decision_reason: str
    risk_level: str | None
    complexity: str | None