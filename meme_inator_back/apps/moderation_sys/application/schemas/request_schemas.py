# application/dtos/request_schemas.py
from ninja import Schema
from uuid import UUID
from typing import Optional

class HumanModerationRequestSchema(Schema):
    """Request schema for human moderation decision."""
    case_id: UUID
    decision: str  # ACCEPT, REJECT, FLAG
    note: Optional[str] = None


class SubmitAppealRequestSchema(Schema):
    """Request schema for submitting an appeal."""
    case_id: UUID
    reason: str


class ResolveAppealRequestSchema(Schema):
    """Request schema for resolving an appeal."""
    case_id: UUID
    outcome: str  # APPROVED, DENIED
    resolution_note: Optional[str] = None


class UpdatePolicyRequestSchema(Schema):
    """Request schema for updating moderation policy."""
    policy_id: UUID
    thresholds: Optional[dict] = None
    appeal_rules: Optional[dict] = None