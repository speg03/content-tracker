import logging
from typing import Optional

from .databases.base import Database
from .notifiers.base import Notifier
from .providers.base import Provider


class ContentTracker:
    def __init__(
        self,
        provider: Provider,
        database: Database,
        notifier: Optional[Notifier] = None,
    ) -> None:
        self.provider = provider
        self.database = database
        self.notifier = notifier

        self._logger = logging.getLogger(__name__)

    def add_content(self, id: str, notify: bool = False) -> None:
        content = self.provider.get_content(id)
        self.database.insert_or_update_content(content)

        self._logger.info(f"Added content: {content}")
        if notify and self.notifier:
            payload = self.notifier.payload_from_contents([content])
            self.notifier.notify(payload)

    def list_contents(self, notify: bool = False) -> None:
        contents = self.database.list_contents()

        self._logger.info("List contents:")
        for content in contents:
            self._logger.info(content)

        if notify and self.notifier:
            payload = self.notifier.payload_from_contents(contents)
            self.notifier.notify(payload)

    def list_changes(
        self, intervals: int = 24, part: str = "HOUR", notify: bool = False
    ) -> None:
        contents = self.database.list_changed_contents(intervals, part)

        self._logger.info("List changes:")
        for content in contents:
            self._logger.info(content)

        if notify and self.notifier:
            payload = self.notifier.payload_from_changed_contents(contents)
            self.notifier.notify(payload)
