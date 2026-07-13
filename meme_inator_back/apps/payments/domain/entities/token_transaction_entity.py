from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class TokenTransaction:
    # 1. Linking
    user_id: UUID
    wallet_id: UUID
    payment_id: Optional[UUID]

    # 2. Movement
    amount: int         # +500 (bought) & -500 (spent)
    description: str    # "bought 500 pack", "Used on SuperLike"
    created_at: datetime