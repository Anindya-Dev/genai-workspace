import json
from pathlib import Path

from backend.normalizer import UnifiedDocument, parse_timestamp


class GitHubConnector:
    """Reads GitHub pull request records from a mock JSON file."""

    def __init__(self, mock_file: str | Path):
        self.mock_file = Path(mock_file)

    def fetch_pull_requests(self) -> list[UnifiedDocument]:
        payload = json.loads(self.mock_file.read_text(encoding="utf-8"))

        documents: list[UnifiedDocument] = []
        for pr in payload.get("pull_requests", []):
            content = f"{pr['title']}\n\n{pr.get('description', '')}".strip()
            documents.append(
                UnifiedDocument(
                    source="github",
                    doc_id=pr["id"],
                    timestamp=parse_timestamp(pr["created_at"]),
                    author=pr["author"],
                    content=content,
                    channel=pr.get("repository"),
                    url=pr.get("url"),
                )
            )
        return documents

