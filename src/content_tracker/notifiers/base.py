from abc import ABC, abstractmethod
from typing import Sequence

from ..models import ChangedContent, Content


class Notifier(ABC):
    """Base class for all notifiers."""

    @abstractmethod
    def payload_from_contents(self, contents: Sequence[Content]) -> str:
        """Payload from contents.

        Args:
            contents (Sequence[Content]): Contents.

        Returns:
            str: Payload.
        """
        raise NotImplementedError

    @abstractmethod
    def payload_from_changed_contents(
        self, changed_contents: Sequence[ChangedContent]
    ) -> str:
        """Payload from changed contents.

        Args:
            changed_contents (Sequence[ChangedContent]): Changed
                contents.

        Returns:
            str: Payload.
        """
        raise NotImplementedError

    @abstractmethod
    def notify(self, payload: str) -> None:
        """Notify.

        Args:
            payload (str): Payload.
        """
        raise NotImplementedError
