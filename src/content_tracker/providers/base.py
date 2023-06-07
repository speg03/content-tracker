from abc import ABC, abstractmethod

from ..models import Content


class Provider(ABC):
    """Base class for all providers."""

    @abstractmethod
    def get_content(self, id: str) -> Content:
        """Get content.

        Args:
            id (str): ID.

        Returns:
            Content: Content.
        """
        raise NotImplementedError  # pragma: no cover
