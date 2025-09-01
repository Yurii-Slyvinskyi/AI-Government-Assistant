from ..parser.fetcher import fetch_url
from ..parser.extractor import extract_content
from ..parser.normalizer import normalize_text
from ..services.text_processing import split_text
from ..services.send_chanks import send_chunks_to_embedding
from .worker import celery


@celery.task(name='app.celery.tasks.ingest_url_task')
def ingest_url_task(url: str):
    html = fetch_url(url)
    raw_text = extract_content(html)
    clean_text = normalize_text(raw_text)
    chunks = split_text(clean_text)

    import asyncio
    asyncio.run(send_chunks_to_embedding(url, chunks))
