# backend/app/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict

class RoundData(BaseModel):
    index: int
    color: str          # e.g., "green", "red", "violet"
    number: int
    timestamp: Optional[str]

class PredictRequest(BaseModel):
    rounds: List[RoundData]
    total_bet: Optional[float] = None
    payout: Optional[float] = None

class PredictResponse(BaseModel):
    color: str
    number: int
    confidence: float
    total_bet: Optional[float]
    payout: Optional[float]

class TrainRequest(BaseModel):
    # data: list of dicts with history and label fields
    data: List[Dict]
