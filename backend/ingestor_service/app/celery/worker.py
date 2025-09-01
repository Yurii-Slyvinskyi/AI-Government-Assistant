from celery import Celery
import os

celery = Celery(
    "ingestor",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
    include=['app.celery.tasks']
)

celery.conf.update(
    task_routes={
        "app.celery.tasks.ingest_url_task": {"queue": "ingest"},
    }
)