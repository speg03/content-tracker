import logging
import urllib.request

from .base import Notifier


class Webhook(Notifier):
    """Webhook notifier."""

    def __init__(
        self,
        url: str,
        content_type: str = "application/json",
        timeout_seconds: int = 10,
    ) -> None:
        """Initialize.

        Args:
            url (str): URL.
            content_type (str, optional): Content type. Defaults to "application/json".
            timeout_seconds (int, optional): Timeout seconds. Defaults to 10.
        """
        self.url = url
        self.content_type = content_type
        self.timeout_seconds = timeout_seconds

        self._logger = logging.getLogger(__name__)

    def notify(self, payload: str) -> None:
        headers = {"Content-type": self.content_type}
        req = urllib.request.Request(self.url, payload.encode(), headers)
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
            the_page: bytes = response.read()

        self._logger.info(the_page.decode())
