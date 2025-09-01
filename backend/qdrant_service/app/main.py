import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.settings import settings
from .api.endpoints import router
from .db.qdrant_client import init_collection

app = FastAPI(title=settings.PROJECT_NAME)

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
app.include_router(router, prefix="/qdrant")


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.on_event("startup")
async def startup_event():
    init_collection()
