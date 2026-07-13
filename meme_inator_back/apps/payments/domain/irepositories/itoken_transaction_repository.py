from abc import ABC, abstractmethod

from apps.payments.domain.entities.token_transaction_entity import TokenTransaction


class ITokenTransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: TokenTransaction) -> TokenTransaction:
        pass