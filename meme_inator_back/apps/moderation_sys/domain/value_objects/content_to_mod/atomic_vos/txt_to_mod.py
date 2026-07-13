from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TextToModerateVo:
    """Text content to moderate."""
    text: str
    language: Optional[str] = None

    def __post_init__(self):
        """Validate text content."""
        if not self.text or not self.text.strip():
            raise ValueError("Text content cannot be empty")
        if len(self.text) > 1000000:  # Example limit: 1MB of text
            raise ValueError("Text content exceeds maximum length")


