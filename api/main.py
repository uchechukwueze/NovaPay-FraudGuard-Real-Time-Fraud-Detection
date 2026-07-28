from fastapi import FastAPI
import joblib
import pandas as pd
from typing import Any

app = FastAPI(title="Real Time Fraud Detection API")

# Load the saved model and feature names
model = joblib.load("model/novapay_lightgb_pipeline.pkl")
feature_names = joblib.load("model/novapay_feature_names.pkl")


@app.get("/")
def home():
    return {
        "message": "Welcome to the NovaPay Fraud Detection API"
    }

@app.get("/health")
def health_check():
    return {
        "status": "API is running",
        "model_loaded": True
    }
     
@app.post("/predict")
def predict_fraud(transaction: dict[str, Any]):

    # Convert the transaction into a one-row table
    transaction_df = pd.DataFrame([transaction])

    # Encode categorical values
    transaction_df = pd.get_dummies(
        transaction_df,
        dtype=int
    )

    # Match the exact features used during training
    transaction_df = transaction_df.reindex(
        columns=feature_names,
        fill_value=0
    )

    # Make prediction
    prediction = model.predict(transaction_df)[0]
    probability = model.predict_proba(transaction_df)[0, 1]

    return {
        "prediction": "Fraud" if prediction == 1 else "Legitimate",
        "fraud_probability": round(float(probability), 4)}

