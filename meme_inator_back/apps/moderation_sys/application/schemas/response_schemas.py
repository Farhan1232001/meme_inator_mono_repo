# application/dtos/response_schemas.py
from ninja import Schema
from uuid import UUID
from datetime import datetime
from typing import Optional

class ModerationCaseResponseSchema(Schema):
    case_id: UUID
    status: str
    decision: Optional[str]
    confidence_score: Optional[float]
    created_at: datetime
    decided_at: Optional[datetime]

class AppealResponseSchema(Schema):
    appeal_id: UUID
    status: str
    submitted_at: datetime