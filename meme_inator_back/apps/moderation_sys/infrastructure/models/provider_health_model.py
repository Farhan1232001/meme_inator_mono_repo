# infrastructure/models/provider_health_model.py
from django.db import models
from uuid import uuid7

class ProviderHealthModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    provider_name = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Error rate metrics
    total_requests = models.IntegerField(default=0)
    total_failures = models.IntegerField(default=0)
    
    # Sliding window metrics (stored as JSON array)
    window_size = models.IntegerField(default=100)
    window_results = models.JSONField(default=list)  # List of booleans
    
    # Circuit breaker state
    circuit_breaker_state = models.CharField(max_length=20, default='CLOSED')
    last_state_change = models.DateTimeField(auto_now_add=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        pass