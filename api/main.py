# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
from feature_extractor import extract_features  # Import our new pipeline

app = FastAPI(title="PhishGuard API")

# Add CORS so the HTML frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


# New Schema: Expecting a URL string
class WebsiteScanRequest(BaseModel):
    url: str


MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_engine/phishing_nn_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")


@app.post("/predict")
async def predict_phishing(request: WebsiteScanRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required.")

    try:
        # 1. Pipeline phase: Text to Vector
        feature_vector = extract_features(request.url)

        # 2. Reshape for the Neural Network
        feature_array = np.array(feature_vector).reshape(1, -1)

        # 3. Model Prediction
        prediction = model.predict(feature_array)[0]
        confidence = np.max(model.predict_proba(feature_array))

        # Following the established schema
        final_verdict = "Legitimate" if prediction == 1 else "Phishing"

        return {
            "verdict": final_verdict,
            "confidenceScore": float(confidence)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))