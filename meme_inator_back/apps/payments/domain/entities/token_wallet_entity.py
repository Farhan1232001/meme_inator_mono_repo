from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from apps.payments.domain.exceptions import InsufficientFundsException



@dataclass
class TokenWallet:
    user_id: UUID
    balance: int
    updated_at: datetime

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.updated_at = datetime.now(timezone.utc)

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise InsufficientFundsException(f"User {self.user_id} has insufficient funds.")
        self.balance -= amount
        self.updated_at = datetime.now(timezone.utc)