"""
Lab3 - Model Training Script with Logging
Trains a TensorFlow model on the Iris dataset and saves it.
Logs training progress and metrics to stdout (captured by Docker).
"""

import os
import json
import logging
from datetime import datetime

import tensorflow as tf
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# =============================================================================
# LOGGING (same JSON format as the API for consistent log parsing)
# =============================================================================
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
        return json.dumps(log_entry)


logger = logging.getLogger("model-trainer")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)


if __name__ == "__main__":
    logger.info("Starting model training")

    # Load data
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    logger.info("Dataset loaded", extra={
        "extra_data": {"samples": len(X), "features": X.shape[1]}
    })

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scale
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"),
        tf.keras.layers.Dense(3, activation="softmax"),
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    # Train
    logger.info("Training started", extra={
        "extra_data": {"epochs": 50, "train_samples": len(X_train)}
    })
    history = model.fit(
        X_train, y_train,
        epochs=50,
        validation_data=(X_test, y_test),
        verbose=1,
    )

    # Log final metrics
    final_acc = history.history["accuracy"][-1]
    final_val_acc = history.history["val_accuracy"][-1]
    final_loss = history.history["loss"][-1]
    logger.info("Training complete", extra={
        "extra_data": {
            "final_accuracy": round(final_acc, 4),
            "final_val_accuracy": round(final_val_acc, 4),
            "final_loss": round(final_loss, 4),
        }
    })

    # Save
    model_path = "my_model.keras"
    model.save(model_path)
    logger.info("Model saved", extra={
        "extra_data": {"path": model_path}
    })