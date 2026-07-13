# apps/posts/application/usecases/delete_post_usecase.py
from uuid import UUID
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.posts.domain.iusecases.idelete_post_usecase import IDeletePostUsecase
from core.results import Result, NotOk, Ok, Error


class DeletePostUsecase(IDeletePostUsecase):
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_public_id: UUID, actor_id: UUID) -> Result[bool]:
        try:
            # Get the post
            post = self.post_repo.get_post_by_public_id(post_public_id)
            
            if not post:
                return NotOk(
                    message="Post not found",
                    static_msg="post.not_found",
                    status_code=404
                )
            
            # Check if actor is the author
            if post.author != actor_id:
                return NotOk(
                    message="You can only delete your own posts",
                    static_msg="post.delete_not_authorized",
                    status_code=403
                )
            
            # Update post entity to be deleted
            post.isDeleted = True
            
            # Save the updated post
            result = self.post_repo.save_post(post)
            
            if isinstance(result, Error):
                return result
            
            return Ok(True)
            
        except Exception as e:
            return Error(
                message="Failed to delete post",
                exception=e,
                status_code=500
            )