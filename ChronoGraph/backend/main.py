from collections import Counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import MOCK_DATA_DIR, NORMALIZED_DATA_DIR
from backend.connectors import GitHubConnector, JiraConnector, SlackConnector
from backend.normalizer import UnifiedDocument, write_unified_documents

app = FastAPI(title="ChronoGraph API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/api/health")
def health() -> dict:
    return {"status": "healthy"}


@app.post("/api/ask")
def ask_question(request: QuestionRequest) -> dict:
    return {
        "question": request.question,
        "answer": "Temporal RAG engine is not connected yet.",
        "cypher_query": None,
        "timeline": [],
    }


@app.post("/api/ingest/mock")
def ingest_mock_data() -> dict:
    documents: list[UnifiedDocument] = []

    slack_file = MOCK_DATA_DIR / "mock_slack.json"
    github_file = MOCK_DATA_DIR / "mock_github.json"
    jira_file = MOCK_DATA_DIR / "mock_jira.json"

    if slack_file.exists():
        documents.extend(SlackConnector(slack_file).fetch_messages())
    if github_file.exists():
        documents.extend(GitHubConnector(github_file).fetch_pull_requests())
    if jira_file.exists():
        documents.extend(JiraConnector(jira_file).fetch_tickets())

    output_file = NORMALIZED_DATA_DIR / "unified_data.json"
    write_unified_documents(documents, output_file)
    source_counts = Counter(document.source for document in documents)

    return {
        "normalized_documents": len(documents),
        "source_counts": {
            "slack": source_counts["slack"],
            "github": source_counts["github"],
            "jira": source_counts["jira"],
        },
        "output_file": str(output_file),
    }

