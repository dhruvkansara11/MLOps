# Docker Lab 3 — Production-Ready ML Deployment with Health Checks & Logging

## Overview

This lab builds on Lab1 (basic Docker) and Lab2 (Docker Compose + Flask API) by adding **production-grade features** that every deployed ML service needs:

1. **Health Checks** — Liveness (`/health`) and readiness (`/ready`) endpoints so Docker (and Kubernetes) know when your container is alive and ready to serve traffic
2. **Structured JSON Logging** — Every request, prediction, and error is logged in machine-parseable JSON format (console + file)
3. **Metrics Endpoint** — Simple `/metrics` endpoint tracking uptime, request count, and errors
4. **Non-root User** — Container runs as `appuser` instead of root for security
5. **Log Persistence** — Application logs survive container restarts via Docker named volumes
6. **Restart Policy** — Container auto-restarts on failure
7. **Docker Log Rotation** — Prevents logs from filling up disk

## Project Structure

```
Lab3/
├── README.md
├── dockerfile                  # Multi-stage: train → serve (with HEALTHCHECK)
├── docker-compose.yml          # Two services + health checks + log config
├── requirements.txt
└── src/
    ├── main.py                 # Flask API with /health, /ready, /metrics
    ├── model_training.py       # TF model training with JSON logging
    ├── templates/
    │   └── predict.html        # Web UI for predictions
    └── statics/
        ├── setosa.jpg
        ├── versicolor.jpg
        └── virginica.jpg
```

## Prerequisites

- Docker Desktop installed and running
- Basic understanding of Lab1 and Lab2

## Quick Start

### Option A: Docker Compose (recommended)

```bash
cd Lab3
docker compose up --build
```

Wait for training to finish, then:
- **Web UI**: http://localhost:4000/predict
- **Health check**: http://localhost:4000/health
- **Readiness**: http://localhost:4000/ready
- **Metrics**: http://localhost:4000/metrics

### Option B: Multi-stage Dockerfile

```bash
cd Lab3
docker build -t lab3:v1 .
docker run -p 4000:4000 lab3:v1
```

## What's New in Lab3 (vs Lab2)

| Feature | Lab2 | Lab3 |
|---------|------|------|
| Health checks | None | `/health` + `/ready` + Docker HEALTHCHECK |
| Logging | print() | Structured JSON (console + file) |
| Metrics | None | `/metrics` endpoint |
| Security | Runs as root | Runs as non-root `appuser` |
| Log persistence | None | Named volume `app_logs` |
| Restart policy | None | `unless-stopped` |
| Docker log rotation | None | `json-file` driver, max 10MB × 5 files |
| Config | Hardcoded | Environment variables |

## Health Check Endpoints

### `GET /health` — Liveness Probe

Returns 200 if the Flask process is running. Docker uses this to detect crashed containers.

```bash
curl http://localhost:4000/health
```
```json
{"status": "healthy", "uptime_seconds": 142.5}
```

### `GET /ready` — Readiness Probe

Returns 200 only if the model is loaded. Returns 503 if the model failed to load.

```bash
curl http://localhost:4000/ready
```
```json
{"status": "ready", "model_loaded": true, "total_requests": 15}
```

### `GET /metrics` — Application Metrics

```bash
curl http://localhost:4000/metrics
```
```json
{
  "uptime_seconds": 300.2,
  "total_requests": 42,
  "total_errors": 1,
  "model_loaded": true
}
```

## Structured Logging

Every log entry is a JSON object for easy parsing by ELK, Datadog, CloudWatch, etc:

```json
{"timestamp": "2026-03-14T10:30:45.123Z", "level": "INFO", "logger": "iris-api", "message": "Prediction made", "input": {"sepal_length": 5.1}, "predicted_class": "Setosa", "confidence": 0.9734}
```

### View logs

```bash
# Docker Compose logs (live)
docker compose logs -f serving

# Application log file (inside container)
docker exec ml_serving_lab3 cat /app/logs/app.log

# Persisted logs (even after container stops)
docker volume inspect lab3_app_logs
```

## Monitoring Container Health

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' ml_serving_lab3

# Watch health check history
docker inspect --format='{{json .State.Health}}' ml_serving_lab3 | python -m json.tool
```

Possible states: `starting` → `healthy` → `unhealthy`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 4000 | Flask server port |
| `LOG_LEVEL` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | /app/logs/app.log | Log file path |
| `MODEL_PATH` | my_model.keras | Path to saved model |
| `FLASK_DEBUG` | false | Enable Flask debug mode |

Override in docker-compose.yml or at runtime:

```bash
docker run -e LOG_LEVEL=DEBUG -e PORT=5000 -p 5000:5000 lab3:v1
```

## Cleanup

```bash
# Stop and remove containers
docker compose down

# Also remove volumes (logs + model)
docker compose down -v

# Remove the image
docker rmi lab3:v1
```

## Key Takeaways

1. **Health checks** tell Docker/Kubernetes whether your container is alive and ready — without them, broken containers keep receiving traffic
2. **Structured logging** (JSON) makes logs searchable and parseable by monitoring tools — never use `print()` in production
3. **Non-root users** reduce the blast radius if your container is compromised
4. **Named volumes** persist important data (logs, models) across container restarts
5. **Restart policies** make your service self-healing — it comes back automatically after crashes
6. **Log rotation** prevents a single chatty container from filling up your disk

## References

- [Docker HEALTHCHECK docs](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [Docker Compose healthcheck](https://docs.docker.com/compose/compose-file/05-services/#healthcheck)
- [12-Factor App: Logs](https://12factor.net/logs)
- [Flask Logging](https://flask.palletsprojects.com/en/3.0.x/logging/)