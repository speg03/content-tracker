from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from itertools import groupby, tee
from operator import attrgetter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

from ..models import Content
from .base import Database


class InstanceStore(Database):
    def __init__(self):
        self.contents: Dict[str, Content] = {}
        self.content_histories: List[Content] = []

    def insert_or_update_content(self, content: Content) -> None:
        if content.id in self.contents:
            # Update content
            self.contents[content.id].title = content.title
            self.contents[content.id].body = content.body
            self.contents[content.id].updated_at = content.created_at
        else:
            # Insert content
            self.contents[content.id] = Content(
                id=content.id,
                title=content.title,
                body=content.body,
                created_at=content.created_at,
                updated_at=content.created_at,
            )

        # Insert content history
        content_history = Content(
            id=content.id,
            title=content.title,
            body=content.body,
            created_at=content.created_at,
        )
        self.content_histories.append(content_history)

    def list_contents(self) -> Sequence[Content]:
        return self.contents.values()

    def list_changed_contents(
        self, interval: int = 24, part: str = "HOUR"
    ) -> Sequence[Content]:
        # Validate part for datetime.timedelta
        # see: https://docs.python.org/ja/3/library/datetime.html#datetime.timedelta
        valid_parts = (
            "MICROSECOND",
            "MILLISECOND",
            "SECOND",
            "MINUTE",
            "HOUR",
            "DAY",
            "WEEK",
        )
        if part.upper() not in valid_parts:
            raise ValueError(
                f"Invalid part: {part}. Valid parts are {', '.join(valid_parts)}."
            )

        # Create a deep copy in the original order
        histories = [Content(**asdict(h)) for h in self.content_histories]

        # Set previous_body for each deep-copied history
        sorted_histories = sorted(histories, key=attrgetter("id", "created_at"))
        for _, g in groupby(sorted_histories, key=attrgetter("id")):
            for lhs, rhs in _pairwise(g):
                rhs.previous_body = lhs.body

        # Filter histories that matches the criteria in the original order
        delta = timedelta(**{f"{part.lower()}s": interval})  # timedelta(hours=24)
        ref = datetime.now(timezone.utc) - delta
        changed_histories = [
            h for h in histories if h.created_at >= ref and h.previous_body != h.body
        ]
        return changed_histories


T = TypeVar("T")


def _pairwise(iterable: Iterable[T]) -> Iterable[Tuple[T, T]]:
    """s -> (s0,s1), (s1,s2), (s2, s3), ...

    itertools.pairwise requires Python 3.10 or higher. The implementation here is for
    cases where a Python version less than that is used.
    see: https://docs.python.org/ja/3/library/itertools.html#itertools.pairwise
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
