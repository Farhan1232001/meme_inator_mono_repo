from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod

from apps.payments.domain.entities.payment_entity import PaymentEntity
from apps.payments.domain.entities.token_transaction_entity import TokenTransaction
from apps.payments.domain.entities.token_wallet_entity import TokenWallet

class IWalletService(ABC):
    """
    Interface for handling all token-based value movements.
    Enforces wallet invariants and creates TokenTransaction records.
    """

    @abstractmethod
    def add_funds(
        self,
        user_id: UUID,
        amount: int,
        *,
        payment: Optional[PaymentEntity] = None,
        description: str,
    ) -> TokenTransaction:
        """
        Deposit tokens into a user's wallet.
        Used for consumable purchases or promotions.
        """
        ...

    @abstractmethod
    def spend_funds(
        self,
        user_id: UUID,
        amount: int,
        *,
        description: str,
    ) -> TokenTransaction:
        """
        Withdraw tokens from a wallet.
        Raises InsufficientFundsException if balance would go negative.
        """
        ...

    @abstractmethod
    def get_wallet(self, user_id: UUID) -> TokenWallet:
        """
        Fetch or lazily create a wallet for the user.
        """
        ...