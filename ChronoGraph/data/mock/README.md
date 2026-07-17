# Mock data

This directory contains deterministic, synthetic engineering-history data for
ChronoGraph's mock ingestion flow. The fixtures describe an AWS-to-GCP migration
from Slack discussions, GitHub implementation work, and Jira planning. They are
read by `POST /api/ingest/mock` and normalized into
`data/normalized/unified_data.json`.

All timestamps use ISO 8601 date-time strings. URLs use `mock.*` domains and are
references only; they do not point to live services.

## Files

### `mock_slack.json`

Contains a top-level `messages` array (112 records). Each item represents one
Slack message and is ingested as a `slack` document.

| Field | Description |
| --- | --- |
| `id` | Unique mock message ID, such as `slack_001`. |
| `timestamp` | When the message was sent; used as the normalized document timestamp. |
| `user` | Message author; used as the normalized document author. |
| `text` | Message body; used as the normalized document content. |
| `channel` | Slack channel name; used as the normalized document channel. |
| `thread_ts` | Thread identifier, or `null` for a non-threaded message; used as the normalized thread ID. |
| `reactions` | Array of reaction names retained in the fixture for richer mock context. |
| `permalink` | Mock source link; used as the normalized document URL. |

### `mock_github.json`

Contains a top-level `pull_requests` array (25 records). Each item represents a
GitHub pull request and is ingested as a `github` document.

| Field | Description |
| --- | --- |
| `id` | Unique pull-request ID, such as `PR-001`; used as the normalized document ID. |
| `title` | Pull-request title; combined with `description` for normalized content. |
| `author` | Pull-request author; used as the normalized document author. |
| `created_at` | When the pull request was opened; used as the normalized document timestamp. |
| `merged_at` | Merge time for merged pull requests, otherwise `null`. |
| `status` | Pull-request state, such as `merged`, `closed`, or `open`. |
| `repository` | Repository name; used as the normalized document channel. |
| `description` | Pull-request description; combined with `title` for normalized content. |
| `comments` | Review/discussion comments, each with `author`, `created_at`, and `body`. |
| `labels` | Array of labels associated with the pull request. |
| `url` | Mock pull-request link; used as the normalized document URL. |

### `mock_jira.json`

Contains a top-level `tickets` array (35 records). Each item represents a Jira
ticket and is ingested as a `jira` document.

| Field | Description |
| --- | --- |
| `id` | Unique ticket ID, such as `JIRA-001`; used as the normalized document ID. |
| `title` | Ticket title; combined with `description` for normalized content. |
| `assignee` | Ticket assignee; used as the normalized document author. |
| `status` | Current workflow status, such as `To Do`, `In Progress`, or `Done`. |
| `created_at` | When the ticket was created; used as the normalized document timestamp. |
| `updated_at` | Most recent ticket update time. |
| `description` | Ticket description; combined with `title` for normalized content. |
| `comments` | Ticket comments, each with `author`, `created_at`, and `body`. |
| `status_history` | Ordered status changes, each with `status` and `changed_at`. |
| `priority` | Ticket priority. |
| `project` | Jira project key; used as the normalized document channel. |
| `url` | Mock ticket link; used as the normalized document URL. |

## Regenerating fixtures

Run the generator from the project root when the mock story needs to change:

```powershell
python generate_mock_data.py
```

The generator uses a fixed random seed, so it produces repeatable fixture data.
