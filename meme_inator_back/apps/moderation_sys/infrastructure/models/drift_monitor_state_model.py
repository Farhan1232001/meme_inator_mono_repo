# infrastructure/models/drift_monitor_state_model.py
from django.db import models
from uuid import uuid7

class DriftMonitorStateModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    fingerprint_hash = models.CharField(max_length=64, unique=True, db_index=True)
    
    # Case reference
    case_id = models.UUIDField()
    
    # Decision tracking
    last_decision = models.CharField(max_length=20)
    last_provider = models.CharField(max_length=100)
    last_confidence = models.FloatField()
    
    # Timestamps
    last_seen_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Drift detection
    drift_detected = models.BooleanField(default=False)
    drift_detected_at = models.DateTimeField(null=True, blank=True)
    previous_provider = models.CharField(max_length=100, null=True, blank=True)
    previous_decision = models.CharField(max_length=20, null=True, blank=True)
    confidence_delta = models.FloatField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['fingerprint_hash']),
            models.Index(fields=['last_provider']),
            models.Index(fields=['drift_detected']),
        ]