from fastapi import APIRouter
from http.client import HTTPException
from ..celery.tasks import ingest_url_task
from ..parser.website_urls import URLS

router = APIRouter()


# Task
def schedule_ingest_tasks():
    for url in URLS:
        ingest_url_task.delay(url)


@router.post("/start/")
async def start_ingestion():
    try:
        schedule_ingest_tasks()
        return {"message": "Tasks Started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
