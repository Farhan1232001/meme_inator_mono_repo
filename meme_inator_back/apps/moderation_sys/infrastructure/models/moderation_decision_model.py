from dataclasses import dataclass
from typing import Optional
from django.db import models


class DecisionChoices(models.TextChoices):
        ACCEPT = "ACCEPT"
        REJECT = "REJECT"
        FLAG = "FLAG"

class ModerationDecisionModel(models.Model):
    outcome = models.CharField(
        max_length=6,
        choices=DecisionChoices.choices
    )
    reason_code = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    note = models.TextField(
        null=True,
        blank=True
    )