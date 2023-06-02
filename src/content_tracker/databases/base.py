from abc import ABC, abstractmethod
from typing import Sequence

from ..models import ChangedContent, Content


class Database(ABC):
    """Base class for all databases."""

    @abstractmethod
    def insert_or_update_content(self, content: Content) -> None:
        """Insert or update content.

        Args:
            content (Content): Content.
        """
        raise NotImplementedError

    @abstractmethod
    def insert_content_history(self, content: Content) -> None:
        """Insert content history.

        Args:
            content (Content): Content.
        """
        raise NotImplementedError

    @abstractmethod
    def list_contents(self) -> Sequence[Content]:
        """List contents.

        Returns:
            Sequence[Content]: Contents.
        """
        raise NotImplementedError

    @abstractmethod
    def list_changed_contents(
        self, interval_months: int = 6
    ) -> Sequence[ChangedContent]:
        """List changed contents.

        Args:
            interval_months (int, optional): Interval months. Defaults to 6.

        Returns:
            Sequence[ChangedContent]: Changed contents.
        """
        raise NotImplementedError
