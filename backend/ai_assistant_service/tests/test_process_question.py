import pytest
from unittest.mock import patch, AsyncMock
from fastapi import status
from httpx import AsyncClient, ASGITransport
from types import SimpleNamespace

from ..app.main import app
from ..app.models.models import QuestionRequest
from ..app.api import endpoints


@pytest.mark.asyncio
async def test_process_question_success():
    transport = ASGITransport(app=app)
    question = QuestionRequest(question="What is a charitable organization?")

    mock_embedding_response = {
        "results": [
            {"id": "1", "score": 0.95,
             "payload": {"chunk": "A charitable organization is...", "url": "http://example.com"}}
        ]
    }

    with patch("httpx.AsyncClient") as mock_client_cls, \
            patch.object(endpoints, "get_answer_from_llm", new_callable=AsyncMock) as mock_llm:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value.post.return_value = SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: mock_embedding_response
        )
        mock_client_cls.return_value = mock_client

        mock_llm.return_value = "A charitable organization is a nonprofit..."

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/api/process-question", json=question.dict())

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "answer" in data
    assert data["answer"].startswith("A charitable organization")
    mock_client.__aenter__.return_value.post.assert_called_once()
    mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_process_question_no_context():
    transport = ASGITransport(app=app)
    question = QuestionRequest(question="Unrelated question?")

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value.post.return_value = SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: {"results": []}
        )
        mock_client_cls.return_value = mock_client

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/api/process-question", json=question.dict())

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No relevant context found"
    mock_client.__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_process_question_embedding_service_error():
    transport = ASGITransport(app=app)
    question = QuestionRequest(question="Test question")

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()

        def raise_error():
            from httpx import HTTPStatusError
            raise HTTPStatusError("Bad request", request=None, response=None)

        mock_client.__aenter__.return_value.post.return_value = SimpleNamespace(
            status_code=400,
            raise_for_status=raise_error,
            json=lambda: {}
        )
        mock_client_cls.return_value = mock_client

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/api/process-question", json=question.dict())

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.json()["detail"] == "Embedding service unavailable"
    mock_client.__aenter__.return_value.post.assert_called_once()


@pytest.mark.asyncio
async def test_process_question_llm_error():
    transport = ASGITransport(app=app)
    question = QuestionRequest(question="Test question")

    mock_embedding_response = {
        "results": [
            {"id": "1", "score": 0.95, "payload": {"chunk": "Some context", "url": None}}
        ]
    }

    with patch("httpx.AsyncClient") as mock_client_cls, \
            patch.object(endpoints, "get_answer_from_llm", new_callable=AsyncMock) as mock_llm:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value.post.return_value = SimpleNamespace(
            status_code=200,
            raise_for_status=lambda: None,
            json=lambda: mock_embedding_response
        )
        mock_client_cls.return_value = mock_client

        mock_llm.side_effect = Exception("LLM failed")

        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.post("/api/process-question", json=question.dict())

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json()["detail"] == "Internal server error"
    mock_client.__aenter__.return_value.post.assert_called_once()
    mock_llm.assert_called_once()
