# ChronoGraph

**Temporal GraphRAG for Enterprise Forensics**

ChronoGraph is an advanced Generative AI project that helps engineering teams
understand historical technical decisions from enterprise communication data.
It ingests mock Slack messages, GitHub pull requests, and Jira tickets, converts
them into a unified document format, and prepares the data for knowledge graph
extraction, temporal retrieval, and cited narrative answers.

## Project Goal

Traditional RAG systems are good at finding related text, but they often lose
timeline and relationship context. ChronoGraph is designed to answer questions
such as:

```text
Why did the team migrate from AWS to GCP in 2023?
Who supported the decision, who raised concerns, and what changed over time?
```

The final system will generate a chronological answer backed by citations from
the original enterprise records.

## Core Capabilities

- Ingest historical data from Slack, GitHub, and Jira sources.
- Normalize source-specific records into one common document schema.
- Extract entities and relationships for graph construction.
- Store temporal knowledge in Neo4j.
- Translate natural language questions into graph queries.
- Generate cited, chronological answers using a Temporal GraphRAG pipeline.
- Provide a frontend chat interface with timeline visualization.

## The current implementation includes:

- FastAPI application entry point.
- Slack, GitHub, and Jira mock-data connectors.
- Unified document schema for normalized ingestion.
- Mock ingestion endpoint for generating normalized data.
- Initial graph schema definitions (entities and relationships).
- Initial graph extractor module scaffold for future LLM-based extraction.
- Project structure for backend, mock data, graph extraction, and normalized output.

## Repository Structure

```text
genai-workspace/
├── ChronoGraph/
│   ├── backend/
│   │   ├── connectors/
│   │   │   ├── github_connector.py
│   │   │   ├── jira_connector.py
│   │   │   └── slack_connector.py
│   │   ├── config.py
│   │   ├── extractor.py
│   │   ├── main.py
│   │   ├── normalizer.py
│   │   └── schema.py
│   ├── data/
│   │   ├── mock/
│   │   └── normalized/
│   ├── README.md
│   └── requirements.txt
├── .gitignore
└── README.md
```

## Team Responsibilities

| Member | Role | Primary Ownership |
| --- | --- | --- |
| Anindya Bhattacharya | Team Lead and RAG Pipeline Engineer | Data ingestion, FastAPI backend, normalization, citations, integration |
| Arik Chakraborty | AI Backend Lead | Graph extraction, Temporal RAG engine, Cypher generation, narrative generation |
| Suryakala M | Full Stack and Database Engineer | Neo4j setup, graph ingestion, React UI, timeline visualization |
| Jaimin Bhadra | Frontend and Testing Support | Mock data, frontend support, API testing, documentation |

## Technology Stack

| Layer | Technology |
| --- | --- |
| Backend API | FastAPI, Pydantic |
| Data Processing | Python |
| Graph Database | Neo4j |
| GraphRAG / LLM | LangChain, LlamaIndex, Groq or Ollama |
| Frontend | React, Vite, Tailwind CSS |
| Visualization | vis.js or React Flow |

## Backend Setup

From the repository root:

```bash
cd ChronoGraph
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Available API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/health` | Checks whether the backend is running |
| POST | `/api/ask` | Placeholder endpoint for future Temporal RAG answers |
| POST | `/api/ingest/mock` | Reads mock source files and writes normalized documents |

## Data Normalization Flow

```text
mock_slack.json   -> SlackConnector   -> UnifiedDocument
mock_github.json  -> GitHubConnector  -> UnifiedDocument
mock_jira.json    -> JiraConnector    -> UnifiedDocument

UnifiedDocument[] -> data/normalized/unified_data.json
```

Each normalized document follows this common schema:

```json
{
  "source": "slack",
  "doc_id": "slack_001",
  "timestamp": "2023-01-10T00:00:00",
  "author": "rahul.sharma",
  "content": "Our AWS bill increased by 40% during the last six months.",
  "channel": "#engineering",
  "thread_id": null,
  "url": "https://mock.slack/001"
}
```

## Graph Extraction (Work in Progress)

The graph extraction module is responsible for transforming normalized
documents into a structured knowledge graph.

The current implementation includes:

- Initial graph schema defining supported entity types.
- Initial relationship schema for enterprise knowledge extraction.
- Graph extractor scaffold that will process `UnifiedDocument` objects.
- Planned integration with LlamaIndex and Groq for automated entity and relationship extraction.

Supported Entity Types:

- Person
- Technology
- Organization
- Concept
- Project

Supported Relationship Types:

- ADVOCATED_FOR
- ARGUED_AGAINST
- MIGRATED_FROM
- MIGRATED_TO
- COMMITTED_CODE
- WORKS_ON

## Planned Milestones

### Week 1: Foundation and Data Pipeline

- Build mock data for Slack, GitHub, and Jira.
- Implement connectors for each source.
- Normalize all source data into a shared schema.
- Initial graph schema completed.
- Graph extraction module scaffold created.
- Begin LLM-powered entity and relationship extraction.

### Week 2: Graph Database and Frontend Scaffold

- Set up Neo4j constraints and indexes.
- Ingest extracted triples into Neo4j.
- Scaffold React frontend and chat UI.
- Create initial timeline visualization.

### Week 3: Temporal RAG and Citations

- Convert user questions into Cypher queries.
- Retrieve and sort subgraphs chronologically.
- Generate narrative answers with citations.
- Connect frontend and backend.

### Week 4: Polish and Final Review

- Add error handling, caching, and fallback behavior.
- Improve conversation memory and follow-up questions.
- Complete documentation and demo script.
- Run end-to-end testing for final presentation.

## Git Workflow

Each member works on their own branch and commits meaningful progress daily.

```bash
git checkout Anindya
git add .
git commit -m "feat: add ingestion connector"
git push origin Anindya
```

Main branch should contain reviewed, stable work.

## Review Focus

The project will be evaluated on:

- Implementation completeness.
- Daily GitHub activity and commit discipline.
- Code quality and documentation.
- Team collaboration and integration.

## Project Status

ChronoGraph is currently in the Week 1 foundation phase.

Completed:
- Backend ingestion scaffold.
- Mock source connectors.
- Unified document normalization pipeline.
- Initial graph schema definitions.
- Graph extraction module scaffold.

Next Steps:
- Integrate LlamaIndex/Groq for entity and relationship extraction.
- Generate graph triples from normalized documents.
- Prepare graph ingestion into Neo4j.
