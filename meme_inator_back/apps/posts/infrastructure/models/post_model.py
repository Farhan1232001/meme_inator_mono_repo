# apps/posts/models.py
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from uuid import uuid7

from meme_inator_back import settings

class PostModel(models.Model):
    post_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    image_url = models.URLField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        db_index=True,
    )
    thumbnail_url = models.URLField(max_length=500, null=True, blank=True)
    caption = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    post_type = models.CharField(max_length=100, null=True, blank=True)
    file_format = models.CharField(max_length=50, null=True, blank=True)
    upvotes_count = models.PositiveIntegerField(default=0)
    downvotes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    tags = ArrayField(base_field=models.CharField(max_length=50), default=list, blank=True)

    # Moderation related attributes
    is_flagged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    visibility = models.CharField(max_length=50, null=True, blank=True)


    def set_image_url(self, url: str):
        self.image_url = url

    def set_thumbnail_url(self, url: str):
        self.thumbnail_url = url

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Post {self.post_id}"

    
    class Meta:
        indexes = [
            models.Index(fields=['-created_on', '-post_id']),
            models.Index(fields=['author', '-created_on']),
        ]
        