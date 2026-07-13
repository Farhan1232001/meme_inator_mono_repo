from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from payments.domain.entities.token_wallet_entity import TokenWalletEntity


class ITokenWalletRepository(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: UUID) -> Optional[TokenWalletEntity]:
        raise NotImplementedError

    @abstractmethod
    def save(self, wallet: TokenWalletEntity) -> TokenWalletEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, wallet: TokenWalletEntity) -> TokenWalletEntity:
        raise NotImplementedError
