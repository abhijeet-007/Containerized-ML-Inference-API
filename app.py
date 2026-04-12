import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="ML Inference API", version="1.0.0")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


class PredictRequest(BaseModel):
    features: List[float]  # 64 pixel values for digits dataset (8x8 image)


class PredictResponse(BaseModel):
    prediction: int
    confidence: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if len(request.features) != 64:
        raise HTTPException(status_code=422, detail="Expected 64 features (8x8 image).")
    
    features = np.array(request.features).reshape(1, -1)
    prediction = int(model.predict(features)[0])
    confidence = float(model.predict_proba(features).max())
    
    return PredictResponse(prediction=prediction, confidence=confidence)
