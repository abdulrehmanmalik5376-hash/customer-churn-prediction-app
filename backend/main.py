from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io

from schemas import Customer
from utils import model, scaler, FEATURE_COLUMNS

app = FastAPI(
    title="Customer Churn Prediction API",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API Running Successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }


@app.get("/model-info")
def model_info():
    return {
        "Model": "Random Forest",
        "Version": "1.0",
        "Features": len(FEATURE_COLUMNS)
    }


@app.post("/predict")
def predict(customer: Customer):

    try:

        data = customer.model_dump()

        df = pd.DataFrame([data])

        # Rename API fields to Training fields
        df.columns = FEATURE_COLUMNS

        # Scale
        scaled = scaler.transform(df)

        # Prediction
        prediction = model.predict(scaled)[0]

        probability = float(model.predict_proba(scaled)[0][1])

        if probability < 0.30:
            risk = "Low"

        elif probability < 0.70:
            risk = "Medium"

        else:
            risk = "High"

        return {

            "Prediction": int(prediction),

            "Probability": round(probability,3),

            "Risk_Level": risk

        }

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={"error":str(e)}

        )


@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        df = pd.read_csv(io.BytesIO(contents))

        # Ensure same feature names
        df = df[FEATURE_COLUMNS]

        scaled = scaler.transform(df)

        prediction = model.predict(scaled)

        probability = model.predict_proba(scaled)[:,1]

        df["Prediction"] = prediction

        df["Probability"] = probability.round(3)

        return df.to_dict(orient="records")

    except Exception as e:

        return JSONResponse(

            status_code=500,

            content={"error":str(e)}

        )