import uuid
import httpx
import logging
from typing import Any
from ..core.settings import settings

logger = logging.getLogger(__name__)
NAMESPACE_UUID = uuid.UUID("12345678-1234-5678-1234-567812345678")


def generate_embedding_id(url: str, chunk: str) -> str:
    return str(uuid.uuid5(NAMESPACE_UUID, f"{url}_{chunk}"))


async def send_vectors_to_qdrant(url: str, embeddings: list[list[float]]):
    qdrant_url = f"{settings.QDRANT_URL}/qdrant/vectors"
    vectors_payload = [
        {
            "id": generate_embedding_id(url, f"chunk_{i}"),
            "vector": vec,
            "payload": {
                "url": url,
                "chunk": f"chunk_{i}"
            }
        }
        for i, vec in enumerate(embeddings)
    ]

    payload = {
        "url": url,
        "embeddings": vectors_payload
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(qdrant_url, json=payload)
        response.raise_for_status()
        return response.json()


async def query_qdrant(vector: list[float], top_k: int = 5) -> Any:
    async with httpx.AsyncClient() as client:
        qdrant_url = f"{settings.QDRANT_URL}/qdrant/search"

        response = await client.post(qdrant_url, json={
            "vector": vector,
            "top_k": top_k
        })
        response.raise_for_status()
        return response.json()
