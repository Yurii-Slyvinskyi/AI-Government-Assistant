# 🧠 Embedding Service

This service creates embedding vectors for text using OpenAI.

## 🔄 Pipeline

1. **Retrieving text chunks** - via API `/embed-text`
2. **Generating embedding vectors** - `services/openai_client::get_embedding_async()`
3. **Writing vectors to Qdrant** - `services/qdrant_client::send_vectors_to_qdrant()`


1. **Receiving search queries** - via API `/embed-question`
2. **Creating an embedding for a query** - again `get_embedding_async()`
3. **Searching for the nearest vectors in Qdrant** - `services/qdrant_client::query_qdrant()`

## 🛠️ Technologies

- `fastapi` - API for running tasks and health checks
- `uvicorn[standard]` - server for FastAPI
- `qdrant-client` - client for interacting with Qdrant
- `pydantic`, `pydantic-settings` - validation and configuration from `.env`
- `python-dotenv` - `.env` file support
- `httpx` - async HTTP client
- `openai` - client for accessing OpenAI API (creating embeddings)

## 🚀 Usage

Run via Docker:

```bash
    docker-compose up --build embedding_service

