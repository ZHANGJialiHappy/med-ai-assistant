from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    age: Optional[int] = None
    gender: Optional[str] = None
    indicators: Optional[dict] = None
    top_k: int = 3