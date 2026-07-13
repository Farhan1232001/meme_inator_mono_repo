# domain/entities/moderation_attempt_entity.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid7
from typing import Optional

@dataclass
class ModerationAttemptEntity:
    attempt_id: UUID = field(default_factory=uuid7)
    moderator_id: Optional[str] = None
    decision: Optional[str] = None
    note: Optional[str] = None
    attempted_at: datetime = field(default_factory= datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    resolution_note: Optional[str] = None