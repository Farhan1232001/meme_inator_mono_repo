# apps/posts/application/orchestration/posts_orchestration.py
from typing import List, Optional
from uuid import UUID

from apps.posts.domain.entities.post_entity import PostEntity
from apps.posts.domain.value_objects.post_data_vo import PostDataVo
from apps.posts.domain.iusecases.ivote_on_post_usecase import IVoteOnPostUsecase
from apps.posts.domain.iusecases.icreate_post_usecase import ICreatePostUsecase
from apps.posts.domain.iusecases.iget_post_usecase import IGetPostUsecase
from apps.posts.domain.iusecases.idelete_post_usecase import IDeletePostUsecase
from core.results import Result


class PostsOrchestration:
    """
    Orchestration/coordinator for post flows.
    Each method is a thin orchestration boundary that will call underlying usecases/repositories.
    """

    def __init__(
        self,
        create_post_uc: ICreatePostUsecase,
        get_post_uc: IGetPostUsecase,
        delete_post_uc: IDeletePostUsecase,
        vote_on_post_uc: IVoteOnPostUsecase,
    ) -> None:
        self.create_post_uc = create_post_uc
        self.get_post_uc = get_post_uc
        self.delete_post_uc = delete_post_uc
        self.vote_on_post_uc = vote_on_post_uc

    def create_post(self, author_id: UUID, **post_data) -> Result[PostEntity]:
        """Create a new meme post."""
        # Create PostDataVo from the provided data
        post_data_dict = post_data.copy()
        post_data_dict['author_id'] = author_id
        
        try:
            post_data_vo = PostDataVo.from_dict(post_data_dict)
            return self.create_post_uc.execute(post_data_vo)
        except ValueError as e:
            from core.results import NotOk
            return NotOk(
                message=f"Invalid post data: {str(e)}",
                static_msg="post.invalid_data",
                status_code=400
            )

    def get_post(self, post_public_id: UUID) -> Result[PostEntity]:
        """Retrieve details of a single post."""
        return self.get_post_uc.execute(post_public_id=post_public_id)

    def delete_post(self, post_public_id: UUID, actor_id: UUID) -> Result[bool]:
        """Delete a post (owner only)."""
        return self.delete_post_uc.execute(
            post_public_id=post_public_id, 
            actor_id=actor_id
        )

    def vote_on_post(self, post_public_id: UUID, voter_user_id: UUID, action: str) -> Result:
        """Apply a vote to a post (upvote/downvote/remove)."""
        return self.vote_on_post_uc.execute(
            post_public_id=post_public_id, 
            voter_user_id=voter_user_id, 
            action=action
        )