from abc import ABC, abstractmethod


class IValidateProfileUsecase(ABC):
    """
    Attributes:
        - profile_repo: IProfileRepository
    Behavior:
        run domain validation rules (raises on invalid)
    """

    def __init__(self, profile_repo: IProfileRepository) -> None:
        self.profile_repo = profile_repo

    @abstractmethod
    def execute(self, profile_data: Dict[str, Any]) -> None:
        """Validate profile data according to domain rules; raise ValueError or custom error if invalid."""
        raise NotImplementedError