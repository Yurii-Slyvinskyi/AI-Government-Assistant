from pydantic import BaseModel, Field
from typing import List, Dict, Union


class TextChunksRequest(BaseModel):
    url: str
    chunks: List[str]


class QueryRequest(BaseModel):
    query: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class StatusResponse(BaseModel):
    status: str
    count: int
    rate_limited: int = 0
    embedding: List[List[float]] = Field(default_factory=list)
    qdrant_status: str = "disabled"


class SearchResult(BaseModel):
    id: Union[str, int]
    score: float
    payload: Dict[str, str]


class SearchResponse(BaseModel):
    embedding: List[float]
    results: List[SearchResult]
