# infrastructure/models/content_snapshot_model.py
from django.db import models
from uuid import uuid7
from apps.moderation_sys.infrastructure.models.content_blob_model import ContentBlobModel


class ContentSnapshotModel(models.Model):
    """Single responsibility: Prove what content was moderated at that time"""
    snapshot_id = models.UUIDField(primary_key=True, default=uuid7)

    mod_case = models.OneToOneField(to='ModerationCaseModel', on_delete=models.CASCADE)
    
    content_blob = models.ForeignKey(ContentBlobModel, on_delete=models.PROTECT)
    
    captured_at = models.DateTimeField(auto_now_add=True)


