import pytest
from fastapi.testclient import TestClient
from sklearn.datasets import load_digits
from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid():
    digits = load_digits()
    sample = digits.data[0].tolist()  # known digit: 0
    response = client.post("/predict", json={"features": sample})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert 0 <= data["prediction"] <= 9
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_wrong_feature_count():
    response = client.post("/predict", json={"features": [0.0] * 10})
    assert response.status_code == 422
