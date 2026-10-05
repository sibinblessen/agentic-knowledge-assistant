# Agentic Knowledge Assistant

A LangGraph agent running on Gemini (Google Cloud), backed by a RAG retrieval API
over Postgres + pgvector. Work in progress.

## Status
- [x] Step 0 - Google Cloud setup + smoke test (`scripts/check_vertex.py`)
- [x] Step 1 - Ingestion: load -> chunk -> embed -> store
- [ ] Step 2 - Retrieval API (FastAPI `/search`)
- [ ] Step 3 - LangGraph agent: plan -> retrieve -> answer -> grounding check
- [ ] Step 4 - Deploy: Cloud Run + Cloud SQL
- [ ] Step 5 - Architecture diagram + design decisions
