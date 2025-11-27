from pydantic import BaseModel
from typing import List

class FraudResult(BaseModel):
    risk_level: str
    fraud_probability: float
    anomaly_score: float
    reasons: List[str]
