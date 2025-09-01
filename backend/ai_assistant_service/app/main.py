import openai
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.endpoints import router
from .core.settings import settings

# FastAPI
app = FastAPI(title=settings.PROJECT_NAME)

# OpenAI
openai.api_key = settings.OPENAI_API_KEY

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=settings.LOG_LEVEL.upper())
logger = logging.getLogger(__name__)

# Routing
app.include_router(router, prefix="/api")


@app.get("/ping")
async def ping():
    return {"message": "pong"}
