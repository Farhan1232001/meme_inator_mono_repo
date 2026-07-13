from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import field_validator, ValidationInfo, model_validator

from apps.moderation_sys.domain.enums.media_src_enum import MediaSourceEnum
from apps.moderation_sys.domain.enums.media_type_enums import MediaTypeEnum


class TextContentSchema(Schema):
    """Text content to moderate."""
    text: str
    language: Optional[str] = None


class ImageContentSchema(Schema):
    """Image content to moderate."""
    image_data: Optional[bytes] = None
    image_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None


class VideoContentSchema(Schema):
    """Video content to moderate."""
    video_data: Optional[bytes] = None
    video_url: Optional[str] = None
    retrieval_key: Optional[str] = None
    format: Optional[str] = None


class ModerationSubmissionRequestSchema(Schema):
    """Request schema for submitting content for moderation.
    
    content_src: Where is content BLOB of request stored?
    """
    content_id: UUID
    author_id: UUID
    policy_routing_key: str
    content_type: MediaTypeEnum
    # TODO: Rename this ingestion_src
    content_source: MediaSourceEnum = MediaSourceEnum.REQUEST_BODY
    region: Optional[str] = None
    
    # Only ONE of these should be present based on content_type
    text_content: Optional[TextContentSchema] = None
    image_content: Optional[ImageContentSchema] = None
    video_content: Optional[VideoContentSchema] = None
    
    @model_validator(mode='after')
    def validate_exactly_one_content_type(self):
        """Validate that exactly one content type is provided."""
        content_fields = ['text_content', 'image_content', 'video_content']
        provided = [f for f in content_fields if getattr(self, f) is not None]
        
        if len(provided) != 1:
            raise ValueError(f"Exactly one content type must be provided. Got: {provided}")
        
        # Also validate that the content type matches the field
        if self.text_content and self.content_type != MediaTypeEnum.TEXT:
            raise ValueError(f"text_content provided but content_type is {self.content_type}")
        if self.image_content and self.content_type != MediaTypeEnum.IMG:
            raise ValueError(f"image_content provided but content_type is {self.content_type}")
        if self.video_content and self.content_type != MediaTypeEnum.VIDEO:
            raise ValueError(f"video_content provided but content_type is {self.content_type}")
        
        return self
    
    @field_validator('image_content')
    @classmethod
    def validate_image_content(cls, v: Optional[ImageContentSchema], info: ValidationInfo) -> Optional[ImageContentSchema]:
        """Validate image content based on content_source and URL presence."""
        if v is None:
            return v
        
        content_source = info.data.get('content_source')
        has_url = v.image_url is not None and v.image_url.strip() != ""
        has_data = v.image_data is not None
        has_key = v.retrieval_key is not None and v.retrieval_key.strip() != ""
        
        if content_source == MediaSourceEnum.REQUEST_BODY:
            # For REQUEST_BODY: Must have either data OR url, but not both
            if has_data and has_url:
                raise ValueError("For REQUEST_BODY source, cannot provide both image_data and image_url")
            if not has_data and not has_url:
                raise ValueError("For REQUEST_BODY source, either image_data or image_url must be provided")
            
            # If URL is provided, data and key must be null
            if has_url:
                if has_data:
                    raise ValueError("When image_url is provided, image_data must be null")
                if has_key:
                    raise ValueError("When image_url is provided, retrieval_key must be null")
            
            # If data is provided, url and key must be null
            if has_data:
                if has_url:
                    raise ValueError("When image_data is provided, image_url must be null")
                if has_key:
                    raise ValueError("When image_data is provided, retrieval_key must be null")
        
        elif content_source == MediaSourceEnum.EXTERNAL_STORAGE:
            # For EXTERNAL_STORAGE: Must have either url OR key, but not both
            if has_url and has_key:
                raise ValueError("For EXTERNAL_STORAGE source, cannot provide both image_url and retrieval_key")
            if not has_url and not has_key:
                raise ValueError("For EXTERNAL_STORAGE source, either image_url or retrieval_key must be provided")
            
            # If URL is provided, data and key must be null
            if has_url:
                if has_data:
                    raise ValueError("When image_url is provided, image_data must be null")
                if has_key:
                    raise ValueError("When image_url is provided, retrieval_key must be null")
            
            # If key is provided, data and url must be null
            if has_key:
                if has_data:
                    raise ValueError("When retrieval_key is provided, image_data must be null")
                if has_url:
                    raise ValueError("When retrieval_key is provided, image_url must be null")
        
        elif content_source == MediaSourceEnum.LOCAL_DB:
            # For LOCAL_DB: Must have retrieval_key, no data or url
            if not has_key:
                raise ValueError("For LOCAL_DB source, retrieval_key is required")
            if has_data:
                raise ValueError("For LOCAL_DB source, image_data must be null")
            if has_url:
                raise ValueError("For LOCAL_DB source, image_url must be null")
        
        return v

    @field_validator('video_content')
    @classmethod
    def validate_video_content(cls, v: Optional[VideoContentSchema], info: ValidationInfo) -> Optional[VideoContentSchema]:
        """Validate video content based on content_source and URL presence."""
        if v is None:
            return v
        
        content_source = info.data.get('content_source')
        has_url = v.video_url is not None and v.video_url.strip() != ""
        has_data = v.video_data is not None
        has_key = v.retrieval_key is not None and v.retrieval_key.strip() != ""
        
        if content_source == MediaSourceEnum.REQUEST_BODY:
            # For REQUEST_BODY: Must have either data OR url, but not both
            if has_data and has_url:
                raise ValueError("For REQUEST_BODY source, cannot provide both video_data and video_url")
            if not has_data and not has_url:
                raise ValueError("For REQUEST_BODY source, either video_data or video_url must be provided")
            
            # If URL is provided, data and key must be null
            if has_url:
                if has_data:
                    raise ValueError("When video_url is provided, video_data must be null")
                if has_key:
                    raise ValueError("When video_url is provided, retrieval_key must be null")
            
            # If data is provided, url and key must be null
            if has_data:
                if has_url:
                    raise ValueError("When video_data is provided, video_url must be null")
                if has_key:
                    raise ValueError("When video_data is provided, retrieval_key must be null")
        
        elif content_source == MediaSourceEnum.EXTERNAL_STORAGE:
            # For EXTERNAL_STORAGE: Must have either url OR key, but not both
            if has_url and has_key:
                raise ValueError("For EXTERNAL_STORAGE source, cannot provide both video_url and retrieval_key")
            if not has_url and not has_key:
                raise ValueError("For EXTERNAL_STORAGE source, either video_url or retrieval_key must be provided")
            
            # If URL is provided, data and key must be null
            if has_url:
                if has_data:
                    raise ValueError("When video_url is provided, video_data must be null")
                if has_key:
                    raise ValueError("When video_url is provided, retrieval_key must be null")
            
            # If key is provided, data and url must be null
            if has_key:
                if has_data:
                    raise ValueError("When retrieval_key is provided, video_data must be null")
                if has_url:
                    raise ValueError("When retrieval_key is provided, video_url must be null")
        
        elif content_source == MediaSourceEnum.LOCAL_DB:
            # For LOCAL_DB: Must have retrieval_key, no data or url
            if not has_key:
                raise ValueError("For LOCAL_DB source, retrieval_key is required")
            if has_data:
                raise ValueError("For LOCAL_DB source, video_data must be null")
            if has_url:
                raise ValueError("For LOCAL_DB source, video_url must be null")
        
        return v
    
    class Config:
        use_enum_values = True