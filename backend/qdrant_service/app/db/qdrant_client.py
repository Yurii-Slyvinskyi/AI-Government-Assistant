import logging
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.http.models import Distance, VectorParams
from typing import List

from ..core.settings import settings
from ..models.models import EmbeddingBatch, SearchResult

COLLECTION_NAME = "gov_faqs"
logger = logging.getLogger(__name__)

if settings.QDRANT_URL:
    client = QdrantClient(
        url=settings.QDRANT_URL,
        # api_key=settings.QDRANT_API_KEY
    )
else:
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT
    )


# Initial Data
def init_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )


# Save data to Qdrant
async def upsert_embeddings(batch: EmbeddingBatch):
    points = [
        PointStruct(
            id=embedding.id,
            vector=embedding.vector,
            payload=embedding.payload,
        )
        for embedding in batch.embeddings
    ]

    if not batch.embeddings:
        return

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# Search Similar Vectors
async def search_similar_vectors(vector: List[float], top_k: int = 5) -> List[SearchResult]:
    try:
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=top_k,
            with_payload=True
        )

        results = []
        for hit in search_result:
            result = SearchResult(
                id=str(hit.id),
                score=hit.score,
                payload=hit.payload or {}
            )
            results.append(result)

        return results

    except Exception as e:
        raise RuntimeError(f"Qdrant search failed: {str(e)}")
