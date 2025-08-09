# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.model import Predictor
from app.schemas import RoundData, PredictRequest, PredictResponse, TrainRequest
import os

app = FastAPI(title="Blue Guyss Prediction API")

MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
predictor = Predictor(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    """
    Expects scraped recent rounds and optional stats.
    The app should collect the recent rounds (color, number, timestamp)
    and send them in the `rounds` field. optional fields: total_bet, payout
    """
    try:
        rounds = payload.rounds
        extra = {"total_bet": payload.total_bet, "payout": payload.payout}
        pred, conf = predictor.predict_next(rounds, extra)
        return {"color": pred["color"], "number": pred["number"], "confidence": conf, "total_bet": payload.total_bet, "payout": payload.payout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
def train(req: TrainRequest):
    """
    Accept training data in CSV-like JSON (or upload file in a later version).
    This endpoint triggers retraining with the provided dataset.
    """
    try:
        predictor.train_from_json(req.data)
        return {"status": "trained"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
