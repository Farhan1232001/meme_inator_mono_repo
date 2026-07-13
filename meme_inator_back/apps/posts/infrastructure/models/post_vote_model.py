# apps/posts/infrastructure/models/post_vote_model.py
import uuid
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from typing import Optional, Tuple


class PostVoteModel(models.Model):
    """
    Join table for tracking user votes on posts.
    Each user can have only one vote (like/dislike) per post.
    """
    class VoteType(models.TextChoices):
        UPVOTE = 'upvote', 'Upvote'
        DOWNVOTE = 'downvote', 'Downvote'
    
    id = models.BigAutoField(primary_key=True)
    public_id = models.UUIDField(default=uuid.uuid7, editable=False, unique=True)
    
    post = models.ForeignKey(
        "posts.PostModel",
        on_delete=models.CASCADE,
        related_name="votes"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_votes"
    )
    
    vote_type = models.CharField(
        max_length=10,
        choices=VoteType.choices
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = "posts"
        db_table = "posts_postvotemodel"
        unique_together = [['post', 'user']]  # One vote per user per post
        indexes = [
            models.Index(fields=['post', 'user']),
            models.Index(fields=['post', 'vote_type']),
            models.Index(fields=['user', 'vote_type']),
        ]
    
    def __str__(self):
        return f"{self.user.user_name} {self.vote_type}d post {self.post.post_id}"
    
    def clean(self):
        """Validate that post and user are not the same (prevent self-voting if desired)."""
        if self.post.author_id == self.user_id:
            raise ValidationError("Users cannot vote on their own posts")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    # ------------------------------------------------------------------
    # Factory Methods
    # ------------------------------------------------------------------
    
    @classmethod
    def create_vote(cls, post, user, vote_type: str) -> "PostVoteModel":
        """
        Create a vote record. Handles atomic creation and post counter updates.
        """
        with transaction.atomic():
            # Get or create/update the vote
            vote, created = cls.objects.update_or_create(
                post=post,
                user=user,
                defaults={'vote_type': vote_type}
            )
            
            # Update post counters based on vote change
            post.refresh_from_db()
            
            if created:
                # New vote - increment the appropriate counter
                if vote_type == cls.VoteType.UPVOTE:
                    post.upvotes_count = models.F('upvotes_count') + 1
                else:
                    post.downvotes_count = models.F('downvotes_count') + 1
            else:
                # Vote changed - adjust both counters
                old_vote_type = vote.vote_type if hasattr(vote, '_old_vote_type') else None
                
                if old_vote_type != vote_type:
                    if old_vote_type == cls.VoteType.UPVOTE:
                        post.upvotes_count = models.F('upvotes_count') - 1
                        post.downvotes_count = models.F('downvotes_count') + 1
                    elif old_vote_type == cls.VoteType.DOWNVOTE:
                        post.downvotes_count = models.F('downvotes_count') - 1
                        post.upvotes_count = models.F('upvotes_count') + 1
                    else:
                        # No previous vote (shouldn't happen but just in case)
                        if vote_type == cls.VoteType.UPVOTE:
                            post.upvotes_count = models.F('upvotes_count') + 1
                        else:
                            post.downvotes_count = models.F('downvotes_count') + 1
            
            post.save(update_fields=['upvotes_count', 'downvotes_count'])
            return vote

    @classmethod
    def remove_vote(cls, post, user) -> Tuple[bool, Optional[str]]:
        """
        Remove a user's vote from a post.
        Returns (success, removed_vote_type)
        """
        try:
            with transaction.atomic():
                vote = cls.objects.filter(post=post, user=user).first()
                if not vote:
                    return False, None
                
                removed_vote_type = vote.vote_type
                
                # Decrement the appropriate counter
                if removed_vote_type == cls.VoteType.UPVOTE:
                    post.upvotes_count = models.F('upvotes_count') - 1
                else:
                    post.downvotes_count = models.F('downvotes_count') - 1
                
                # Delete the vote
                vote.delete()
                post.save(update_fields=['upvotes_count', 'downvotes_count'])
                
                return True, removed_vote_type
                
        except Exception:
            return False, None
    
    @classmethod
    def get_user_vote(cls, post, user) -> Optional["PostVoteModel"]:
        """Get a user's vote on a specific post."""
        return cls.objects.filter(post=post, user=user).first()
    
    @classmethod
    def get_post_vote_stats(cls, post) -> dict:
        """Get vote statistics for a post."""
        from django.db.models import Count
        
        stats = cls.objects.filter(post=post).values('vote_type').annotate(
            count=Count('id')
        )
        
        result = {'upvote': 0, 'downvote': 0}
        for stat in stats:
            result[stat['vote_type']] = stat['count']
        
        return result