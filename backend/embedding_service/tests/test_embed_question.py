import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from httpx import AsyncClient, ASGITransport

from ..app.main import app
from ..app.api import endpoints


@pytest.mark.asyncio
async def test_embed_question_success():
    mock_embedding = [0.1, 0.2, 0.3]
    mock_search_results = {
        "results": [
            {"id": "1", "score": 0.95, "payload": {"text": "result 1"}},
            {"id": "2", "score": 0.85, "payload": {"text": "result 2"}}
        ]
    }
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async",
                          new_callable=AsyncMock, return_value=mock_embedding) as mock_embed, \
                patch.object(endpoints, "query_qdrant",
                             new_callable=AsyncMock, return_value=mock_search_results) as mock_query:
            response = await client.post(
                "/embed-question",
                json={"query": "test question"}
            )

            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Response error: {response.text}")
            print(f"Mock embed called: {mock_embed.called}")
            print(f"Mock query called: {mock_query.called}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["embedding"] == mock_embedding
    assert data["results"] == mock_search_results["results"]
    assert len(data["results"]) == 2
    mock_embed.assert_called_once_with("test question")
    mock_query.assert_called_once_with(mock_embedding, top_k=5)


@pytest.mark.asyncio
async def test_embed_question_custom_top_k():
    mock_embedding = [0.1, 0.2, 0.3]
    mock_search_results = {
        "results": [
            {"id": 1, "score": 0.95, "payload": {"text": "result 1"}}
        ]
    }
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async",
                          new_callable=AsyncMock, return_value=mock_embedding), \
                patch.object(endpoints, "query_qdrant",
                             new_callable=AsyncMock, return_value=mock_search_results):
            response = await client.post(
                "/embed-question",
                json={"query": "test question", "top_k": 3}
            )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["embedding"] == mock_embedding
    assert len(data["results"]) == 1


@pytest.mark.asyncio
async def test_embed_question_embedding_error():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async",
                          new_callable=AsyncMock, side_effect=Exception("Embedding failed")), \
                patch.object(endpoints, "query_qdrant", new_callable=AsyncMock):
            response = await client.post(
                "/embed-question",
                json={"query": "test question"}
            )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error processing query" in response.json()["detail"]


@pytest.mark.asyncio
async def test_embed_question_qdrant_error():
    mock_embedding = [0.1, 0.2, 0.3]
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        with patch.object(endpoints, "get_embedding_async",
                          new_callable=AsyncMock, return_value=mock_embedding), \
                patch.object(endpoints, "query_qdrant",
                             new_callable=AsyncMock, side_effect=Exception("Qdrant error")):
            response = await client.post(
                "/embed-question",
                json={"query": "test question"}
            )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Error processing query" in response.json()["detail"]
