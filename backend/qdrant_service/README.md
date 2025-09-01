# 🧠 Qdrant Service

This service stores vectors (embeddings) in the Qdrant database and performs similar vector searches for the RAG
project.

## 🔄 Pipeline

1. **Receive vectors from embedding_service** - `POST /qdrant/vectors`
2. **Store in Qdrant** - `db/qdrant_client.py::upsert_embeddings()`


1. **Receive a user query** - `POST /qdrant/search`
2. **Search for similar vectors** - `db/qdrant_client.py::search_similar_vectors()`

## 🛠️ Technologies

- `fastapi` - API for running tasks and health checks
- `uvicorn[standard]` - server for FastAPI
- `qdrant-client` - integration with Qdrant
- `pydantic`, `pydantic-settings` - validation, configuration from `.env`
- `python-dotenv` - `.env` file support

## 🚀 Usage

Run via Docker:

```bash
    docker-compose up --build qdrant embedding_service ai_assistant_service qdrant_service

