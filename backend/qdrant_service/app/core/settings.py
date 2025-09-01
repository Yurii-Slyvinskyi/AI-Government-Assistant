from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Qdrant Service"

    OPENAI_API_KEY: Optional[SecretStr] = Field(None, env="OPENAI_API_KEY")

    QDRANT_HOST: Optional[str] = Field(None, env="QDRANT_HOST")
    QDRANT_PORT: Optional[int] = Field(None, env="QDRANT_PORT")
    QDRANT_URL: Optional[str] = Field(None, env="QDRANT_URL")

    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "info"

    ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
