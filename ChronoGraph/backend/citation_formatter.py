from datetime import datetime
from typing import Any

from backend.normalizer import UnifiedDocument, parse_timestamp


def _format_date(value: datetime | str) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    return parse_timestamp(value).date().isoformat()


def format_citation(source: str, doc_id: str, timestamp: datetime | str) -> str:
    """Format one source citation for narrative answers."""
    return f"[cite: {source}/{doc_id}, {_format_date(timestamp)}]"


def citation_from_document(document: UnifiedDocument | dict[str, Any]) -> str:
    """Create a citation from a normalized document."""
    if isinstance(document, UnifiedDocument):
        return format_citation(
            source=document.source,
            doc_id=document.doc_id,
            timestamp=document.timestamp,
        )

    return format_citation(
        source=document["source"],
        doc_id=document["doc_id"],
        timestamp=document["timestamp"],
    )


def append_citation(text: str, document: UnifiedDocument | dict[str, Any]) -> str:
    """Append a normalized source citation to generated text."""
    return f"{text.rstrip()} {citation_from_document(document)}"

