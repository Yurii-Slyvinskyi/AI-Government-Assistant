import pytest
from unittest.mock import patch
from fastapi import status
from httpx import AsyncClient, ASGITransport

from ..app.main import app
from ..app.models.models import EmbeddingBatch, EmbeddingVector


@pytest.mark.asyncio
async def test_upsert_vectors_success():
    transport = ASGITransport(app=app)

    test_batch = EmbeddingBatch(
        url="http://example.com",
        embeddings=[
            EmbeddingVector(
                id="1",
                vector=[0.1, 0.2, 0.3],
                payload={"text": "test chunk 1"}
            ),
            EmbeddingVector(
                id="2",
                vector=[0.4, 0.5, 0.6],
                payload={"text": "test chunk 2"}
            )
        ]
    )

    with patch("backend.qdrant_service.app.api.endpoints.upsert_embeddings") as mock_upsert:
        mock_upsert.return_value = None

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post(
                "/qdrant/vectors",
                json=test_batch.dict()
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Saved 2 embeddings for http://example.com"
        mock_upsert.assert_called_once_with(test_batch)


@pytest.mark.asyncio
async def test_upsert_vectors_empty_batch(mock_qdrant_client):
    transport = ASGITransport(app=app)

    test_batch = EmbeddingBatch(
        url="http://example.com",
        embeddings=[]
    )

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/qdrant/vectors",
            json=test_batch.dict()
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Saved 0 embeddings for http://example.com"
    mock_qdrant_client.upsert.assert_not_called()


@pytest.mark.asyncio
async def test_upsert_vectors_qdrant_error():
    transport = ASGITransport(app=app)

    test_batch = EmbeddingBatch(
        url="http://example.com",
        embeddings=[
            EmbeddingVector(
                id="1",
                vector=[0.1, 0.2, 0.3],
                payload={"text": "test chunk"}
            )
        ]
    )

    with patch("backend.qdrant_service.app.api.endpoints.upsert_embeddings") as mock_upsert:
        mock_upsert.side_effect = Exception("Qdrant connection failed")

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/qdrant/vectors", json=test_batch.dict())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Qdrant connection failed" in response.json()["detail"]
