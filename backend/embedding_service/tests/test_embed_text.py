from unittest.mock import patch, AsyncMock
from fastapi import status
from httpx import AsyncClient, ASGITransport
import pytest
from ..app.main import app
from ..app.api import endpoints


@pytest.mark.asyncio
async def test_embed_text_success():
    mock_embedding = [0.1, 0.2, 0.3]
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async",
                          new_callable=AsyncMock, return_value=mock_embedding) as mock_embed, \
                patch.object(endpoints, "send_vectors_to_qdrant",
                             new_callable=AsyncMock, return_value={"status": "ok"}) as mock_qdrant:
            response = await client.post(
                "/embed-text",
                json={"url": "http://example.com", "chunks": ["chunk1", "chunk2"]}
            )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 2
    assert data["embedding"] == [mock_embedding, mock_embedding]
    assert data["qdrant_status"] == "ok"
    assert data["rate_limited"] == 0


@pytest.mark.asyncio
async def test_embed_text_rate_limit():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async", new=AsyncMock(side_effect=Exception("RateLimitError"))), \
                patch.object(endpoints, "send_vectors_to_qdrant", new=AsyncMock(return_value={"status": "ok"})):
            response = await client.post(
                "/embed-text",
                json={"url": "http://example.com", "chunks": ["onlychunk"]}
            )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Embedding error" in response.json()["detail"]
