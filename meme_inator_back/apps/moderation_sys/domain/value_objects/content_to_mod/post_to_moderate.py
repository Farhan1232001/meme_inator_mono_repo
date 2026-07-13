from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.img_to_mod import ImageToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.txt_to_mod import TextToModerateVo
from apps.moderation_sys.domain.value_objects.content_to_mod.atomic_vos.video_to_mod import VideoToModerateVo


# TODO: Remove. Bad design. moderation_system should not care about particular content types: posts, comments, etc. 
# use generic ContentToModerateVo, since all content is composed of media (text, images, video, audio etc). 
@dataclass(frozen=True)
class PostToModerateVo:

    post_id: UUID
    author_id: UUID
    policy_routing_key: str
    content_type: MediaTypeEnum
    content_src: MediaSourceEnum
    region: Optional[str] = None

    # Post can be an image or video
    image_content: Optional[ImageToModerateVo] = None
    video_content: Optional[VideoToModerateVo] = None

    # Post can have caption and tags
    caption: Optional[TextToModerateVo] = None
    tags: list[str] = field(default_factory=list)