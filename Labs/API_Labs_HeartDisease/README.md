# FastAPI ML Lab – Modified Implementation

## Overview
This project is a modified version of the original FastAPI ML lab.  
The goal of the lab is to demonstrate how a machine learning model can be trained and exposed as a REST API using **FastAPI** and **uvicorn**.

In this implementation, the **dataset, machine learning model, input features, and API response format** have been changed to make the solution original while preserving the core workflow of the lab.

---

## Summary of Modifications

| Component | Original Lab | Updated Version |
|---------|-------------|----------------|
| Dataset | Iris Dataset | Heart Disease Dataset (Kaggle – UCI) |
| ML Task | Multi-class classification | Binary classification |
| Model | Decision Tree Classifier | Random Forest Classifier |
| Input Features | 4 flower attributes | 13 clinical health attributes |
| Output | Numeric class label | Boolean prediction |
| API Response | Generic response | Domain-specific response |

---

## Dataset

### Updated Dataset
- **Source:** Kaggle – Heart Disease (UCI)
- **Problem Type:** Binary classification
- **Target column:** `target`
  - `0` → No heart disease
  - `1` → Presence of heart disease

### Features Used
The model is trained using the following 13 numerical features:

- `age`
- `sex`
- `cp` (chest pain type)
- `trestbps` (resting blood pressure)
- `chol` (serum cholesterol)
- `fbs` (fasting blood sugar)
- `restecg` (resting ECG results)
- `thalach` (maximum heart rate achieved)
- `exang` (exercise-induced angina)
- `oldpeak` (ST depression)
- `slope` (slope of peak exercise ST segment)
- `ca` (number of major vessels)
- `thal` (thalassemia)

---

## Model

### Original Model
- Decision Tree Classifier
- Simple baseline model

### Updated Model
- **Random Forest Classifier**
- Ensemble-based model using multiple decision trees
- Provides better generalization and robustness
- Commonly used for medical classification tasks

**Saved model file:**
