from dataclasses import dataclass
from uuid import UUID


@dataclass
class PolicyRuleEntity:
    rule_id: UUID
    name: str
    expression: str  # domain-specific expression language / JSONLogic etc.
    priority: int
    is_active: bool
