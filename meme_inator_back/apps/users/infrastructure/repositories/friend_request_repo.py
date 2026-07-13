from time import timezone
from typing import Optional, List
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.db.models import Q
from apps.users.domain.entities.friend_request_entity import FriendRequestEntity
from apps.users.domain.irepositories.friend_request_repository import IFriendRequestRepository
from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequestRepository(IFriendRequestRepository):

    # -----------------------------
    # Utility: convert model → entity
    # -----------------------------
    def _to_entity(self, model: FriendRequestModel) -> FriendRequestEntity:
        return FriendRequestEntity(
            id=model.id,
            sender_id=model.sender_id,
            receiver_id=model.receiver_id,
            status=model.status,
            created_at=model.created_at,
        )

    # -----------------------------
    # Create request
    # -----------------------------
    def create_friend_request(self, sender_id: UUID, receiver_id: UUID) -> FriendRequestEntity:
        if sender_id == receiver_id:
            raise ValueError("Users cannot send friend requests to themselves.")

        # Validate users exist
        if not User.objects.filter(id=sender_id).exists():
            raise ValueError("Sender user does not exist.")
        if not User.objects.filter(id=receiver_id).exists():
            raise ValueError("Receiver user does not exist.")

        # Ensure no existing pending request
        existing = FriendRequestModel.objects.filter(
            sender_id=sender_id, receiver_id=receiver_id
        ).first()
        if existing:
            raise ValueError("A friend request already exists between these users.")

        try:
            friend_request = FriendRequestModel.objects.create(
                sender_id=sender_id,
                receiver_id=receiver_id,
                status="pending",
            )
            return self._to_entity(friend_request)

        except IntegrityError:
            raise ValueError("Friend request already exists (unique constraint).")

    # -----------------------------
    # Get by ID
    # -----------------------------
    def get_by_id(self, request_id: int) -> Optional[FriendRequestEntity]:
        try:
            model = FriendRequestModel.objects.get(id=request_id)
            return self._to_entity(model)
        except FriendRequestModel.DoesNotExist:
            return None

    # -----------------------------
    # Get pending request
    # -----------------------------
    def get_pending_request(self, sender_id: UUID, receiver_id: UUID) -> Optional[FriendRequestEntity]:
        model = FriendRequestModel.objects.filter(
            sender_id=sender_id,
            receiver_id=receiver_id,
            status="pending",
        ).first()
        return self._to_entity(model) if model else None

    # -----------------------------
    # List received
    # -----------------------------
    def list_received_requests(self, user_id: UUID) -> List[FriendRequestEntity]:
        models = FriendRequestModel.objects.filter(receiver_id=user_id)
        return [self._to_entity(m) for m in models]

    # -----------------------------
    # List sent
    # -----------------------------
    def list_sent_requests(self, user_id: UUID) -> List[FriendRequestEntity]:
        models = FriendRequestModel.objects.filter(sender_id=user_id)
        return [self._to_entity(m) for m in models]

    # -----------------------------
    # Update status
    # -----------------------------
    def update_status(self, request_id: UUID, status: str) -> FriendRequestEntity:
        if status not in ["pending", "accepted", "rejected", "cancelled"]:
            raise ValueError("Invalid friend request status.")

        try:
            model = FriendRequestModel.objects.get(id=request_id)
            model.status = status
            model.save()
            return self._to_entity(model)
        except FriendRequestModel.DoesNotExist:
            raise ValueError("Friend request not found.")

    # -----------------------------
    # Delete request
    # -----------------------------
    def delete_request(self, request_id: UUID) -> None:
        FriendRequestModel.objects.filter(id=request_id).delete()
    
    def delete_request_between(self, user1_id: UUID, user2_id: UUID) -> None:
        FriendRequestModel.objects.filter(
            Q(sender_id=user1_id, receiver_id=user2_id) |
            Q(sender_id=user2_id, receiver_id=user1_id)
        ).delete()

    # -----------------------------
    # Check any request exists
    # -----------------------------
    def exists_between(self, user1_id: UUID, user2_id: UUID) -> bool:
        return FriendRequestModel.objects.filter(
            sender_id=user1_id, receiver_id=user2_id
        ).exists() or FriendRequestModel.objects.filter(
            sender_id=user2_id, receiver_id=user1_id
        ).exists()
    
    def expire_old_requests(self) -> int:
        """
        Mark expired pending requests as EXPIRED and return count.
        """
        now = timezone.now()
        expired_requests = FriendRequestModel.objects.filter(
            status="pending",
            expires_at__lt=now
        )
        count = expired_requests.count()
        expired_requests.update(status="expired")
        return count