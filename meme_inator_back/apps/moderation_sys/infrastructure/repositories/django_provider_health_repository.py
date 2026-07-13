# infrastructure/repositories/django_provider_health_repository.py
from collections import deque
from uuid import UUID
from typing import List, Optional
from django.core.exceptions import ObjectDoesNotExist

from apps.moderation_sys.domain.aggregates.provider_health import ProviderHealth
from apps.moderation_sys.domain.irepositories.provider_health_repository import IProviderHealthRepository
from apps.moderation_sys.domain.value_objects.error_rate import ErrorRateVo
from apps.moderation_sys.domain.value_objects.sliding_window_metrics import SlidingWindowMetricsVo
from apps.moderation_sys.infrastructure.models.provider_health_model import ProviderHealthModel


class DjangoProviderHealthRepository(IProviderHealthRepository):

    def save(self, health: ProviderHealth) -> ProviderHealth:
        model, _ = ProviderHealthModel.objects.update_or_create(
            provider_name=health.provider_name,
            defaults={
                "total_requests": health.error_rate.total_requests,
                "total_failures": health.error_rate.total_failures,
                "window_size": health.sliding_window_metrics.window_size,
                "window_results": list(health.sliding_window_metrics.results),
                "circuit_breaker_state": health.circuit_breaker_state,
                "last_state_change": health.last_state_change,
            },
        )
        return health

    def find_by_provider_name(self, provider_name: str) -> Optional[ProviderHealth]:
        try:
            model = ProviderHealthModel.objects.get(provider_name=provider_name)
            return self._to_domain(model)
        except ProviderHealthModel.DoesNotExist:
            return None

    def find_all(self) -> List[ProviderHealth]:
        return [self._to_domain(m) for m in ProviderHealthModel.objects.all()]

    def find_available_providers(self) -> List[ProviderHealth]:
        available = []
        for model in ProviderHealthModel.objects.all():
            health = self._to_domain(model)
            if health.is_available():
                available.append(health)
        return available

    def find_by_circuit_state(self, state: str) -> List[ProviderHealth]:
        models = ProviderHealthModel.objects.filter(circuit_breaker_state=state)
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: ProviderHealthModel) -> ProviderHealth:
        error_rate = ErrorRateVo(
            total_requests=model.total_requests,
            total_failures=model.total_failures,
        )
        window_metrics = SlidingWindowMetricsVo(
            window_size=model.window_size,
            results=deque(model.window_results, maxlen=model.window_size),
        )
        return ProviderHealth(
            provider_name=model.provider_name,
            error_rate=error_rate,
            sliding_window_metrics=window_metrics,
            circuit_breaker_state=model.circuit_breaker_state,
            last_state_change=model.last_state_change,
        )