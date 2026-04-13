# Containerized ML Inference API

A FastAPI app that classifies handwritten digits (0–9) using a Random Forest model, served via Docker.

## Setup

```bash
pip install -r requirements.txt
python train_model.py
```

## Run

```bash
# Locally
uvicorn app:app --reload

# With Docker
docker compose up --build
```

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

## Endpoints

| Method | Endpoint  | Description   |
|--------|-----------|---------------|
| GET    | /health   | Health check  |
| POST   | /predict  | Run inference |

### Example

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0,0,5,13,9,1,0,0,...,0,0,6,13,10,0,0,0]}'
```

```json
{"prediction": 0, "confidence": 0.98}
```

> Input must be exactly 64 float values (8×8 image).

## CI/CD

- **CI** — runs tests, builds and pushes Docker image to Docker Hub
- **CD** — SSHs into AWS EC2, pulls the latest image and restarts the container

## Deploy to AWS EC2

```bash
docker pull <your-dockerhub-username>/ml-inference-api:latest
docker run -d --name ml-api -p 8000:8000 --restart unless-stopped \
  <your-dockerhub-username>/ml-inference-api:latest
```

### GitHub Secrets needed

| Secret               | Description                  |
|----------------------|------------------------------|
| `DOCKERHUB_USERNAME` | Docker Hub username          |
| `DOCKERHUB_TOKEN`    | Docker Hub access token      |
| `VPS_HOST`           | EC2 public IP or hostname    |
| `VPS_USER`           | SSH username                 |
| `VPS_SSH_KEY`        | Private SSH key              |
