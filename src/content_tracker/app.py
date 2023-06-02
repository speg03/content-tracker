import logging

from .databases import Database
from .providers import Provider


class Application:
    def __init__(self, provider: Provider, database: Database) -> None:
        self.provider = provider
        self.database = database

        self._logger = logging.getLogger(__name__)

    def add_content(self, id: str) -> None:
        content = self.provider.get_content(id)
        self.database.insert_or_update_content(content)
        self.database.insert_content_history(content)

    def list_changes(self, interval_months: int = 6) -> None:
        changes = self.database.list_changed_contents(interval_months)
        for change in changes:
            self._logger.info(f"Changed content {change.id}: {change.title}")
