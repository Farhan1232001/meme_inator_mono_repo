# core/dependency_injections.py
# TODO: Refactor this file to use python-dependency-injector or Ninja extra's lightweight DI system




class CoreDependencyProvider:
    """Centralized dependency injection container.
    Dependency Injection, how it works in this layer achtecture.

    orchestration 
            -> irepositories (infastructure/data) 
                    -> instances required by irepositories
    """

    def __init__(self):
        # TODO: Why are the orchestrations being saved?
        self._authorization_orchestration = None
        self.comment_sections_orchestration = None
        self._feeds_orchestration = None
        self._init_app_sys = None
        self._posts_orchestration = None
        self._profiles_orchestration = None
        self._registration_orchestration = None
        self._users_orchestration = None
        self._moderation_orchestration = None


    # --- Public Dependency Getters ---
    def create_registration_orchestration(self):
        """
        Lazily build and return a RegistrationOrchestration instance.
        Uses local imports to avoid circular import issues during Django startup.
        """
        from apps.profiles.application.usecases.create_user_profile_usecase import CreateUserProfileUsecase
        from apps.registration.application.orchestration.registration_orchestration import RegistrationOrchestration
        from apps.registration.application.usecases.user_register_usecase import UserRegisterUsecase
        from apps.profiles.infrastructure.repositories.profile_repository import ProfileRepository
        from apps.registration.application.usecases.create_registration_intent_token_usecase import CreateRegistrationIntentTokenUsecase
        from apps.registration.application.usecases.registration_verification_usecase import RegistrationVerificationUsecase
        from apps.registration.infrastructure.repositories.registration_intent_token_repository import RegistrationIntentTokenRepository


        self._registration_orchestration = RegistrationOrchestration(
            register_user_usecase=UserRegisterUsecase(),
            create_profile_usecase=CreateUserProfileUsecase(
                profile_repo=ProfileRepository()
            ),
            create_registration_intent_token_usecase=CreateRegistrationIntentTokenUsecase(),
            registration_verification_usecase=RegistrationVerificationUsecase(
                registration_intent_token_repo=RegistrationIntentTokenRepository()
            )
        )

        return self._registration_orchestration

    def create_feeds_orchestration(self):
        from apps.feeds.application.orchestration.feeds_orchestration import FeedsOrchestration
        from apps.feeds.application.usecases.get_gridfeed_page_usecase import GetGridfeedPageUsecase
        from apps.feeds.application.usecases.get_sectionalfeed_page_usecase import GetSectionalfeedPageUsecase
        from apps.feeds.infrastructure.repositories.gridfeed_repository import GridfeedRepository
        from apps.feeds.application.hydrator import PostHydrator
        from apps.feeds.infrastructure.services.feeds_s3_service import FeedsS3Service
        from apps.feeds.infrastructure.repositories.sectionalfeed_repository import SectionalfeedRepository
        from apps.feeds.infrastructure.models.gridfeeds_model import GridfeedsModel
        from apps.feeds.infrastructure.models.sectionalfeeds_model import SectionalFeedsModel

        if self._feeds_orchestration != None: return self._feeds_orchestration

        self._feeds_orchestration = FeedsOrchestration(
            # init Get Gridfeed Usecase
            get_gridfeed_usecase=GetGridfeedPageUsecase(
                repository=GridfeedRepository(
                    gridfeeds_model=GridfeedsModel() # TODO: should models take in instance or class?
                ),
                post_hydrator=PostHydrator(
                    s3_service=FeedsS3Service(
                        bucket_name="dummy",
                        aws_client=None
                    )
                ),
            ),

            # init Get sectionalfeed usecase
            get_sectional_feed_usecase=GetSectionalfeedPageUsecase(
                repository=SectionalfeedRepository(
                    sectionalfeed_model=SectionalFeedsModel() # TODO: should models take in instance or class?
                ),
                post_hydrator=PostHydrator(
                    s3_service=FeedsS3Service(
                        bucket_name="dummy",
                        aws_client=None
                    )
                ),
            )
        )

        return self._feeds_orchestration

    def create_authorization_orchestration(self):
            """
            Lazily build and return the AuthorizationOrchestration instance.
            """
            from apps.authorization.infrastructure.repositories.django_authorization_repository import DjangoAuthorizationRepository
            from apps.authorization.application.orchestration.authz_orchestration import AuthorizationOrchestration
            from apps.authorization.application.usecases.assign_permission_to_role_usecase import AssignPermissionToRoleUseCase
            from apps.authorization.application.usecases.assign_role_to_user_usecase import AssignRoleToUserUseCase
            from apps.authorization.application.usecases.bootstrap_roles_and_permissions_usecase import BootstrapRolesAndPermissionsUseCase
            from apps.authorization.application.usecases.can_user_perform_action_usecase import CanUserPerformActionUseCase
            from apps.authorization.application.usecases.compute_effective_permissions_usecase import ComputeEffectivePermissionsUseCase
            from apps.authorization.application.usecases.create_object_acl_usecase import CreateObjectACLUseCase
            from apps.authorization.application.usecases.create_permission_usecase import CreatePermissionUseCase
            from apps.authorization.application.usecases.grant_entitlement_usecase import GrantEntitlementUseCase
            from apps.authorization.application.usecases.remove_permission_from_role_usecase import RemovePermissionFromRoleUseCase
            from apps.authorization.application.usecases.remove_role_from_user_usecase import RemoveRoleFromUserUseCase
            from apps.authorization.application.usecases.restore_purchases_usecase import RestorePurchasesUseCase
            from apps.authorization.application.usecases.revoke_entitlement_usecase import RevokeEntitlementUseCase

            # Initialize Shared Repository
            auth_repo = DjangoAuthorizationRepository()

            # Build Orchestration
            self._authorization_orchestration = AuthorizationOrchestration(
                bootstrap_use_case=BootstrapRolesAndPermissionsUseCase(repository=auth_repo),
                create_permission_use_case=CreatePermissionUseCase(repository=auth_repo),
                assign_permission_use_case=AssignPermissionToRoleUseCase(repository=auth_repo),
                remove_permission_use_case=RemovePermissionFromRoleUseCase(repository=auth_repo),
                can_perform_use_case=CanUserPerformActionUseCase(repository=auth_repo),
                assign_role_use_case=AssignRoleToUserUseCase(repository=auth_repo),
                remove_role_use_case=RemoveRoleFromUserUseCase(repository=auth_repo),
                compute_permissions_use_case=ComputeEffectivePermissionsUseCase(repository=auth_repo),
                create_acl_use_case=CreateObjectACLUseCase(repository=auth_repo),
                grant_entitlement_use_case=GrantEntitlementUseCase(repository=auth_repo),
                revoke_entitlement_use_case=RevokeEntitlementUseCase(repository=auth_repo),
                restore_purchases_use_case=RestorePurchasesUseCase(repository=auth_repo)
            )

            return self._authorization_orchestration
    

    def create_comment_sections_orchestration(self):
         
        from apps.commentsections.application.orchestration.comment_sections_orchestration import CommentSectionsOrchestration
        from apps.commentsections.application.usecases.add_comment_usecase import AddCommentUsecase
        from apps.commentsections.application.usecases.delete_comment_usecase import DeleteCommentUsecase
        from apps.commentsections.application.usecases.get_comment_thread_usecase import GetCommentThreadUsecase
        from apps.commentsections.application.usecases.get_comments_usecase import GetCommentsUsecase
        from apps.commentsections.application.usecases.update_comment_usecase import UpdateCommentUsecase
        from apps.commentsections.application.usecases.validate_comment_content_usecase import ValidateCommentContentUsecase
        from apps.commentsections.application.usecases.vote_on_comment_usecase import VoteOnCommentUsecase
        from apps.commentsections.infrastructure.repositories.django_comment_repository import DjangoCommentRepository
        from apps.posts.infrastructure.repositories.django_posts_repository import DjangoPostRepository
        from apps.commentsections.infrastructure.models.comments_model import CommentModel
        from apps.authorization.infrastructure.repositories.django_authorization_repository import UserModel
        from apps.posts.infrastructure.models.post_model import PostModel
        from apps.commentsections.infrastructure.repositories.django_comment_vote_repository import DjangoCommentVoteRepository
        from apps.commentsections.infrastructure.models.comment_vote_model import CommentVoteModel


        
        comment_repo = DjangoCommentRepository(
            comment_model=CommentModel,
            post_model=PostModel,
            user_model=UserModel
        )
        post_repo = DjangoPostRepository()
        comment_vote_repo = DjangoCommentVoteRepository(
            vote_model=CommentVoteModel,
            comment_model=CommentModel,
            user_model=UserModel
        )

        self.comment_sections_orchestration = CommentSectionsOrchestration(
            add_comment_uc = AddCommentUsecase(
                comment_repo=comment_repo,
                post_repo=post_repo
            ),
            delete_comment_uc = DeleteCommentUsecase(
                 comment_repo=comment_repo,
                 post_repo=post_repo
            ),
            get_comment_thread_uc = GetCommentThreadUsecase(
                 comment_repo=comment_repo
            ),
            get_comments_uc = GetCommentsUsecase(
                comment_repo=comment_repo,
                post_repo=post_repo
            ),
            update_comment_uc = UpdateCommentUsecase(
                comment_repo=comment_repo,
            ),
            validate_comment_content_uc = ValidateCommentContentUsecase(),
            vote_on_comment_uc = VoteOnCommentUsecase(
                comment_repo=comment_repo,
                comment_vote_repo=comment_vote_repo
            ),
        )

        return self.comment_sections_orchestration

    def create_posts_orchestration(self):
        from apps.posts.application.orchestration.posts_orchestration import PostsOrchestration
        from apps.posts.application.usecases.create_post_usecase import CreatePostUsecase
        from apps.posts.application.usecases.get_post_usecase import GetPostUsecase
        from apps.posts.application.usecases.delete_post_usecase import DeletePostUsecase
        from apps.posts.application.usecases.vote_on_post_usecase import VoteOnPostUsecase
        from apps.posts.infrastructure.repositories.django_post_vote_repository import DjangoPostVoteRepository
        from apps.posts.infrastructure.models.post_vote_model import PostVoteModel
        from apps.posts.infrastructure.models.post_model import PostModel
        from apps.authorization.infrastructure.repositories.django_authorization_repository import UserModel
        from apps.posts.infrastructure.repositories.django_posts_repository import DjangoPostRepository

        # Create repositories
        post_repo = DjangoPostRepository()
        post_vote_repo = DjangoPostVoteRepository(
            vote_model=PostVoteModel,
            post_model=PostModel,
            user_model=UserModel
        )
        
        # Create usecases
        create_post_uc = CreatePostUsecase(post_repo=post_repo)
        get_post_uc = GetPostUsecase(post_repo=post_repo)
        delete_post_uc = DeletePostUsecase(post_repo=post_repo)
        vote_on_post_uc = VoteOnPostUsecase(
            post_repo=post_repo,
            post_vote_repo=post_vote_repo
        )
        
        # Create orchestration
        self._posts_orchestration = PostsOrchestration(
            create_post_uc=create_post_uc,
            get_post_uc=get_post_uc,
            delete_post_uc=delete_post_uc,
            vote_on_post_uc=vote_on_post_uc,
        )
        
        return self._posts_orchestration
        

    def create_profiles_orchestration(self):
        """
        Lazily build and return a ProfilesOrchestration instance.
        """
        if self._profiles_orchestration is not None:
            return self._profiles_orchestration
        
        from apps.profiles.application.orchestration.profiles_orchestration import ProfilesOrchestration
        from apps.profiles.application.usecases.create_user_profile_usecase import CreateUserProfileUsecase
        from apps.profiles.application.usecases.get_my_profile_usecase import GetMyProfileUsecase
        from apps.profiles.application.usecases.get_profile_img_urls_usecase import GetProfileImageUrlsUsecase
        from apps.profiles.application.usecases.get_profile_posts_usecase import GetProfilePostsUsecase
        from apps.profiles.application.usecases.get_public_profile_usecase import GetPublicProfileUsecase
        from apps.profiles.application.usecases.patch_my_profile_usecase import PatchMyProfileUsecase
        from apps.profiles.application.usecases.replace_my_profile_usecase import ReplaceMyProfileUsecase
        from apps.profiles.application.usecases.sync_profile_media_usecase import SyncProfileMediaUsecase
        from apps.profiles.application.usecases.update_profile_counters_usecase import UpdateProfileCountersUsecase
        from apps.profiles.infrastructure.repositories.profile_repository import ProfileRepository
        from apps.users.application.usecases.followship_usecases.does_fellowship_exist_usecase_impl import DoesFollowshipExistUsecase
        from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository
        from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository
        from apps.users.infrastructure.repositories.friendship_repository import FriendshipRepository
        from apps.users.infrastructure.repositories.user_repository import UserRepository

        profile_repo = ProfileRepository()
        friend_request_repo = FriendRequestRepository()
        friendship_repo = FriendshipRepository()
        user_repo = UserRepository()
        social_actions_repo = SocialActionsRepository(
            friend_req_repo=friend_request_repo,
            friendship_repo=friendship_repo,
            user_repo=user_repo
        )

        self._profiles_orchestration = ProfilesOrchestration(
            get_public_profile_usecase=GetPublicProfileUsecase(profile_repo=profile_repo),
            get_my_profile_usecase=GetMyProfileUsecase(profile_repo=profile_repo),
            create_profile_usecase=CreateUserProfileUsecase(profile_repo=profile_repo),
            patch_my_profile_usecase=PatchMyProfileUsecase(profile_repo=profile_repo),
            replace_my_profile_usecase=ReplaceMyProfileUsecase(profile_repo=profile_repo),
            update_counters_usecase=UpdateProfileCountersUsecase(profile_repo=profile_repo),
            sync_media_usecase=SyncProfileMediaUsecase(profile_repo=profile_repo),
            get_profile_posts_usecase=GetProfilePostsUsecase(profile_repo=profile_repo),
            get_profile_image_urls_usecase=GetProfileImageUrlsUsecase(profile_repo=profile_repo),
            does_follow_exist_usecase=DoesFollowshipExistUsecase(social_actions_repo=social_actions_repo)
        )

        return self._profiles_orchestration

    def create_users_orchestration(self):
        """
        Lazily build and return a UserOrchestration instance.
        """
        if self._users_orchestration is not None:
            return self._users_orchestration
        
        from apps.users.application.orchestration.users_orchestration import UsersOrchestration
        from apps.users.infrastructure.repositories.user_repository import UserRepository
        from apps.users.application.usecases.user_usecases.get_user_by_token_id import GetUserByTokenIdUseCase
        from apps.users.application.usecases.user_usecases.get_user_by_username import GetUserByUsernameUseCase
        from apps.users.application.usecases.social_actions_usecases.friendrequest_usecases.cancel_friendrequest_usecase_impl import CancelFriendRequestUsecase
        from apps.users.application.usecases.social_actions_usecases.friendrequest_usecases.get_friendrequests_usecase_impl import GetFriendRequestsUsecase
        from apps.users.application.usecases.social_actions_usecases.friendrequest_usecases.handle_friendrequest_usecase_impl import HandleFriendRequestUsecase
        from apps.users.application.usecases.social_actions_usecases.friendrequest_usecases.remove_friendrequest_usecase_impl import RemoveFriendUsecase
        from apps.users.application.usecases.social_actions_usecases.friendrequest_usecases.send_friendrequest_usecase_impl import SendFriendRequestUsecase
        from apps.users.application.usecases.social_actions_usecases.follow_actions_usecases.follow_user_usecase_impl import FollowUserUsecase
        from apps.users.application.usecases.social_actions_usecases.follow_actions_usecases.get_followers_list_usecase_impl import GetFollowersListUsecase
        from apps.users.application.usecases.social_actions_usecases.follow_actions_usecases.get_following_list_usecase_impl import GetFollowingListUsecase
        from apps.users.application.usecases.social_actions_usecases.follow_actions_usecases.unfollow_user_usecase_impl import UnfollowUserUsecase
        from apps.users.infrastructure.repositories.friend_request_repo import FriendRequestRepository
        from apps.users.infrastructure.repositories.friendship_repository import FriendshipRepository
        from apps.users.infrastructure.repositories.social_actions_repository import SocialActionsRepository

        # Create repositories
        user_repo = UserRepository()
        friend_request_repo = FriendRequestRepository()
        friendship_repo = FriendshipRepository()
        
        # Create social actions repository with proper dependencies
        social_actions_repo = SocialActionsRepository(
            friend_req_repo=friend_request_repo,
            friendship_repo=friendship_repo,
            user_repo=user_repo
        )


        # Create usecases with correct dependencies
        self._users_orchestration = UsersOrchestration(
            get_user_by_token_id=GetUserByTokenIdUseCase(user_repo=user_repo),
            get_user_by_username=GetUserByUsernameUseCase(user_repo=user_repo),
            follow_user=FollowUserUsecase(social_actions_repo=social_actions_repo),
            unfollow_user=UnfollowUserUsecase(social_actions_repo=social_actions_repo),
            get_followers=GetFollowersListUsecase(social_actions_repo=social_actions_repo),
            get_following=GetFollowingListUsecase(social_actions_repo=social_actions_repo),
            send_friend_request=SendFriendRequestUsecase(friend_request_repo=friend_request_repo),
            get_friend_requests=GetFriendRequestsUsecase(friend_request_repo=friend_request_repo),
            handle_friend_request=HandleFriendRequestUsecase(
                friend_request_repo=friend_request_repo,
                friendship_repo=friendship_repo
            ),
            cancel_friend_request=CancelFriendRequestUsecase(friend_request_repo=friend_request_repo),
            remove_friend=RemoveFriendUsecase(
                friendship_repo=friendship_repo,
                friend_request_repo=friend_request_repo
            ),
        )


        return self._users_orchestration

    

    def create_moderation_orchestration(self):
        """
        Lazily build and return a ModerationOrchestration instance.
        All dependencies (repositories, services, use cases) are instantiated here.
        """
        if hasattr(self, '_moderation_orchestration') and self._moderation_orchestration is not None:
            return self._moderation_orchestration

        # -------------------------------------------------------------------------
        # Imports (local to avoid circular imports during Django startup)
        # -------------------------------------------------------------------------
        from apps.moderation_sys.application.orchestration.moderation_orchestration import ModerationOrchestration
        from apps.moderation_sys.application.usecases.notify_user_of_moderated_content import NotifyUserOfModeratedContentUsecase
        from apps.moderation_sys.application.usecases.process_content_for_moderation import ProcessContentForModerationUsecase
        from apps.moderation_sys.application.usecases.resolve_appeal import ResolveAppealUsecase
        from apps.moderation_sys.application.usecases.run_moderation_drift_cron import RunModerationDriftCronJobUsecase
        from apps.moderation_sys.application.usecases.submit_appeal import SubmitAppealUsecase
        from apps.moderation_sys.application.usecases.submit_moderation_case import SubmitModerationCaseUsecase
        from apps.moderation_sys.application.usecases.switch_to_fallback_provider import SwitchToFallbackProviderUsecase
        from apps.moderation_sys.application.usecases.update_policy import UpdatePolicyUsecase
        from apps.moderation_sys.application.usecases.direct_for_human_moderation import DirectContentForHumanModerationUsecase
        from apps.moderation_sys.domain.services.policy_registry_service import PolicyRegistryService
        from apps.moderation_sys.infrastructure.repositories.django_drift_monitor_state_repository import DjangoDriftMonitorStateRepository
        from apps.moderation_sys.infrastructure.repositories.django_moderation_case_repository import DjangoModerationCaseRepository
        from apps.moderation_sys.infrastructure.repositories.django_policy_definition_repository import DjangoPolicyDefinitionRepository
        from apps.moderation_sys.infrastructure.repositories.django_provider_health_repository import DjangoProviderHealthRepository
        from apps.moderation_sys.infrastructure.repositories.django_webhook_delivery_record_repository import DjangoWebhookDeliveryRecordRepository
        from apps.moderation_sys.infrastructure.services.openai_moderation_service import OpenAIModerationService
        from apps.moderation_sys.infrastructure.services.webhook_delivery_service import WebhookDeliveryService
        from apps.moderation_sys.domain.value_objects.webhook_retry_policy import WebhookRetryPolicyVo
        from apps.users.infrastructure.repositories.user_repository import UserRepository
        from apps.moderation_sys.domain.services.content_fetcher.django_content_fetcher import DjangoContentFetcher
        from apps.moderation_sys.domain.services.fingerprint_service import FingerprintDomainService
        from core.api_clients.base_api_client import BaseApiClient
        from core.api_clients.moderation_api_client import ModerationSysApiClient
        from apps.moderation_sys.domain.services.moderation_decision_engine import ModerationDecisionEngine
        from apps.moderation_sys.infrastructure.factories.moderation_provider_factory import ModerationProviderFactory
        from apps.moderation_sys.infrastructure.repositories.django_blob_storage_repository import DjangoBlobStorageRepository


        import os

        # -------------------------------------------------------------------------
        # Repositories
        # -------------------------------------------------------------------------
        blob_storage_repo = DjangoBlobStorageRepository()
        case_repo = DjangoModerationCaseRepository(
            blob_storage_repo=blob_storage_repo
        )
        policy_def_repo = DjangoPolicyDefinitionRepository()
        provider_health_repo = DjangoProviderHealthRepository()
        webhook_repo = DjangoWebhookDeliveryRecordRepository()
        drift_monitor_repo = DjangoDriftMonitorStateRepository()
        user_repo = UserRepository()

        # -------------------------------------------------------------------------
        # Domain Services
        # -------------------------------------------------------------------------
        policy_registry = PolicyRegistryService(policy_def_repo=policy_def_repo)
        decision_engine = ModerationDecisionEngine()

        # -------------------------------------------------------------------------
        # Infrastructure Services
        # -------------------------------------------------------------------------
        # openai_moderation_provider = OpenAIModerationService(
        #     api_key=os.environ.get('OPENAI_API_KEY'),
        #     model="omni-moderation-latest"
        # )
        moderation_provider_factory = ModerationProviderFactory()

        webhook_delivery_service = WebhookDeliveryService(
            webhook_repo=webhook_repo,
            retry_policy=WebhookRetryPolicyVo(
                max_retries=3,
                initial_delay_seconds=5,
                backoff_multiplier=2.0,
                max_delay_seconds=10
            ),
            timeout_seconds=30
        )

        # -------------------------------------------------------------------------
        # Placeholders for missing services (implement when ready)
        # -------------------------------------------------------------------------
        class DummyNotificationService:
            def send(self, *args, **kwargs):
                return True

        class DummyReputationService:
            def update_reputation(self, *args, **kwargs):
                return None
            
        notification_service = DummyNotificationService()
        reputation_service = DummyReputationService()

        openai_mod_api = BaseApiClient(
            base_url='https://api.openai.com',
            timeout_seconds=5,
            max_retries=3,
            backoff_factor=0.5,
            default_headers={
                "User-Agent": "Memeinator/0.1 (dev; localhost) python-requests/2.31"
                # TODO: Update User-Agent for production. Something like example below. 
                # "User-Agent": "Memeinator/1.0 (https://memeinator.example.com; moderation@memeinator.example.com)"
            },
        )

        content_fetcher = DjangoContentFetcher(
            api_client=ModerationSysApiClient(base_http_client=openai_mod_api)
        ) 

        finger_print = FingerprintDomainService(
            content_fetcher=content_fetcher
        )

        # -------------------------------------------------------------------------
        # Use cases – all dependencies satisfied
        # -------------------------------------------------------------------------
        submit_moderation_usecase = SubmitModerationCaseUsecase(
            case_repo=case_repo,
            policy_registry=policy_registry,
            content_fetcher=content_fetcher,
            fingerprint_service=finger_print
        )

        process_content_usecase = ProcessContentForModerationUsecase(
            case_repo=case_repo,
            policy_registry=policy_registry,
            provider_health_repo=provider_health_repo,
            moderation_provider_factory=moderation_provider_factory,
            moderation_decision_engine=decision_engine
        )

        direct_human_moderation_usecase = DirectContentForHumanModerationUsecase(
            case_repo=case_repo,
        )

        submit_appeal_usecase = SubmitAppealUsecase(
            case_repo=case_repo,
            policy_registry=policy_registry,
            # user_repo=user_repo, # TODO: Does appeal require access to User info?
        )

        resolve_appeal_usecase = ResolveAppealUsecase(
            case_repo=case_repo,
        )

        notify_user_usecase = NotifyUserOfModeratedContentUsecase(
            case_repo=case_repo,
            # notification_service=notification_service,
            # user_repo=user_repo,
        )

        run_drift_cron_usecase = RunModerationDriftCronJobUsecase(
            drift_state_repo=drift_monitor_repo,
            case_repo=case_repo,
            policy_registry=policy_registry,
        )

        switch_provider_usecase = SwitchToFallbackProviderUsecase(
            provider_health_repo=provider_health_repo,
        )

        update_policy_usecase = UpdatePolicyUsecase(
            policy_repo=policy_def_repo,
        )

        # -------------------------------------------------------------------------
        # Build orchestration with all use cases injected
        # -------------------------------------------------------------------------
        self._moderation_orchestration = ModerationOrchestration(
            submit_moderation_usecase=submit_moderation_usecase,
            process_content_usecase=process_content_usecase,
            direct_human_moderation_usecase=direct_human_moderation_usecase,
            submit_appeal_usecase=submit_appeal_usecase,
            resolve_appeal_usecase=resolve_appeal_usecase,
            notify_user_usecase=notify_user_usecase,
            run_drift_cron_usecase=run_drift_cron_usecase,
            switch_provider_usecase=switch_provider_usecase,
            update_policy_usecase=update_policy_usecase,
        )

        # Optionally attach other services for convenience (not required for orchestration)
        # self._moderation_orchestration.policy_registry = policy_registry
        # self._moderation_orchestration.openai_provider = openai_moderation_provider
        # self._moderation_orchestration.webhook_delivery_service = webhook_delivery_service

        return self._moderation_orchestration

# Create global DI container
di = CoreDependencyProvider()
