# domain/services/moderation_decision_engine.py

from apps.moderation_sys.domain.enums.moderation_enums import ConfidenceBandEnum, DecisionEnum, ModerationActionEnum, ModerationProviderEnum, VisibilityEffectEnum
from apps.moderation_sys.domain.value_objects.confidence_score import ConfidenceScoreVo
from apps.moderation_sys.domain.value_objects.confidence_thresholds import ConfidenceThresholdsVo
from apps.moderation_sys.domain.value_objects.moderation_action import ModerationActionVo
from apps.moderation_sys.domain.value_objects.moderation_decision import ModerationDecisionVo
from apps.moderation_sys.domain.value_objects.moderation_response import ModerationResponseVo

# domain/services/moderation_decision_engine.py

class ModerationDecisionEngine:
    """
    Makes automated moderation decisions based on API risk scores.
    
    Uses standard moderation API scoring model:
    Higher scores = higher violation risk = should be rejected.
    Lower scores = lower violation risk = should be accepted.
    
    Decision logic:
    - score >= HIGH_RISK_THRESHOLD  → REJECT immediately (clear violation)
    - score < LOW_RISK_THRESHOLD    → ACCEPT immediately (clearly safe)
    - Otherwise                      → FLAG for human review (uncertain)
    
    This aligns with how most production APIs work:
    OpenAI, Google Perspective, AWS Rekognition, Azure Content Moderator, etc.
    """

    def evaluate(
        self,
        response: ModerationResponseVo,
        thresholds: ConfidenceThresholdsVo,
    ) -> tuple[ModerationDecisionVo, ConfidenceScoreVo]:
        """
        Produces an automated moderation decision based on the provider's response
        and the policy's risk thresholds.
        
        Args:
            response: Raw moderation API response with risk scores
            thresholds: Policy-defined risk thresholds
            
        Returns:
            Tuple of (decision, confidence_score)
        """
        match response.provider:
            case ModerationProviderEnum.OPENAI_API:
                return self._evaluate_response_from_openai(response, thresholds)
            case _:
                raise NotImplementedError(
                    f"Provider {response.provider} not yet supported"
                )

    def _evaluate_response_from_openai(
        self,
        response: ModerationResponseVo,
        thresholds: ConfidenceThresholdsVo,
    ) -> tuple[ModerationDecisionVo, ConfidenceScoreVo]:
        """
        Evaluate OpenAI moderation response.
        
        OpenAI returns per-category violation probabilities (0-1).
        We take the maximum violation probability as our risk score.
        Higher scores = more likely to be violating content.
        """
        # OpenAI's category_scores are violation probabilities (0-1)
        # 1. We use the highest one as our risk score
        risk_score = response.highest_score
        highest_category = response.highest_category or "unknown"
        
        confidence = ConfidenceScoreVo(value=risk_score)
        band = thresholds.classify_confidence(confidence)
        
        # 2. Map risk bands to decisions
        if band == ConfidenceBandEnum.HIGH:
            # Clear violation → auto-reject
            outcome = DecisionEnum.REJECT
            reason:str = (
                f"High-risk content detected in '{highest_category}' "
                f"(risk score: {risk_score:.4f})"
            )
        elif band == ConfidenceBandEnum.LOW:
            # Clearly safe → auto-accept
            outcome = DecisionEnum.ACCEPT
            reason:str = (
                f"Low-risk content (risk score: {risk_score:.4f})"
            )
        else:  # GREY zone
            # Uncertain → flag for human review
            outcome = DecisionEnum.FLAG
            reason:str = (
                f"Uncertain risk in '{highest_category}' "
                f"(risk score: {risk_score:.4f})"
            )
        
        decision = ModerationDecisionVo(
            outcome=outcome,
            reason_code=highest_category,
            note=reason,
        )
        return decision, confidence