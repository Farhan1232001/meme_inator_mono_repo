from uuid import UUID
from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist

from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.domain.entities.friendship_entity import FriendshipEntity
from apps.users.infrastructure.models.friendship_model import FriendshipModel
from apps.users.infrastructure.friendship_mappers import FriendshipMapper

class FriendshipRepository(IFriendshipRepository):
    def create(self, friendship: FriendshipEntity) -> FriendshipEntity:
        model = FriendshipMapper.to_model(friendship)
        model.save()
        return FriendshipMapper.to_entity(model)

    def get_by_users(self, user_a_id: UUID, user_b_id: UUID) -> Optional[FriendshipEntity]:
        try:
            model = FriendshipModel.objects.get(
                user=user_a_id, friend=user_b_id, is_soft_deleted=False
            )
            return FriendshipMapper.to_entity(model)
        except ObjectDoesNotExist:
            return None

    def list_active_for_user(self, user_id: UUID) -> List[FriendshipEntity]:
        models = FriendshipModel.objects.filter(
            user=user_id, is_soft_deleted=False
        )
        return [FriendshipMapper.to_entity(m) for m in models]

    def end_friendship(self, friendship_id: UUID) -> None:
        FriendshipModel.objects.filter(id=friendship_id).update(is_soft_deleted=True)

    def exists(self, user_a_id: UUID, user_b_id: UUID) -> bool:
        return FriendshipModel.objects.filter(
            user=user_a_id, friend=user_b_id, is_soft_deleted=False
        ).exists()