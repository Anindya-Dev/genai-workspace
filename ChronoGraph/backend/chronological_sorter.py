from datetime import datetime
from typing import Any

from backend.normalizer import UnifiedDocument, parse_timestamp


def get_event_timestamp(event: UnifiedDocument | dict[str, Any]) -> datetime:
    """Return a comparable timestamp from a document or event dictionary."""
    if isinstance(event, UnifiedDocument):
        return event.timestamp

    timestamp = event.get("timestamp") or event.get("created_at") or event.get("date")
    if isinstance(timestamp, datetime):
        return timestamp
    if isinstance(timestamp, str):
        return parse_timestamp(timestamp)

    raise ValueError(f"Event is missing a valid timestamp: {event}")


def sort_chronologically(
    events: list[UnifiedDocument | dict[str, Any]],
) -> list[UnifiedDocument | dict[str, Any]]:
    """Sort normalized documents or graph events from oldest to newest."""
    return sorted(events, key=get_event_timestamp)


def group_by_month(
    events: list[UnifiedDocument | dict[str, Any]],
) -> dict[str, list[UnifiedDocument | dict[str, Any]]]:
    """Group events by YYYY-MM after chronological sorting."""
    grouped_events: dict[str, list[UnifiedDocument | dict[str, Any]]] = {}

    for event in sort_chronologically(events):
        month_key = get_event_timestamp(event).strftime("%Y-%m")
        grouped_events.setdefault(month_key, []).append(event)

    return grouped_events

