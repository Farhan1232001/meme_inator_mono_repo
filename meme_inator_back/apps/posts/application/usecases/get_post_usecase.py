# apps/posts/application/usecases/get_post_usecase.py
from uuid import UUID
from apps.posts.domain.irepositories.iposts_repository import IPostRepository
from apps.posts.domain.iusecases.iget_post_usecase import IGetPostUsecase
from core.results import Ok, Result, NotOk


class GetPostUsecase(IGetPostUsecase):
    def __init__(self, post_repo: IPostRepository):
        self.post_repo = post_repo
    
    def execute(self, post_public_id: UUID) -> Result:
        # Get post from repository
        post = self.post_repo.get_post_by_public_id(post_public_id)
        
        if not post:
            return NotOk(
                message="Post not found",
                static_msg="post.not_found",
                status_code=404
            )
        
        return Ok(post)