import json
from collections import Counter
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
UNIFIED_DATA_FILE = PROJECT_ROOT / "data" / "normalized" / "unified_data.json"

REQUIRED_FIELDS = {
    "source",
    "doc_id",
    "timestamp",
    "author",
    "content",
    "channel",
    "thread_id",
    "url",
}

REQUIRED_NON_EMPTY_FIELDS = {
    "source",
    "doc_id",
    "timestamp",
    "author",
    "content",
}


def load_documents() -> list[dict]:
    if not UNIFIED_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Missing normalized data file: {UNIFIED_DATA_FILE}"
        )

    payload = json.loads(UNIFIED_DATA_FILE.read_text(encoding="utf-8"))
    documents = payload.get("documents")

    if not isinstance(documents, list):
        raise ValueError("Expected unified_data.json to contain a documents list.")

    return documents


def validate_documents(documents: list[dict]) -> list[str]:
    errors: list[str] = []
    seen_keys: set[tuple[str, str]] = set()

    for index, document in enumerate(documents, start=1):
        missing_fields = REQUIRED_FIELDS - set(document)
        if missing_fields:
            errors.append(
                f"Document {index} is missing fields: {sorted(missing_fields)}"
            )

        for field in REQUIRED_NON_EMPTY_FIELDS:
            if not document.get(field):
                errors.append(f"Document {index} has empty required field: {field}")

        timestamp = document.get("timestamp")
        if timestamp:
            try:
                datetime.fromisoformat(timestamp)
            except ValueError:
                errors.append(f"Document {index} has invalid timestamp: {timestamp}")

        source = document.get("source")
        doc_id = document.get("doc_id")
        document_key = (source, doc_id)
        if source and doc_id:
            if document_key in seen_keys:
                errors.append(f"Duplicate document found: {source}/{doc_id}")
            seen_keys.add(document_key)

    return errors


def print_summary(documents: list[dict]) -> None:
    source_counts = Counter(document["source"] for document in documents)

    print("Ingestion validation summary")
    print("----------------------------")
    print(f"Slack documents: {source_counts.get('slack', 0)}")
    print(f"GitHub documents: {source_counts.get('github', 0)}")
    print(f"Jira documents: {source_counts.get('jira', 0)}")
    print(f"Total documents: {len(documents)}")


def main() -> int:
    documents = load_documents()
    errors = validate_documents(documents)
    print_summary(documents)

    if errors:
        print("\nValidation errors")
        print("-----------------")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

