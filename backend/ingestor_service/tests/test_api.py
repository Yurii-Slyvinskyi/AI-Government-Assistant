from unittest.mock import patch
from ..app.api import endpoints


def test_start_ingestion_endpoint(client):
    with patch.object(endpoints, "schedule_ingest_tasks") as mock_schedule:
        response = client.post("/ingest/start/")
        assert response.status_code == 200
        assert response.json() == {"message": "Tasks Started"}
        mock_schedule.assert_called_once()
