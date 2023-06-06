from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Content:
    """Content."""

    id: str
    title: Optional[str]
    body: Optional[str]
    previous_body: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = None
