import logging
import openai
from fastapi import APIRouter, HTTPException
import traceback

from ..models.models import TextChunksRequest, QueryRequest, StatusResponse, SearchResponse
from ..services.openai_client import get_embedding_async
from ..services.qdrant_client import send_vectors_to_qdrant, query_qdrant

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/embed-text", response_model=StatusResponse)
async def embed_text(data: TextChunksRequest):
    embeddings = []
    success_count = 0
    rate_limit_count = 0

    for chunk in data.chunks:
        try:
            embedding = await get_embedding_async(chunk)
            embeddings.append(embedding)
            success_count += 1
        except openai.RateLimitError:
            rate_limit_count += 1
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding error: {e}")

    qdrant_status = "disabled"
    if embeddings:
        try:
            qdrant_response = await send_vectors_to_qdrant(data.url, embeddings)
            qdrant_status = qdrant_response.get("status", "disabled")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Qdrant error: {e}")

    return {
        "status": "success",
        "count": success_count,
        "rate_limited": 0,
        "embedding": embeddings,
        "qdrant_status": qdrant_status
    }


@router.post("/embed-question", response_model=SearchResponse)
async def embed_query_and_search(data: QueryRequest):
    try:
        embedding = await get_embedding_async(data.query)
        search_results = await query_qdrant(embedding, top_k=5)
        return SearchResponse(embedding=embedding, results=search_results["results"])
    except Exception as e:
        logger.error(f"Error in embed-question: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
