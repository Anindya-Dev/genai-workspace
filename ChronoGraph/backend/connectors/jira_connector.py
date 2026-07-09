import json
from pathlib import Path

from backend.normalizer import UnifiedDocument, parse_timestamp


class JiraConnector:
    """Reads Jira ticket records from a mock JSON file."""

    def __init__(self, mock_file: str | Path):
        self.mock_file = Path(mock_file)

    def fetch_tickets(self) -> list[UnifiedDocument]:
        payload = json.loads(self.mock_file.read_text(encoding="utf-8"))

        documents: list[UnifiedDocument] = []
        for ticket in payload.get("tickets", []):
            content = f"{ticket['title']}\n\n{ticket.get('description', '')}".strip()
            documents.append(
                UnifiedDocument(
                    source="jira",
                    doc_id=ticket["id"],
                    timestamp=parse_timestamp(ticket["created_at"]),
                    author=ticket["assignee"],
                    content=content,
                    channel=ticket.get("project"),
                    url=ticket.get("url"),
                )
            )
        return documents

