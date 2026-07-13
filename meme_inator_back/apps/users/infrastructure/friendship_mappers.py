from apps.users.domain.entities.friend_request_entity import FriendRequestEntity
from apps.users.domain.entities.friendship_entity import FriendshipEntity
from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
from apps.users.infrastructure.models.friendship_model import FriendshipModel
from apps.users.domain.enums.friend_request_status import FriendRequestStatus

class FriendRequestMapper:
    @staticmethod
    def to_entity(model: FriendRequestModel) -> FriendRequestEntity:
        return FriendRequestEntity(
            id=model.id,
            sender_id=model.sender_id,
            receiver_id=model.receiver_id,
            created_at=model.created_at,
            status=FriendRequestStatus(model.status),
            updated_at=model.updated_at,
            expires_at=model.expires_at,
        )

    @staticmethod
    def to_model(entity: FriendRequestEntity, model: FriendRequestModel = None) -> FriendRequestModel:
        if model is None:
            model = FriendRequestModel()
        model.id = entity.id
        model.sender_id = entity.sender_id
        model.receiver_id = entity.receiver_id
        model.status = entity.status.value
        model.created_at = entity.created_at
        model.updated_at = entity.updated_at
        model.expires_at = entity.expires_at
        return model

class FriendshipMapper:
    @staticmethod
    def to_entity(model: FriendshipModel) -> FriendshipEntity:
        return FriendshipEntity(
            id=model.id,
            user=model.user_id,
            friend=model.friend_id,
            started_at=model.started_at,
        )

    @staticmethod
    def to_model(entity: FriendshipEntity, model: FriendshipModel = None) -> FriendshipModel:
        if model is None:
            model = FriendshipModel()
        model.id = entity.id
        model.user_id = entity.user
        model.friend_id = entity.friend
        model.started_at = entity.started_at
        return model