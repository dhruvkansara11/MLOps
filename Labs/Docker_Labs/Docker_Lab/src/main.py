"""
Lab3 - Production-Ready Flask API with Health Checks & Logging
Serves Iris classification predictions with structured logging,
health/readiness endpoints, and request tracking.
"""

import os
import time
import logging
import json
from datetime import datetime

from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np

# =============================================================================
# LOGGING SETUP — Structured JSON logging for production
# =============================================================================
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.environ.get("LOG_FILE", "/app/logs/app.log")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging():
    """Configure root logger with console + file handlers."""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    json_fmt = JSONFormatter()

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(json_fmt)
    logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(json_fmt)
    logger.addHandler(file_handler)

    return logging.getLogger("iris-api")


logger = setup_logging()

# =============================================================================
# APP SETUP
# =============================================================================
app = Flask(__name__, static_folder="statics")

# Track app state for health checks
app_state = {
    "model_loaded": False,
    "start_time": time.time(),
    "request_count": 0,
    "error_count": 0,
}

# Load model
MODEL_PATH = os.environ.get("MODEL_PATH", "my_model.keras")
class_labels = ["Setosa", "Versicolor", "Virginica"]

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    app_state["model_loaded"] = True
    logger.info("Model loaded successfully", extra={
        "extra_data": {"model_path": MODEL_PATH}
    })
except Exception as e:
    model = None
    logger.error("Failed to load model", extra={
        "extra_data": {"model_path": MODEL_PATH, "error": str(e)}
    })


# =============================================================================
# MIDDLEWARE — Request logging
# =============================================================================
@app.before_request
def log_request_start():
    """Log every incoming request."""
    request._start_time = time.time()
    app_state["request_count"] += 1


@app.after_request
def log_request_end(response):
    """Log response status and latency."""
    latency_ms = (time.time() - getattr(request, "_start_time", time.time())) * 1000
    logger.info("Request completed", extra={
        "extra_data": {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "latency_ms": round(latency_ms, 2),
        }
    })
    return response


# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================
@app.route("/health", methods=["GET"])
def health():
    """
    Liveness probe — is the container alive?
    Returns 200 if the Flask process is running.
    Used by Docker HEALTHCHECK and orchestrators.
    """
    return jsonify({
        "status": "healthy",
        "uptime_seconds": round(time.time() - app_state["start_time"], 1),
    }), 200


@app.route("/ready", methods=["GET"])
def ready():
    """
    Readiness probe — is the app ready to serve traffic?
    Returns 200 only if the model is loaded successfully.
    Returns 503 if the model failed to load.
    """
    if app_state["model_loaded"]:
        return jsonify({
            "status": "ready",
            "model_loaded": True,
            "total_requests": app_state["request_count"],
        }), 200
    else:
        return jsonify({
            "status": "not_ready",
            "model_loaded": False,
            "reason": "Model failed to load",
        }), 503


@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Simple metrics endpoint for monitoring.
    In production, you'd use Prometheus format.
    """
    return jsonify({
        "uptime_seconds": round(time.time() - app_state["start_time"], 1),
        "total_requests": app_state["request_count"],
        "total_errors": app_state["error_count"],
        "model_loaded": app_state["model_loaded"],
    }), 200


# =============================================================================
# PREDICTION ENDPOINTS
# =============================================================================
@app.route("/")
def home():
    return "Welcome to the Iris Classifier API! (Lab3 - Production Ready)"


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    if not app_state["model_loaded"]:
        app_state["error_count"] += 1
        logger.error("Prediction attempted but model not loaded")
        return jsonify({"error": "Model not loaded"}), 503

    try:
        data = request.form
        features = {
            "sepal_length": float(data["sepal_length"]),
            "sepal_width": float(data["sepal_width"]),
            "petal_length": float(data["petal_length"]),
            "petal_width": float(data["petal_width"]),
        }

        input_data = np.array(list(features.values()))[np.newaxis, :]
        prediction = model.predict(input_data, verbose=0)
        predicted_class = class_labels[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        logger.info("Prediction made", extra={
            "extra_data": {
                "input": features,
                "predicted_class": predicted_class,
                "confidence": round(confidence, 4),
            }
        })

        return jsonify({
            "predicted_class": predicted_class,
            "confidence": round(confidence, 4),
        })

    except Exception as e:
        app_state["error_count"] += 1
        logger.error("Prediction failed", extra={
            "extra_data": {"error": str(e)}
        })
        return jsonify({"error": str(e)}), 400


# =============================================================================
# ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    logger.info("Starting Iris API server", extra={
        "extra_data": {"port": port, "debug": debug, "log_level": LOG_LEVEL}
    })
    app.run(debug=debug, host="0.0.0.0", port=port)