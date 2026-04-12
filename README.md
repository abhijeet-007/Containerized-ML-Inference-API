# Containerized ML Inference API

A Dockerized FastAPI app serving a scikit-learn digit classifier (0–9), with GitHub Actions CI that runs tests, builds, and pushes to Docker Hub.

## Project Structure

```
├── app.py               # FastAPI app
├── train_model.py       # Train & save model.pkl
├── test_app.py          # Unit tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Quick Start

### 1. Train the model
```bash
pip install -r requirements.txt
python train_model.py
```

### 2. Run locally
```bash
uvicorn app:app --reload
```

### 3. Run with Docker
```bash
docker compose up --build
```

API is available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint   | Description          |
|--------|------------|----------------------|
| GET    | /health    | Health check         |
| POST   | /predict   | Run inference        |

### Example Request
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0,0,5,13,9,1,0,0,0,0,13,15,10,15,5,0,0,3,15,2,0,11,8,0,0,4,12,0,0,8,8,0,0,5,8,0,0,9,8,0,0,4,11,0,1,12,7,0,0,2,14,5,10,12,0,0,0,0,6,13,10,0,0,0]}'
```

### Example Response
```json
{"prediction": 0, "confidence": 0.98}
```

## CI/CD (GitHub Actions)

The pipeline on every push to `main`:
1. Installs dependencies & trains the model
2. Runs `pytest`
3. Builds the Docker image and pushes to Docker Hub

### Required GitHub Secrets

| Secret               | Description                  |
|----------------------|------------------------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username     |
| `DOCKERHUB_TOKEN`    | Docker Hub access token      |

Go to **GitHub → Settings → Secrets and variables → Actions** to add them.

## Deploy to a VPS

```bash
docker pull <your-dockerhub-username>/ml-inference-api:latest
docker run -d -p 8000:8000 <your-dockerhub-username>/ml-inference-api:latest
```
