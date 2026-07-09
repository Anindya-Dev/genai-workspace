from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class UnifiedDocument:
    """Common schema for Slack, GitHub, and Jira source records."""

    source: str
    doc_id: str
    timestamp: datetime
    author: str
    content: str
    channel: str | None = None
    thread_id: str | None = None
    url: str | None = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


def parse_timestamp(value: str) -> datetime:
    """Parse ISO timestamps from mock/API data."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def write_unified_documents(
    documents: Iterable[UnifiedDocument],
    output_file: str | Path,
) -> None:
    """Write normalized documents to JSON for graph extraction."""
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "documents": [document.to_dict() for document in documents],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

