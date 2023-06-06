from abc import ABC, abstractmethod
from typing import Sequence

from ..models import Content


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
        self, intervals: int = 24, part: str = "HOUR"
    ) -> Sequence[Content]:
        """List changed contents.

        Args:
            intervals (int, optional): A value indicating an interval of time. The unit
                is specified in `part`. Defaults to 24.
            part (str, optional): Unit of time indicated by `intervals`. Defaults to
                "HOUR".

        Returns:
            Sequence[Content]: Changed contents.
        """
        raise NotImplementedError
