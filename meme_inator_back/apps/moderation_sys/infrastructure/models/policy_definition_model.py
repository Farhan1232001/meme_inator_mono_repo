# infrastructure/models/policy_definition_model.py
from django.db import models
from uuid import uuid7

class PolicyDefinitionModel(models.Model):
    policy_id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    routing_key = models.CharField(max_length=255, db_index=True)
    version = models.IntegerField(default=1)
    
    # Confidence thresholds
    high_confidence_min = models.FloatField(default=0.8)
    low_confidence_max = models.FloatField(default=0.2)
    grey_zone_min = models.FloatField(default=0.5)
    
    # Appeal eligibility rules (JSON)
    appeal_rules = models.JSONField(default=dict)
    
    # Reputation impact (JSON)
    reputation_impact = models.JSONField(default=dict)
    
    # Webhook retry policy (JSON)
    webhook_retry_policy = models.JSONField(default=dict)
    
    # Drift detection policy (JSON)
    drift_detection_policy = models.JSONField(default=dict)
    
    # Status and timestamps
    active_from = models.DateTimeField()
    active_to = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.UUIDField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['routing_key', 'active_from']),
            models.Index(fields=['routing_key', 'version']),
        ]
        unique_together = [['routing_key', 'version']]