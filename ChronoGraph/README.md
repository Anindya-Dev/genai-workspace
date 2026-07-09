# ChronoGraph

Temporal GraphRAG for enterprise forensics.

This project turns historical engineering data from Slack, GitHub, and Jira into
a temporal knowledge graph. Users can ask questions about past decisions and get
chronological, cited answers.

## Backend

The backend is owned by Anindya for the ingestion, API, citation, and integration
pipeline.

```bash
cd ChronoGraph
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

API docs will be available at:

```text
http://localhost:8000/docs
```

