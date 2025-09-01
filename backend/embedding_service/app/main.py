import openai
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import settings
from .api.endpoints import router

# FastAPI
app = FastAPI(title="Embedding Service")

# OpenAI
openai.api_key = settings.OPENAI_API_KEY

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routing
app.include_router(router)


@app.get("/ping")
async def ping():
    return {"message": "pong"}
