# MLMD Lab 1 — Enhanced: Tracking a Real Sklearn Pipeline with Lineage Visualization

## Overview

This lab extends the original MLMD Lab 1 walkthrough with two major features:

1. **Real sklearn model training** — instead of placeholder artifacts, we train an actual `RandomForestClassifier` on the Iris dataset and record every stage (ingestion → preprocessing → training/evaluation) in MLMD.
2. **Lineage tracking & visualization** — we build and render a full lineage DAG from the metadata store using `networkx` + `matplotlib`, and implement recursive lineage tracing from any artifact back to its origins.

## Repository Structure

```
MLMD_Labs/
└── Lab1/
    ├── README.md                         # You are here
    ├── mlmd_lab1_enhanced.py             # Main lab script
    └── artifacts/                        # Generated at runtime
        ├── iris_rf_model.joblib          # Trained model
        └── lineage_dag.png              # Lineage visualization
```

## Prerequisites

- Python 3.8+
- Required packages:

```bash
pip install ml-metadata scikit-learn matplotlib networkx joblib
```

## What You'll Learn

| Part | Topic | What Happens |
|------|-------|--------------|
| 1 | Setup | Install deps, initialize in-memory MLMD store |
| 2 | Type Registration | Define ArtifactTypes (RawDataset, TransformedDataset, Model, ModelMetrics) and ExecutionTypes (DataIngestion, Preprocessing, Training) |
| 3 | Data Ingestion | Load Iris dataset, register as RawDataset artifact |
| 4 | Preprocessing | Train/test split + StandardScaler, register TransformedDataset artifacts |
| 5 | Training & Eval | Train RandomForest, evaluate, register Model + ModelMetrics artifacts |
| 6 | Context | Group all artifacts and executions under an Experiment context |
| 7 | Querying | Answer questions like "which dataset trained this model?" |
| 8 | Lineage DAG | Build and visualize the full pipeline lineage graph |
| 9 | Lineage Tracing | Recursively trace any artifact back to its upstream origins |

## MLMD Data Model

```
ArtifactType ──> Artifact ──┐
                             ├──> Event ──> links artifacts to executions
ExecutionType ─> Execution ─┘

ContextType ──> Context ──┬──> Attribution (artifact ↔ context)
                          └──> Association (execution ↔ context)
```

## Pipeline Tracked in This Lab

```
┌─────────────┐     ┌────────────────┐     ┌───────────────┐
│   Iris Raw   │────>│ Preprocessing  │────>│   Training    │
│   Dataset    │     │ (split+scale)  │     │ (RandomForest)│
└─────────────┘     └───────┬────────┘     └──┬─────────┬──┘
                            │                  │         │
                     ┌──────┴──────┐     ┌─────┴──┐  ┌──┴───────┐
                     │ Train Split │     │ Model  │  │ Metrics  │
                     │ Test Split  │     │(.joblib│  │(acc, f1) │
                     └─────────────┘     └────────┘  └──────────┘
```

## Running the Lab

```bash
python mlmd_lab1_enhanced.py
```

## Sample Output

### Console Output
```
============================================================
MLMD Lab 1 (Enhanced) — Sklearn Pipeline with Lineage Tracking
============================================================

[Part 1] Metadata store initialized (in-memory).

[Part 2] Registered Artifact Types:
  - RawDataset (id=1)
  - TransformedDataset (id=2)
  - Model (id=3)
  - ModelMetrics (id=4)

Registered Execution Types:
  - DataIngestion (id=5)
  - Preprocessing (id=6)
  - Training (id=7)

[Part 3] Loaded Iris dataset: 150 samples, 4 features
  Data Ingestion complete. Raw dataset artifact ID: 1

[Part 4] Train set: 120 samples | Test set: 30 samples
  Preprocessing complete.

[Part 5] Accuracy: 0.9667 | F1 (weighted): 0.9665
  Model saved to artifacts/iris_rf_model.joblib

[Part 6] Experiment context: "iris-classification-exp-1"
  Linked 5 artifacts and 3 executions.
```

### Lineage Trace
```
Full lineage of the trained model:
============================================================
ROOT [Model] "Iris RandomForest v1" (id=5)
  <-- [TransformedDataset] "Iris Train (scaled)" (id=3)
    <-- [RawDataset] "Iris Dataset" (id=1)
  <-- [TransformedDataset] "Iris Test (scaled)" (id=4)
    <-- [RawDataset] "Iris Dataset" (id=1)
```

### Lineage DAG

The script generates `artifacts/lineage_dag.png` — a visual DAG showing all artifacts (blue squares) and executions (orange circles) connected by directional edges.

## Exercises for Students

1. **Add a second experiment** — train `SVC` or `LogisticRegression`, register everything, and compare experiments by querying the store.
2. **Persist with SQLite** — switch from `fake_database` to `sqlite.filename_uri` so metadata survives across runs.
3. **Add data validation** — integrate TFDV to generate statistics/schema and register those as additional artifacts.
4. **Extend visualization** — color-code nodes by artifact type in the lineage DAG.

## Key Differences from the Original Lab

| Original Lab 1 | This Enhanced Lab |
|---|---|
| Uses TFDV with Chicago Taxi data | Uses sklearn with Iris data |
| Registers placeholder artifacts | Trains a real model, records actual metrics |
| Single execution type (Data Validation) | Three execution types (Ingestion, Preprocessing, Training) |
| No visualization | Full lineage DAG visualization with networkx |
| Manual lineage queries only | Recursive lineage tracing function |
| No context grouping detail | Full Experiment context with attributions and associations |

## References

- [ML Metadata Documentation](https://www.tensorflow.org/tfx/guide/mlmd)
- [MLMD API Reference](https://www.tensorflow.org/tfx/ml_metadata/api_docs/python/mlmd/MetadataStore)
- [MLMD GitHub Repository](https://github.com/google/ml-metadata)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)