from unittest.mock import patch
from ..app.parser.website_urls import URLS
from ..app.api.endpoints import schedule_ingest_tasks
from ..app.celery import tasks


def test_schedule_ingest_tasks_calls_celery():
    with patch.object(tasks.ingest_url_task, "delay") as mock_delay:
        schedule_ingest_tasks()
        assert mock_delay.call_count == len(URLS)