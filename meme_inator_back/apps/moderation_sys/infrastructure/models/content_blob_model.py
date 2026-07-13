# infrastructure/models/content_blob_model.py
from uuid import uuid7

from django.core.exceptions import ValidationError
from django.db import models

class StorageSourceChoices(models.TextChoices):
    LOCAL_DB = "local_db"              # fetch from local database using content_id + retrieval_key
    EXTERNAL_STORAGE = "external_storage"  # fetch from S3/blob storage



class ContentBlobModel(models.Model):
    """
    Represents a unique piece of content (deduplicated by hash).
    Acts as the source of truth for stored media/text blobs.

    Stored content has a source type (LOCAL_DB or EXTERNAL_STORAGE) and Storage Location (ie storage provider) for the blob. 
    """

    id = models.UUIDField(default=uuid7, primary_key=True, editable=False, unique=True)

    # SHA-256 (32 bytes)
    dedup_content_hash = models.BinaryField(
        max_length=32,
        editable=False
    )

    # Storage Source ie Storage location ie content source(where is blob stored?)
    storage_location = models.CharField(
        max_length=32,
        choices=StorageSourceChoices.choices,
    )

    # storage_src as EXTERNAL_STORAGE attributes (means blob stored external to memeinator system)
    # ... EXTERNAL Storage location (S3, GCS, etc.)
    external_storage_url = models.CharField(max_length=1024, null=True)
    external_storage_key = models.CharField(max_length=512, null=True)
    external_storage_provider = models.CharField(max_length=50, null=True) # s3

    # Metadata
    mime_type = models.CharField(max_length=100)
    file_size_bytes = models.BigIntegerField()

    # content_src as LOCAL_DB attributes (means blob stored external to memeinator system)
    # ... Store in local db (use sparingly)
    blob = models.BinaryField(blank=True, null=True)

    file_format = models.CharField( # jpeg, mp4, etc
        max_length=32,
        null=True,
        blank=True,
    )
    

    # Lifecycle
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                name="external_storage_requires_storage_info",
                condition=(
                    # For LOCAL_DB: no constraints on external storage fields
                    models.Q(storage_location="local_db") |
                    # For EXTERNAL_STORAGE: must have either URL OR (key AND provider)
                    models.Q(
                        storage_location="external_storage",
                        external_storage_url__isnull=False
                    ) |
                    models.Q(
                        storage_location="external_storage",
                        external_storage_key__isnull=False,
                        external_storage_provider__isnull=False
                    )
                )
            ),
            # Ensure that for EXTERNAL_STORAGE, we don't have both URL and key/provider
            models.CheckConstraint(
                name="external_storage_no_duplicate_location",
                condition=(
                    models.Q(storage_location="local_db") |
                    models.Q(
                        storage_location="external_storage",
                        external_storage_url__isnull=True,
                        external_storage_key__isnull=False,
                        external_storage_provider__isnull=False
                    ) |
                    models.Q(
                        storage_location="external_storage",
                        external_storage_url__isnull=False,
                        external_storage_key__isnull=True,
                        external_storage_provider__isnull=True
                    )
                )
            ),
        ]

    def __str__(self):
        return f"ContentBlob<{self.dedup_content_hash.hex()[:8]}>"
    

    def clean(self):
        super().clean()
        if self.storage_location == StorageSourceChoices.LOCAL_DB:
            if not self.blob:
                raise ValidationError({
                    "blob": "blob is required for LOCAL_DB content."
                })

            if self.external_storage_key:
                raise ValidationError({
                    "external_storage_key": "external_storage_key must be empty for LOCAL_DB content."
                })

        elif self.storage_location == StorageSourceChoices.EXTERNAL_STORAGE:

            if not self.external_storage_key:
                raise ValidationError({
                    "external_storage_key": "external_storage_key is required for EXTERNAL_STORAGE content."
                })

            if self.blob:
                raise ValidationError({
                    "blob": "blob must be empty for EXTERNAL_STORAGE content."
                })

