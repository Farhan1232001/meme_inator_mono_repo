# application/gateways/moderation_gateway.py

from apps.moderation_sys.application.schemas.moderation_submission_request import ModerationSubmissionRequestSchema
from apps.moderation_sys.application.usecases.submit_moderation_case import SubmitModerationCaseUsecase
from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from apps.moderation_sys.domain.enums.moderation_enums import DecisionEnum
from apps.moderation_sys.domain.value_objects.content_to_mod.post_to_moderate import PostToModerateVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from apps.posts.domain.entities.post_entity import PostEntity
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import (
    ContentToModerateVo,
    ImageToModerateVo,
)
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from core.results import Error, NotOk, Result

class ModerationGateway:

    def __init__(self, submit_moderation_usecase: SubmitModerationCaseUsecase):
        self._submit_moderation_usecase = submit_moderation_usecase

    def submit_and_process_content_to_moderation_sys(
        self,
        post: PostEntity
    ) -> ModerationDecisionVo:
        
        
        
        # 1. Map post to ContentToModerateVo
        content = ContentToModerateVo(
            post_id=post.post_id,
            author_id=post.author,
            policy_routing_key="mod_sys:default:image",
            content_type=MediaTypeEnum.IMG,
            content_src=MediaSourceEnum.EXTERNAL_STORAGE,
            region=None,
            image_content=ImageToModerateVo(
                retrieval_key=None,
                image_data=None,
                image_url=post.imageURL,
                format=post.fileFormat
            ),
            video_content=None,
            caption=None,
            tags=list
        )

        # 2. Submit the content
        submit:SubmitModerationCaseUsecase = self._submit_moderation_usecase
        submission_result:Result[ModerationCase] = submit.execute(
            content_to_moderate=content
        )

        if (not submission_result.is_ok):
            return submission_result
        moderation_case:ModerationCase = submission_result.value

        # 3. Process the Content for moderation
    
        return ModerationDecisionVo(
            outcome=DecisionEnum.UNDECIDED,
            reason_code=None,
            note=None
        )


PostsToModerationSysGateway = ModerationGateway
