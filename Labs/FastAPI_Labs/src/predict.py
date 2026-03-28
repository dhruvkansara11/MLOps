import pickle

with open("../model/heart_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_data(features):
    return model.predict(features)
