# apps/commentsections/infrastructure/models/comment_vote_model.py
import uuid
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from typing import Optional, Tuple


class CommentVoteModel(models.Model):
    """
    Join table for tracking user votes on comments.
    Each user can have only one vote (like/dislike) per comment.
    entry tracks if user has a upvote or downvote. No entry implies NO vote has been casted. 
    """
    class VoteType(models.TextChoices):
        UPVOTE = 'upvote'
        DOWNVOTE = 'downvote'
    
    id = models.BigAutoField(primary_key=True)
    public_id = models.UUIDField(default=uuid.uuid7, editable=False, unique=True)
    
    comment = models.ForeignKey(
        "commentsections.CommentModel",
        on_delete=models.CASCADE,
        related_name="votes"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_votes"
    )
    
    vote_type = models.CharField(
        max_length=10,
        choices=VoteType.choices
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = "commentsections"
        db_table = "commentsections_commentvotemodel"
        unique_together = [['comment', 'user']]  # One vote per user per comment
        indexes = [
            models.Index(fields=['comment', 'user']),
            models.Index(fields=['comment', 'vote_type']),
            models.Index(fields=['user', 'vote_type']),
        ]
    
    def __str__(self):
        return f"{self.user.user_name} {self.vote_type}d comment {self.comment.public_id}"
    
    def clean(self):
        """Validate that comment and user are not the same (prevent self-voting if desired)."""
        if self.comment.author_id == self.user_id:
            raise ValidationError("Users cannot vote on their own comments")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    # ------------------------------------------------------------------
    # Factory Methods
    # ------------------------------------------------------------------
    
    @classmethod
    def create_vote(cls, comment, user, vote_type: str) -> "CommentVoteModel":
        """
        Create a vote record. Handles atomic creation and comment counter updates.
        """
        with transaction.atomic():
            # Get or create/update the vote
            vote, created = cls.objects.update_or_create(
                comment=comment,
                user=user,
                defaults={'vote_type': vote_type}
            )
            
            # Update comment counters based on vote change
            comment.refresh_from_db()
            
            if created:
                # New vote - increment the appropriate counter
                if vote_type == cls.VoteType.UPVOTE:
                    comment.upvote_count = models.F('upvote_count') + 1
                else:
                    comment.downvote_count = models.F('downvote_count') + 1
            else:
                # Vote changed - adjust both counters
                old_vote_type = vote.vote_type if hasattr(vote, '_old_vote_type') else None
                
                if old_vote_type != vote_type:
                    if old_vote_type == cls.VoteType.UPVOTE:
                        comment.upvote_count = models.F('upvote_count') - 1
                        comment.downvote_count = models.F('downvote_count') + 1
                    elif old_vote_type == cls.VoteType.DOWNVOTE:
                        comment.downvote_count = models.F('downvote_count') - 1
                        comment.upvote_count = models.F('upvote_count') + 1
                    else:
                        # No previous vote (shouldn't happen but just in case)
                        if vote_type == cls.VoteType.UPVOTE:
                            comment.upvote_count = models.F('upvote_count') + 1
                        else:
                            comment.downvote_count = models.F('downvote_count') + 1
            
            comment.save(update_fields=['upvote_count', 'downvote_count'])
            return vote
    
    @classmethod
    def remove_vote(cls, comment, user) -> Tuple[bool, Optional[str]]:
        """
        Remove a user's vote from a comment.
        Returns (success, removed_vote_type)
        """
        try:
            with transaction.atomic():
                vote = cls.objects.filter(comment=comment, user=user).first()
                if not vote:
                    return False, None
                
                removed_vote_type = vote.vote_type
                
                # Decrement the appropriate counter
                if removed_vote_type == cls.VoteType.UPVOTE:
                    comment.upvote_count = models.F('upvote_count') - 1
                else:
                    comment.downvote_count = models.F('downvote_count') - 1
                
                # Delete the vote
                vote.delete()
                comment.save(update_fields=['upvote_count', 'downvote_count'])
                
                return True, removed_vote_type
                
        except Exception:
            return False, None
    
    @classmethod
    def get_user_vote(cls, comment, user) -> Optional["CommentVoteModel"]:
        """Get a user's vote on a specific comment."""
        return cls.objects.filter(comment=comment, user=user).first()
    
    @classmethod
    def get_comment_vote_stats(cls, comment) -> dict:
        """Get vote statistics for a comment."""
        from django.db.models import Count
        
        stats = cls.objects.filter(comment=comment).values('vote_type').annotate(
            count=Count('id')
        )
        
        result = {'like': 0, 'dislike': 0}
        for stat in stats:
            result[stat['vote_type']] = stat['count']
        
        return result