import httpx
import logging

logger = logging.getLogger(__name__)


async def send_chunks_to_embedding(url: str, chunks: list[str]):
    """
    Send chunks to embedding service and return response JSON.
    """
    embedding_url = "http://embedding_service:8000/embed-text"
    payload = {"url": url, "chunks": chunks}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(embedding_url, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.ReadTimeout:
            logger.error("Embedding service timed out for url=%s", url)
            return None
        except httpx.HTTPStatusError as e:
            logger.error("Embedding service returned HTTP error: %s", e)
            return None
        except Exception as e:
            logger.exception("Unexpected error while calling embedding service")
            return None
