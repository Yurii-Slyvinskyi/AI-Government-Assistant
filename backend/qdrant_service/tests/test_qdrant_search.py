import pytest
from unittest.mock import patch
from fastapi import status
from httpx import AsyncClient, ASGITransport

from ..app.main import app
from ..app.models.models import SearchQuery


@pytest.mark.asyncio
async def test_search_vectors_success():
    transport = ASGITransport(app=app)

    search_query = SearchQuery(vector=[0.1, 0.2, 0.3], top_k=2)

    with patch("backend.qdrant_service.app.api.endpoints.search_similar_vectors") as mock_search:
        mock_search.return_value = [
            {"id": "1", "score": 0.95, "payload": {"text": "test payload 1"}},
            {"id": "2", "score": 0.90, "payload": {"text": "test payload 2"}},
        ]

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/search", json=search_query.dict())

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["id"] == "1"
    assert data["results"][0]["score"] == 0.95
    assert data["results"][0]["payload"] == {"text": "test payload 1"}
    mock_search.assert_called_once_with(search_query.vector, top_k=search_query.top_k)


@pytest.mark.asyncio
async def test_search_vectors_qdrant_error():
    transport = ASGITransport(app=app)

    search_query = SearchQuery(vector=[0.1, 0.2, 0.3], top_k=5)

    with patch("backend.qdrant_service.app.api.endpoints.search_similar_vectors") as mock_search:
        mock_search.side_effect = Exception("Search failed")

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/search", json=search_query.dict())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Search failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_search_vectors_empty_results():
    transport = ASGITransport(app=app)

    search_query = SearchQuery(vector=[0.1, 0.2, 0.3], top_k=5)

    with patch("backend.qdrant_service.app.api.endpoints.search_similar_vectors") as mock_search:
        mock_search.return_value = []

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/search", json=search_query.dict())

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["results"] == []


@pytest.mark.asyncio
async def test_search_vectors_default_top_k():
    transport = ASGITransport(app=app)

    search_query = SearchQuery(vector=[0.1, 0.2, 0.3])

    with patch("backend.qdrant_service.app.api.endpoints.search_similar_vectors") as mock_search:
        mock_search.return_value = [
            {"id": "1", "score": 0.95, "payload": {"text": "payload 1"}},
        ]

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/search", json=search_query.dict())

    assert response.status_code == status.HTTP_200_OK
    mock_search.assert_called_once_with(search_query.vector, top_k=5)


@pytest.mark.asyncio
async def test_search_vectors_custom_top_k():
    transport = ASGITransport(app=app)

    search_query = SearchQuery(vector=[0.1, 0.2, 0.3], top_k=10)

    with patch("backend.qdrant_service.app.api.endpoints.search_similar_vectors") as mock_search:
        mock_search.return_value = [
            {"id": "1", "score": 0.95, "payload": {"text": "payload 1"}},
        ]

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/search", json=search_query.dict())

    assert response.status_code == status.HTTP_200_OK
    mock_search.assert_called_once_with(search_query.vector, top_k=10)
