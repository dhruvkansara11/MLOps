from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Predicts whether a patient has heart disease using a Decision Tree model",
    version="1.0.0"
)

# -------------------------------
# Request Model (Heart Dataset)
# -------------------------------
class HeartData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int


class HeartResponse(BaseModel):
    has_heart_disease: bool


@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    return {"status": "healthy"}


@app.post("/predict", response_model=HeartResponse)
async def predict_heart(data: HeartData):
    try:
        features = [[
            data.age,
            data.sex,
            data.cp,
            data.trestbps,
            data.chol,
            data.fbs,
            data.restecg,
            data.thalach,
            data.exang,
            data.oldpeak,
            data.slope,
            data.ca,
            data.thal
        ]]

        prediction = predict_data(features)
        result = int(prediction[0])

        return HeartResponse(
            has_heart_disease=bool(result)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
