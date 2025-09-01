# 🧠 AI Assistant Service

This service processes user queries by returning AI-generated answers using OpenAI.

## 🔄 Pipeline

1. **Receive a user question** - `POST /api/process-question`
2. **Forward the question to the system** - the service queries Qdrant to get the most relevant context vectors.
3. **Generate an AI answer** - `services/openai_service.py::get_answer_from_llm()`
4. **Return** the generated answer to the user.

## 🛠️ Technologies

- `fastapi` - API for handling user queries and health checks
- `uvicorn[standard]` - server for FastAPI
- `httpx` - async HTTP client
- `openai` - client for accessing OpenAI API (embeddings and completions)
- `pydantic`, `pydantic-settings` - validation, configuration from `.env`
- `python-dotenv` - `.env` file support

## 🚀 Usage

Run via Docker:

```bash
    docker-compose up --build ai_assistant_service
