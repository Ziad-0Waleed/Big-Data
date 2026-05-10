from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="PhishGuard API")



class WebsiteFeatures(BaseModel):
    features: list[int]



MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_engine/phishing_nn_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}. Did you run train.py first?")


@app.post("/predict")
async def predict_phishing(data: WebsiteFeatures):
    if len(data.features) != 30:
        raise HTTPException(status_code=400, detail="Exactly 30 feature values are required.")

    try:

        feature_array = np.array(data.features).reshape(1, -1)


        prediction = model.predict(feature_array)[0]
        confidence = np.max(model.predict_proba(feature_array))


        final_verdict = "Legitimate" if prediction == 1 else "Phishing"

        return {
            "verdict": final_verdict,
            "confidenceScore": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))