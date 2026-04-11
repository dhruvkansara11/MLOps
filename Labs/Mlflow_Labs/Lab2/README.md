# Wine Quality Prediction Lab

This lab covers the full machine learning lifecycle for predicting wine quality using Python and MLflow — including data preprocessing, model training with hyperparameter tuning, model registration, batch inference, and real-time serving.

---

## Prerequisites

- Python 3.8+
- Required libraries installed (see `requirements.txt`)
- Datasets: `winequality-white.csv` and `winequality-red.csv` inside the `data/` folder

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Lab Steps Overview

| Step | Description |
|------|-------------|
| 1 | Import Data |
| 2 | Explore Data |
| 3 | Data Preprocessing |
| 4 | Data Visualization |
| 5 | Define High-Quality Wines |
| 6 | Exploratory Data Analysis (EDA) |
| 7 | Check for Missing Data |
| 8 | Data Splitting |
| 9 | Baseline Model — Random Forest |
| 10 | Feature Importance Analysis |
| 11 | Model Registration in MLflow |
| 12 | Transition Model to Production |
| 13 | Model Inference & Evaluation |
| 14 | ⭐ NEW: XGBoost with Hyperopt Hyperparameter Tuning |
| 15 | Update Best Model to Production |
| 16 | Batch Inference (Spark UDF) |
| 17 | Real-Time Inference (REST API) |

---

## New Feature: XGBoost + Hyperopt Hyperparameter Tuning

### What was added

An **XGBoost classifier** with **automated hyperparameter tuning using Hyperopt and SparkTrials** has been added as an advanced alternative to the baseline Random Forest model.

### Why XGBoost?

- Gradient boosting consistently outperforms random forests on tabular data
- Supports early stopping to avoid overfitting
- Native MLflow integration via `mlflow.xgboost.autolog()`

### Why Hyperopt?

Rather than manually picking hyperparameters, Hyperopt uses **Tree-structured Parzen Estimator (TPE)** — a Bayesian optimization algorithm — to intelligently search the hyperparameter space. **SparkTrials** enables parallel evaluation of up to 96 configurations simultaneously.

### Hyperparameters Tuned

| Parameter | Search Strategy | Description |
|-----------|----------------|-------------|
| `max_depth` | Integer uniform (4–100) | Tree depth |
| `learning_rate` | Log-uniform | Step size shrinkage |
| `reg_alpha` | Log-uniform | L1 regularization |
| `reg_lambda` | Log-uniform | L2 regularization |
| `min_child_weight` | Log-uniform | Minimum instance weight in a child |

### What's Logged in MLflow

- All hyperparameter configurations as **nested child runs** under a parent `xgboost_models` run
- AUC score per configuration
- The best trained XGBoost booster with input/output signature
- Params and metrics autologged via `mlflow.xgboost.autolog()`

### Model Promotion Flow

Once the best XGBoost run is found, it is registered as a new version of `wine_quality` in the MLflow Model Registry and promoted to **Production**, while the Random Forest baseline is archived:

```
Random Forest v1  →  Archived
XGBoost Best Run  →  Production 
```

---

## Comparing Models

After running both steps, compare all runs in the MLflow UI:

```bash
mlflow ui
```

Open `http://localhost:5000` in your browser to view and compare AUC scores across all runs side by side.

---

## Running the Notebook

```bash
jupyter notebook starter.ipynb
```

---

## Real-Time Serving

```bash
# Run in terminal after activating virtual environment
mlflow models serve --env-manager=local -m models:/wine_quality/production -h 0.0.0.0 -p 5001
```

Then send inference requests:

```python
import requests

url = 'http://localhost:5001/invocations'
response = requests.post(url, json={"dataframe_split": X_test.to_dict(orient='split')})
print(response.json())
```

---

## Project Structure

```
Lab2/
├── data/
│   ├── winequality-white.csv
│   └── winequality-red.csv
├── starter.ipynb                              # Main lab notebook
├── README.md                                  # This file
├── requirements.txt                           # Dependencies
└── Wine Quality Prediction Lab Documentation.pdf
```