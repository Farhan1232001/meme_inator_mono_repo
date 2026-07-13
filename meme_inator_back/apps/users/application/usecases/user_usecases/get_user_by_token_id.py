from typing import Optional
from uuid import UUID

from apps.users.domain.entities.user_entity import UserEntity
from apps.users.domain.usecases.user_usecases.get_user_by_token_id import IGetUserByTokenIdUseCase
from apps.users.domain.irepositories.user_repository import IUserRepository

class GetUserByTokenIdUseCase(IGetUserByTokenIdUseCase):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: UUID) -> Optional[UserEntity]:
        return self.user_repo.get_by_id(user_id)