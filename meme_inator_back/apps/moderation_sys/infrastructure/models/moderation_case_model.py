# infrastructure/models/moderation_case_model.py
from django.db import models
from uuid import uuid7

from apps.moderation_sys.infrastructure.models.moderation_action_model import ModerationActionModel
from apps.moderation_sys.infrastructure.models.moderation_appeal_model import ModerationAppealModel
from apps.moderation_sys.infrastructure.models.moderation_decision_model import ModerationDecisionModel
from meme_inator_back import settings

class ContentTypeChoices(models.TextChoices):
    IMG = "image"
    VIDEO = "video"
    TEXT = "text"

class CaseStatusEnum(models.TextChoices):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    RESOLVED = "RESOLVED"
    FLAGGED = "FLAGGED"
    APPEALING = "APPEALING"

class ModerationProviderEnum(models.TextChoices):
    OPENAI_API = "openai_moderation_api"


# TODO: Consider denormalization fields for performance. 
class ModerationCaseModel(models.Model):
    """
    Database model for ModerationCase aggregate.
    
    This is a denormalized representation for query performance.
    Value objects are stored as structured fields.
    Related entities (snapshot, fingerprint, appeal, attempts) are separate tables
    linked by ForeignKey relationships.
    """
    # Identity of case
    case_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    # Loose-Reference to Particular Content across bounded context ie across apps
    source_app = models.CharField(max_length=16) # ex. posts django app
    source_model_type = models.CharField(max_length=16) # ex. PostModel
    source_model_id = models.UUIDField(db_index=True)
    # Loose-reference approach above better than tight coupled foriegn key approach. 
    # content_id = models.ForeignKey(to=ContentToModerateModel, on_delete=models.CASCADE)


    # NOTE: On Related Entities (Snapshot & Fingerprint):
    # Immutable snapshot & fingerprint taken at submission time, a MUST for all cases. 
    # Snapshot is proof of content state at submission; fingerprint is proof of identity of content. 
    # ... If snapshot deleted then delete case. If fingerprint deleted then 
    #
    # - ContentSnapshotModel links to this case via models.CASCADE.
    # - FingerprintModel links to this case via models.DO_NOTHING / separate persistence. 
    

    # Who, whats, # where pertaing the case
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    policy_routing_key = models.CharField(max_length=40)
    content_type = models.CharField(
        max_length=32,
        choices=ContentTypeChoices.choices,
    )
    region = models.CharField(max_length=8)

    # Status and Decisions
    status = models.CharField(
        max_length=9,
        choices=CaseStatusEnum.choices
    )
    action = models.OneToOneField(
        to = ModerationActionModel,
        on_delete=models.DO_NOTHING,
        null = True
    )
    decision = models.OneToOneField(
        to = ModerationDecisionModel,
        on_delete=models.DO_NOTHING,
        null = True
    )
    # ... ConfidenceScoreVo is denormalized; vo only has one value
    confidence_score = models.FloatField(null=True)
    provider_used = models.CharField(
        max_length=24,
        choices=ModerationProviderEnum.choices,
        null=True
    )

    # Timestamps
    created_at = models.DateTimeField()
    decided_at = models.DateTimeField(null=True)

    # Embedded Entities
    appeal = models.ForeignKey(
        to = ModerationAppealModel,
        on_delete=models.DO_NOTHING,
        null=True
    )


    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['source_app', 'source_model_type', 'source_model_id']),
            models.Index(fields=['source_model_id']), 
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['policy_routing_key']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"ModerationCase {self.case_id} - {self.status}"
