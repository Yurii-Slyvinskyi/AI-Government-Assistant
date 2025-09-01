import httpx
import logging
from fastapi import APIRouter, HTTPException
from httpx import HTTPStatusError

from ..models.models import QuestionRequest, AnswerResponse
from ..services.openai_service import get_answer_from_llm
from ..core.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/process-question", response_model=AnswerResponse)
async def process_question(request: QuestionRequest):
    try:
        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{settings.EMBEDDING_SERVICE_URL}/embed-question",
                json={"query": request.question},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            context_chunks = []
            for item in results:
                payload = item.get("payload", {})
                chunk_text = payload.get("chunk", "").strip()
                url = payload.get("url")

                if chunk_text:
                    if url:
                        context_chunks.append(f"{chunk_text}\nSource: {url}")
                    else:
                        context_chunks.append(chunk_text)

            if not context_chunks:
                raise HTTPException(status_code=404, detail="No relevant context found")

            logger.info(f"context_chunks: {context_chunks}")
            answer = await get_answer_from_llm(request.question, context_chunks)
            return AnswerResponse(answer=answer)

    except HTTPStatusError as e:
        logger.error(f"Embedding service error: {str(e)}")
        raise HTTPException(status_code=502, detail="Embedding service unavailable")

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
