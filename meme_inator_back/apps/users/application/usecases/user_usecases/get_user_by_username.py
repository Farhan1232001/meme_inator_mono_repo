from typing import Optional

from apps.users.domain.entities.user_entity import UserEntity
from apps.users.domain.usecases.user_usecases.get_user_by_username import IGetUserByUsernameUseCase
from apps.users.domain.irepositories.user_repository import IUserRepository

class GetUserByUsernameUseCase(IGetUserByUsernameUseCase):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def execute(self, username: str) -> Optional[UserEntity]:
        return self.user_repo.get_by_username(username)