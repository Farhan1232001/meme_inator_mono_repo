from typing import List, Optional, Literal
from uuid import UUID
from core.results import Result, Ok, NotOk, Error

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from apps.profiles.infrastructure.models.profile_model import ProfileModel
from apps.users.domain.entities.user_entity import UserEntity
from apps.users.domain.entities.friend_request_entity import FriendRequestEntity
from apps.users.domain.enums.friend_request_status import FriendRequestStatus
from apps.users.domain.irepositories.friend_request_repository import IFriendRequestRepository
from apps.users.domain.irepositories.ifriendship_repository import IFriendshipRepository
from apps.users.infrastructure.models.fellowship_model import FellowshipModel
from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.repositories.user_repository import UserRepository
from apps.users.infrastructure.user_mappers import user_model_to_entity


# TODO: Utilize the interface for this class, update interface so taht it reflects impl. 
class SocialActionsRepository:
    def __init__(
        self,
        friend_req_repo: IFriendRequestRepository,
        friendship_repo: IFriendshipRepository,
        user_repo: UserRepository
    ):
        self.friend_req_repo = friend_req_repo
        self.friendship_repo = friendship_repo
        self.user_repo = user_repo

    # ---------- Following (Fellowships) ----------
    # TODO: Can queries be reduced? checking existence of follower & target, can it happen in one query?
    def follow_user(self, follower_id: UUID, target_id: UUID) -> Result[None]:
        """Create a follow relationship.
        Returns Ok(None) on success, NotOk(409) if already following.
        """
        if follower_id == target_id:
            return NotOk(
                message="Users cannot follow themselves.",
                static_msg="SELF_FOLLOW",
                status_code=400
            )

        with transaction.atomic():
            # Fetch users (will raise 404 if missing – you may want to catch and return NotOk)
            try:
                follower = UserModel.objects.get(id=follower_id)
                target = UserModel.objects.get(id=target_id)
            except UserModel.DoesNotExist:
                return NotOk(
                    message="One or both users not found.",
                    static_msg="USER_NOT_FOUND",
                    status_code=404
                )
            except Exception as e:
                return Error(
                    message="Failed to fetch users",
                    static_msg="USER_FETCH_ERROR",
                    exception=e,
                    status_code=500
                )


            # Check if already actively following
            existing = FellowshipModel.objects.filter(
                user=follower, followed_user=target, is_soft_deleted=False
            ).first()
            if existing:
                return NotOk(
                    message="Already following this user.",
                    static_msg="ALREADY_FOLLOWING",
                    status_code=409
                )

            # Try to reactivate a soft‑deleted fellowship, else create new
            fellowship, created = FellowshipModel.objects.get_or_create(
                user=follower,
                followed_user=target,
                defaults={"is_soft_deleted": False}
            )
            if not created and fellowship.is_soft_deleted:
                fellowship.is_soft_deleted = False
                fellowship.save(update_fields=["is_soft_deleted"])

            # Increment counters
            ProfileModel.objects.filter(user=follower).update(following_count=F("following_count") + 1)
            ProfileModel.objects.filter(user=target).update(followers_count=F("followers_count") + 1)

        return Ok(None)

    # TODO: Can queries be reduced? checking existence of follower & target, can it happen in one query?
    def unfollow_user(self, follower_id: UUID, target_id: UUID) -> Result[None]:
        """Remove a follow relationship.
        Returns Ok(None) on success, NotOk(404) if not following.
        """
        with transaction.atomic():
            try:
                follower = UserModel.objects.get(id=follower_id)
                target = UserModel.objects.get(id=target_id)
            except UserModel.DoesNotExist:
                return NotOk(
                    message="One or both users not found.",
                    static_msg="USER_NOT_FOUND",
                    status_code=404
                )
            except Exception as e:
                return Error(
                    message="Failed to fetch users",
                    static_msg="USER_FETCH_ERROR",
                    exception=e,
                    status_code=500
                )

            # Find active fellowship
            fellowship = FellowshipModel.objects.filter(
                user=follower, followed_user=target, is_soft_deleted=False
            ).first()
            if not fellowship:
                return NotOk(
                    message="Not following this user.",
                    static_msg="NOT_FOLLOWING",
                    status_code=404
                )

            # Soft delete
            fellowship.is_soft_deleted = True
            fellowship.save(update_fields=["is_soft_deleted"])

            # Decrement counters
            ProfileModel.objects.filter(user=follower).update(following_count=F("following_count") - 1)
            ProfileModel.objects.filter(user=target).update(followers_count=F("followers_count") - 1)

        return Ok(None)

    def get_followers(self, user_id: UUID) -> List[UserEntity]:
        """Return all users who follow the given user."""
        target = get_object_or_404(UserModel, id=user_id)
        fellowships = FellowshipModel.objects.filter(
            followed_user=target, is_soft_deleted=False
        ).select_related("user")
        return [user_model_to_entity(f.user) for f in fellowships]

    def get_following(self, user_id: UUID) -> List[UserEntity]:
        """Return all users that the given user follows."""
        follower = get_object_or_404(UserModel, id=user_id)
        fellowships = FellowshipModel.objects.filter(
            user=follower, is_soft_deleted=False
        ).select_related("followed_user")
        return [user_model_to_entity(f.followed_user) for f in fellowships]

    
    def is_following(self, follower_id: UUID, target_id: UUID) -> bool:
        """Return True if an active follow relationship exists."""
        return FellowshipModel.objects.filter(
            user_id=follower_id,
            followed_user_id=target_id,
            is_soft_deleted=False
        ).exists()
    # ---------- Friend Requests (unchanged, but keep as is) ----------
    def _map_to_friend_request_entity(self, req_instance):
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        return FriendRequestEntity(
            id=req_instance.id,
            sender_id=req_instance.sender_id,
            receiver_id=req_instance.receiver_id,
            created_at=req_instance.created_at,
            status=FriendRequestStatus(req_instance.status),
            updated_at=req_instance.updated_at,
            expires_at=req_instance.expires_at,
        )

    def create_friend_request(self, sender_id: UUID, receiver_id: UUID) -> FriendRequestEntity:
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        req = FriendRequestModel.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            status='pending'
        )
        return self._map_to_friend_request_entity(req)

    def get_friend_requests(
        self,
        user_id: UUID,
        type: Literal['incoming', 'outgoing']
    ) -> List[FriendRequestEntity]:
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        if type == 'incoming':
            qs = FriendRequestModel.objects.filter(receiver_id=user_id, status='pending')
        else:
            qs = FriendRequestModel.objects.filter(sender_id=user_id, status='pending')
        return [self._map_to_friend_request_entity(req) for req in qs]

    def update_friend_request_status(self, request_id: UUID, status: str) -> Optional[FriendRequestEntity]:
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        try:
            req = FriendRequestModel.objects.get(id=request_id)
            req.status = status
            req.save()
            return self._map_to_friend_request_entity(req)
        except FriendRequestModel.DoesNotExist:
            return None

    def delete_friend_request(self, request_id: UUID) -> None:
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        FriendRequestModel.objects.filter(id=request_id).delete()

    def remove_friend(self, user_id: UUID, friend_id: UUID) -> None:
        from django.db.models import Q
        from apps.users.infrastructure.models.friend_request_model import FriendRequestModel
        FriendRequestModel.objects.filter(
            Q(sender_id=user_id, receiver_id=friend_id) |
            Q(sender_id=friend_id, receiver_id=user_id)
        ).delete()