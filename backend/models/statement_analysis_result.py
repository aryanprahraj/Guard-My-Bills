from pydantic import BaseModel
from typing import List, Dict, Any

class StatementAnalysisResult(BaseModel):
    summary: Dict[str, Any]
    transactions: List[Dict[str, Any]]
