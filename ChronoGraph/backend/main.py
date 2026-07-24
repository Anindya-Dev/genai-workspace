import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.config import MOCK_DATA_DIR, NORMALIZED_DATA_DIR
from backend.connectors import GitHubConnector, JiraConnector, SlackConnector
from backend.normalizer import (
    UnifiedDocument,
    summarize_documents,
    write_unified_documents,
)
from backend.extractor import GraphExtractor
from backend.normalizer import parse_timestamp

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


class HealthResponse(BaseModel):
    status: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    cypher_query: str | None = None
    timeline: list[dict] = Field(default_factory=list)


class IngestMockResponse(BaseModel):
    normalized_documents: int
    source_counts: dict[str, int]
    missing_files: list[str] = Field(default_factory=list)
    output_file: str


@app.get("/api/health", response_model=HealthResponse)
def health() -> dict:
    return {"status": "healthy"}


@app.post("/api/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> dict:
    return {
        "question": request.question,
        "answer": "Temporal RAG engine is not connected yet.",
        "cypher_query": None,
        "timeline": [],
    }


@app.post("/api/ingest/mock", response_model=IngestMockResponse)
def ingest_mock_data() -> dict:
    documents: list[UnifiedDocument] = []
    missing_files: list[str] = []

    slack_file = MOCK_DATA_DIR / "mock_slack.json"
    github_file = MOCK_DATA_DIR / "mock_github.json"
    jira_file = MOCK_DATA_DIR / "mock_jira.json"

    if slack_file.exists():
        documents.extend(SlackConnector(slack_file).fetch_messages())
    else:
        missing_files.append(str(slack_file))

    if github_file.exists():
        documents.extend(GitHubConnector(github_file).fetch_pull_requests())
    else:
        missing_files.append(str(github_file))

    if jira_file.exists():
        documents.extend(JiraConnector(jira_file).fetch_tickets())
    else:
        missing_files.append(str(jira_file))

    output_file = NORMALIZED_DATA_DIR / "unified_data.json"
    write_unified_documents(documents, output_file)

    return {
        "normalized_documents": len(documents),
        "source_counts": summarize_documents(documents),
        "missing_files": missing_files,
        "output_file": str(output_file),
    }


@app.post("/api/extract/test")
def test_extraction():
    normalized_file = NORMALIZED_DATA_DIR / "unified_data.json"
    if not normalized_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Normalized data not found. Run POST /api/ingest/mock first.",
        )

    with open(normalized_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = data["documents"][0]

    document = UnifiedDocument(
        source=doc["source"],
        doc_id=doc["doc_id"],
        timestamp=parse_timestamp(doc["timestamp"]),
        author=doc["author"],
        content=doc["content"],
        channel=doc.get("channel"),
        thread_id=doc.get("thread_id"),
        url=doc.get("url"),
    )

    try:
        extractor = GraphExtractor()
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    extractor.extract(document)

    return {"status": "Extraction completed. Check terminal for LLM output."}
