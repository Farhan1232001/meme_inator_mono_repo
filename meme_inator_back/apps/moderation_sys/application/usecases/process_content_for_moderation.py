import logging
from uuid import UUID
from typing import Callable, Optional
from collections import deque

from apps.moderation_sys.domain.aggregates.moderation_case import ModerationCase
from apps.moderation_sys.domain.aggregates.provider_health import CircuitBreakerStateEnum, ProviderHealth
from apps.moderation_sys.domain.enums.moderation_enums import CaseStatusEnum, ModerationProviderEnum
from apps.moderation_sys.domain.irepositories.moderation_case_repository import IModerationCaseRepository
from apps.moderation_sys.domain.irepositories.provider_health_repository import IProviderHealthRepository
from apps.moderation_sys.domain.services.moderation_decision_engine import ModerationDecisionEngine
from apps.moderation_sys.domain.services.moderation_provider import IModerationProvider
from apps.moderation_sys.domain.services.policy_registry_service import PolicyRegistryService
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo
from apps.moderation_sys.domain.value_objects.content_to_mod.content_to_moderate import ContentToModerateVo
from apps.moderation_sys.domain.value_objects.error_rate import ErrorRateVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from apps.moderation_sys.domain.value_objects.moderation_response import ModerationResponseVo
from apps.moderation_sys.domain.value_objects.sliding_window_metrics import SlidingWindowMetricsVo
from apps.moderation_sys.infrastructure.factories.moderation_provider_factory import ModerationProviderFactory
from apps.moderation_sys.infrastructure.services.openai_moderation_service import OpenAIModerationService
from core.api_clients.moderation_api_client import ModerationSysApiClient
from core.results import Error, NotOk, Ok, Result


logger = logging.getLogger(__name__)


class ProcessContentForModerationUsecase:
    """
    Invoked after SubmitModerationCase has persisted the case.
    Runs the moderation provider, records health, evaluates the decision,
    and updates the case accordingly.

    # TODO: Pass in a ModerationProviderFactory instead of a particular provider type. Factory can have OpenAIModerationService, AnthropicModerationService, etc
    """

    def __init__(
        self,
        case_repo: IModerationCaseRepository,
        policy_registry: PolicyRegistryService,
        provider_health_repo: IProviderHealthRepository,
        moderation_provider_factory: ModerationProviderFactory, 
        moderation_decision_engine: ModerationDecisionEngine
    ):
        self._case_repo = case_repo
        self._policy_registry = policy_registry
        self._health_repo = provider_health_repo
        self._moderation_provider_factory = moderation_provider_factory
        self._moderation_decision_engine = moderation_decision_engine

    def execute(self, *, case_id: Optional[UUID], case: Optional[ModerationCase]) -> Result[ModerationCase]:
        """
        Input case_id OR case to process case.
        """
        try:
            if case_id is None and case is None:
                return Error(message="Either case_id or case must be provided", static_msg="MISSING_ARGUMENT")

            # 1. Load case via case_id IF case not given
            case:ModerationCase 
            if not case:
                case = self._case_repo.find_by_id(case_id)
                if not case:
                    return Error(message=f"Case {case_id} not found", static_msg="CASE_NOT_FOUND")
                if case.status != CaseStatusEnum.PENDING:
                    return NotOk(
                        message="Case is not in a pending state",
                        static_msg="CASE_NOT_PENDING",
                        status_code=409,
                    )
            else:
                case = case
            
            # 2. Get ContentToModerateVo
            content_to_moderate:ContentToModerateVo = case.content

            # 3. Active policy
            policy = self._policy_registry.lookup_active_policy(case.policy_routing_key)
            if not policy:
                return Error(message="No active policy found", static_msg="POLICY_NOT_FOUND")

            # 4. Select an available provider (simplified: just OpenAI for now)
            provider_name = self._select_healthy_provider()
            if not provider_name:
                return Error(
                    message="No moderation provider available",
                    static_msg="NO_PROVIDER_AVAILABLE",
                )
            

            provider:IModerationProvider = self._moderation_provider_factory.create(provider_name)
            
            # 5. Send to provider & update IProviderHealthRepository 
            try:
                response:ModerationResponseVo = provider.moderate(case.content)
            except Exception as exc:
                self._record_failure(provider_name)
                logger.exception(f"Moderation provider call failed | provider name: {provider_name}")
                return Error(
                    message=f"Provider error: {exc}",
                    exception=exc,
                    static_msg="PROVIDER_ERROR",
                )

            self._record_success(provider_name)

            # 6. Apply decision engine
            engine = self._moderation_decision_engine
            decision:ModerationDecisionVo
            confidence:ConfidenceScoreVo
            decision, confidence = engine.evaluate(response, policy.confidence_thresholds)

            # 7. Update aggregate
            case.auto_moderate(decision, confidence)
            case.provider_used = ModerationProviderEnum(provider_name)
            self._case_repo.save(case)

            return Ok(case)

        except Exception as exc:
            logger.exception("Unhandled error in ProcessContentForModerationUsecase")
            return Error(message="Internal processing error", exception=exc, static_msg="PROCESSING_ERROR")

    # ---------------------------------------------------------
    #  private helpers
    # ---------------------------------------------------------
    def _select_healthy_provider(self) -> Optional[ModerationProviderEnum]:
        """Simple single-provider strategy; can be extended later.
        selects available provider. 
        """
        return ModerationProviderEnum.OPENAI_API
        # provider_name = ModerationProviderEnum.OPENAI_API
        # health:ProviderHealth = self._health_repo.find_by_provider_name(provider_name)
        # if health and health.is_available():
        #     return provider_name
        # return None

    def _record_success(self, provider_name: ModerationProviderEnum) -> None:
        health = self._get_or_create_health(provider_name)
        health.record_success()
        self._health_repo.save(health)

    def _record_failure(self, provider_name: ModerationProviderEnum) -> None:
        health:ProviderHealth = self._get_or_create_health(provider_name)
        health.record_failure()
        self._health_repo.save(health)

    def _get_or_create_health(self, provider_name: str) -> ProviderHealth:
        health = self._health_repo.find_by_provider_name(provider_name)
        if health is not None:
            return health
        return ProviderHealth(
            provider_name=provider_name,
            error_rate=ErrorRateVo(total_requests=0, total_failures=0),
            sliding_window_metrics=SlidingWindowMetricsVo(
                window_size=100, results=deque()
            ),
            circuit_breaker_state=CircuitBreakerStateEnum.CLOSED,
        )