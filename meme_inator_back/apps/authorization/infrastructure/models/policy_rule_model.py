from uuid import uuid7
from django.db import models


class PolicyRuleModel(models.Model):
    """
    Declarative policy rule used by your ABAC/conditional checks.
    `expression` can be JSONLogic, a small DSL, or any string your evaluator understands.
    Keep expressions small and well-tested.
    """
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=200, unique=True)
    expression = models.TextField(help_text="Condition expression (JSONLogic or domain DSL)")
    priority = models.IntegerField(default=100, help_text="Lower numbers = higher priority")
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Policy Rule"
        verbose_name_plural = "Policy Rules"
        ordering = ["priority", "-created_at"]
        indexes = [
            models.Index(fields=["active", "priority"]),
        ]

    def __str__(self) -> str:
        return f"PolicyRule(name={self.name}, priority={self.priority}, active={self.active})"
