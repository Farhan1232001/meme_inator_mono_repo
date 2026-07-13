from abc import ABC, abstractmethod

from apps.registration.domain.entities.registration_result_entity import RegistrationResultEntity


class IUserRegistrationUsecase(ABC):
    """
    Interface for the User Registration Usecase.
    Defines the contract for creating a user and returning a RegistrationResult.
    """

    @abstractmethod
    def execute(
        self,
        *,
        user_name: str,
        email: str,
        raw_password: str,
    ) -> RegistrationResultEntity:
        """
        Executes the user registration process.

        Args:
            user_name: The desired username.
            email: The user's email address.
            raw_password: The raw or hashed password.

        Raises:
            ValueError: If the username or email already exists.

        Returns:
            A RegistrationResult object containing the created user entity and status info.
        """
        ...