from pydantic import BaseModel
from typing import List, Dict


class EmbeddingVector(BaseModel):
    id: str
    vector: List[float]
    payload: Dict[str, str]


class EmbeddingBatch(BaseModel):
    url: str
    embeddings: List[EmbeddingVector]


class SearchQuery(BaseModel):
    vector: List[float]
    top_k: int = 5


class SearchResult(BaseModel):
    id: str
    score: float
    payload: Dict[str, str]


class SearchResponse(BaseModel):
    results: List[SearchResult]
