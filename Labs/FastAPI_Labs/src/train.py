import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_model():

    df = pd.read_csv("/Users/dhruvkansara/Documents/NEU/Sem3/MLOPs/MLOps/Labs/API_Labs/FastAPI_Labs/src/heart.csv")

    X = df.drop("target", axis=1)
    y = df["target"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    os.makedirs("../model", exist_ok=True)
    with open("../model/heart_rf_model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_model()