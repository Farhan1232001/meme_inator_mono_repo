from ninja import Schema
from typing import List, Dict, Any
from domain.value_objects.moderation_response import ModerationResponseVo

class OpenAIModerationApiResponseSchema(Schema):
    """
    Full response from OpenAI Moderation API.
    Used to deserialize and validate the API response.
    """
    id: str
    model: str
    results: List[OpenAIModerationResultItemSchema]
    
    def to_domain(self) -> ModerationResponseVo:
        """
        Convert validated API response to domain value object.
        
        Raises:
            ValueError: If results list is empty
        """
        if not self.results:
            raise ValueError("OpenAI moderation response contains no results")
        
        first = self.results[0]
        
        return ModerationResponseVo(
            flagged=first.flagged,
            categories=first.categories.to_dict(),
            category_scores=first.category_scores.to_dict(),
            applied_input_types=None,  # Not available in standard moderation endpoint
        )

class OpenAICategorySchema(Schema):
    """Categories flagged by OpenAI moderation API."""
    hate: bool = False
    hate_threatening: bool = False
    self_harm: bool = False
    sexual: bool = False
    sexual_minors: bool = False
    violence: bool = False
    violence_graphic: bool = False

    class Config:
        # OpenAI uses 'hate/threatening' etc. in JSON
        # Ninja doesn't support '/' in field names, so we alias them
        fields = {
            'hate_threatening': 'hate/threatening',
            'self_harm': 'self-harm',
            'sexual_minors': 'sexual/minors',
            'violence_graphic': 'violence/graphic',
        }
    
    def to_dict(self) -> Dict[str, bool]:
        """Convert to flat category dict for domain VO."""
        return {
            "hate": self.hate,
            "hate/threatening": self.hate_threatening,
            "self-harm": self.self_harm,
            "sexual": self.sexual,
            "sexual/minors": self.sexual_minors,
            "violence": self.violence,
            "violence/graphic": self.violence_graphic,
        }


class OpenAICategoryScoresSchema(Schema):
    """Confidence scores for each category."""
    hate: float = 0.0
    hate_threatening: float = 0.0
    self_harm: float = 0.0
    sexual: float = 0.0
    sexual_minors: float = 0.0
    violence: float = 0.0
    violence_graphic: float = 0.0

    class Config:
        fields = {
            'hate_threatening': 'hate/threatening',
            'self_harm': 'self-harm',
            'sexual_minors': 'sexual/minors',
            'violence_graphic': 'violence/graphic',
        }
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to flat scores dict for domain VO."""
        return {
            "hate": self.hate,
            "hate/threatening": self.hate_threatening,
            "self-harm": self.self_harm,
            "sexual": self.sexual,
            "sexual/minors": self.sexual_minors,
            "violence": self.violence,
            "violence/graphic": self.violence_graphic,
        }


class OpenAIModerationResultItemSchema(Schema):
    """Individual result item from moderation API."""
    flagged: bool
    categories: OpenAICategorySchema
    category_scores: OpenAICategoryScoresSchema


