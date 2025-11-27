from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    date: str
    time: str
    amount: float
    merchant_name: str
    merchant_category: str
    city: str
    state: str
    country: str
    channel: Optional[str] = None
