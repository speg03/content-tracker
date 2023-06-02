from abc import ABC, abstractmethod


class Notifier(ABC):
    """Base class for all notifiers."""

    @abstractmethod
    def notify(self, payload: str) -> None:
        """Notify.

        Args:
            payload (str): Payload.
        """
        raise NotImplementedError
