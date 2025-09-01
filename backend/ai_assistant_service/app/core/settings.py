from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, List


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Assistant Service"

    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    EMBEDDING_SERVICE_URL: str = Field("http://embedding_service:8000", env="EMBEDDING_SERVICE_URL")

    QDRANT_URL: str = Field("http://qdrant:6333", env="QDRANT_URL")
    QDRANT_API_KEY: Optional[str] = None

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
