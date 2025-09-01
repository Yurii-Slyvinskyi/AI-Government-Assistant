from pydantic import BaseModel
from typing import List, Dict


class QuestionRequest(BaseModel):
    question: str


class SearchResult(BaseModel):
    id: str
    score: float
    payload: Dict[str, str]


class Response(BaseModel):
    embedding: List[float]
    results: List[dict]


class AnswerResponse(BaseModel):
    answer: str
