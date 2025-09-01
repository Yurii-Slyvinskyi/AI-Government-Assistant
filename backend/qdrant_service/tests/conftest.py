import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_qdrant_client():
    with patch("backend.qdrant_service.app.db.qdrant_client.client") as mock_client:
        mock_client.get_collections.return_value = MagicMock(collections=[])
        mock_client.upsert.return_value = None
        yield mock_client
