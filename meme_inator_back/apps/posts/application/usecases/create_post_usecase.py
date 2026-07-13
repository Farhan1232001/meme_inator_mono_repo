# apps/posts/application/usecases/create_post_usecase.py
from uuid import UUID
import uuid

from apps.posts.domain.entities.post_data_vo import PostDataVo
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.posts.domain.iusecases.icreate_post_usecase import ICreatePostUsecase
from apps.posts.domain.entities.post_entity import PostEntity
from datetime import datetime
from core.results import Ok, Result, NotOk, Error


class CreatePostUsecase(ICreatePostUsecase):
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_data: PostDataVo) -> Result[PostEntity]:
        """Create a new post with the given data."""
        try:
            # Create PostEntity from PostDataVo
            post_entity = PostEntity(
                post_id=uuid.uuid7(),
                imageURL=post_data.image_url,
                author=post_data.author_id,
                thumbnailURL=post_data.thumbnail_url,
                caption=post_data.caption,
                createdOn=datetime.now(),
                post_type=post_data.post_type,
                fileFormat=post_data.file_format,
                upvotesCount=0,
                downvotesCount=0,
                commentsCount=0,
                sharesCount=0,
                tags=post_data.tags or [],
                isFlagged=False,
                isDeleted=False,
                visibility=post_data.visibility or 'public'
            )
            
            # Save the post via repository
            result = self.post_repo.save_post(post_entity)
            
            if isinstance(result, Error):
                return result
            
            return Ok(result.value)
            
        except ValueError as e:
            return NotOk(
                message=f"Invalid post data: {str(e)}",
                static_msg="post.invalid_data",
                status_code=400
            )
        except Exception as e:
            return Error(
                message="Failed to create post",
                exception=e,
                status_code=500
            )