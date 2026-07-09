import json
from pathlib import Path

from backend.normalizer import UnifiedDocument, parse_timestamp


class SlackConnector:
    """Reads Slack messages from a mock JSON file."""

    def __init__(self, mock_file: str | Path):
        self.mock_file = Path(mock_file)

    def fetch_messages(self) -> list[UnifiedDocument]:
        payload = json.loads(self.mock_file.read_text(encoding="utf-8"))

        documents: list[UnifiedDocument] = []
        for message in payload.get("messages", []):
            documents.append(
                UnifiedDocument(
                    source="slack",
                    doc_id=message["id"],
                    timestamp=parse_timestamp(message["timestamp"]),
                    author=message["user"],
                    content=message["text"],
                    channel=message.get("channel"),
                    thread_id=message.get("thread_ts"),
                    url=message.get("permalink"),
                )
            )
        return documents

