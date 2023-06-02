from abc import ABC, abstractmethod

from .. import models


class Provider(ABC):
    """Base class for all providers."""

    @abstractmethod
    def get_content(self, id: str) -> models.Content:
        """Get content.

        Args:
            id (str): ID.

        Returns:
            models.Content: Content.
        """
        raise NotImplementedError
