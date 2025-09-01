# 🧠 Ingestor Service

This service fetches, cleans, and splits web page content into chunks for vector embedding.

## 🔄 Pipeline

1. **Collect URLs** - `parser/website_urls.py::URLS`
2. **Fetch HTML** - `parser/fetcher.py::fetch_url()`
3. **Remove navigation, footers, scripts** - `parser/extractor.py::extract_content()`
4. **Normalize text (spaces, newlines)** - `parser/normalizer.py::normalize_text()`
5. **Split into chunks** - `services/text_processing.py::split_text()`
6. **Send chunks to embedding_service** - `services/send_chunks.py::send_chunks_to_embedding()`
7. **Asynchronous processing via Celery** - `celery/tasks.py::ingest_url_task()`

## 🛠️ Technologies

- `beautifulsoup4` - HTML parsing
- `requests` - HTML fetching
- `pydantic`, `pydantic-settings` - validation, configuration from `.env`
- `celery` - asynchronous tasks
- `redis` - broker for Celery
- `httpx` - async HTTP client
- `fastapi` - API for running tasks and health checks
- `uvicorn[standard]` - server for FastAPI
- `python-dotenv` - `.env` file support

## 🚀 Usage

Run via Docker:

```bash
    docker-compose up --build redis celery_worker_ingestor ingestor_service

