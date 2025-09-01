import logging
from fastapi import APIRouter, HTTPException

from ..db.qdrant_client import upsert_embeddings, search_similar_vectors
from ..models.models import EmbeddingBatch, SearchQuery, SearchResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/vectors")
async def upsert_vectors(batch: EmbeddingBatch):
    logger.info(f"Received batch for upsert: {batch}")
    try:
        await upsert_embeddings(batch)
        return {"message": f"Saved {len(batch.embeddings)} embeddings for {batch.url}"}
    except Exception as e:
        logger.exception("Failed to upsert embeddings")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_vectors(search: SearchQuery):
    try:
        results = await search_similar_vectors(search.vector, top_k=search.top_k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
