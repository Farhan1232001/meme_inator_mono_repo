from datetime import datetime, timezone
from uuid import UUID
from typing import Optional

from apps.payments.domain.entities.payment_entity import PaymentEntity
from apps.payments.domain.entities.token_transaction_entity import TokenTransaction
from apps.payments.domain.entities.token_wallet_entity import TokenWallet
from apps.payments.domain.irepositories.itoken_transaction_repository import ITokenTransactionRepository
from apps.payments.domain.irepositories.itoken_wallet_repository import ITokenWalletRepository
from apps.payments.domain.iservices.iwallet_service import IWalletService



class WalletService(IWalletService):
    """
    Handles all token-based value movements.
    Enforces wallet invariants and creates TokenTransaction records.
    """
    def __init__(
            self, 
            wallet_repo: ITokenWalletRepository, 
            transaction_repo: ITokenTransactionRepository
        ):
        self.wallet_repo = wallet_repo
        self.transaction_repo = transaction_repo

    def grant_tokens(self, user_id: UUID, amount: int) -> None:
        """
        Entry point from FulfillmentService for consumable purchases.
        """
        wallet = self.get_wallet(user_id)
        
        # Logic: Increment balance
        wallet.balance += amount
        self.wallet_repo.save(wallet)

        # Audit: Log the transaction
        self.transaction_repo.create_log(
            user_id=user_id,
            type="PURCHASE",
            amount=amount,
            description=f"Purchased {amount} tokens"
        )

    def get_wallet(self, user_id: UUID) -> TokenWallet:
        # Lazy creation pattern
        wallet = self.wallet_repo.find_by_user_id(user_id)
        if not wallet:
            wallet = TokenWallet(user_id=user_id, balance=0)
        return wallet
    
    def add_funds(
        self,
        user_id: UUID,
        amount: int,
        *,
        payment: Optional[PaymentEntity] = None,
        description: str,
    ) -> TokenTransaction:
        wallet = self.get_wallet(user_id)
        
        # Update Entity State
        wallet.deposit(amount)
        self.wallet_repo.save(wallet)

        # Create Audit Log
        transaction = TokenTransaction(
            user_id=user_id,
            wallet_id=user_id, # Usually wallet_id is user_id in 1:1 mappings
            payment_id=payment.id if payment else None,
            amount=amount,
            description=description,
            created_at=datetime.now(timezone.utc)
        )
        return self.transaction_repo.save(transaction)

    def spend_funds(
        self,
        user_id: UUID,
        amount: int,
        *,
        description: str,
    ) -> TokenTransaction:
        wallet = self.get_wallet(user_id)
        
        # This will raise InsufficientFundsException if balance is too low
        wallet.withdraw(amount)
        self.wallet_repo.save(wallet)

        # Create Audit Log (Negative amount to show withdrawal)
        transaction = TokenTransaction(
            user_id=user_id,
            wallet_id=user_id,
            payment_id=None,
            amount=-amount, 
            description=description,
            created_at=datetime.now(timezone.utc)
        )
        return self.transaction_repo.save(transaction)