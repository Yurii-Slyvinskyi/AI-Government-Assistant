import asyncio
import openai
import logging
from ..core.settings import settings

openai.api_key = settings.OPENAI_API_KEY
semaphore = asyncio.Semaphore(2)
client = openai.AsyncOpenAI()
logger = logging.getLogger(__name__)


async def get_embedding_async(text: str) -> list[float]:
    async with semaphore:
        await asyncio.sleep(0.5)
        response = await client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        logger.info(f"Full embedding response: {response}")
        return response.data[0].embedding
