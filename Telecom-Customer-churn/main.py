from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Telecom Churn Prediction API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_PATH = "models/best_gradient_boosting_model.pkl"
SCALER_PATH = "models/scaler.pkl"
COLUMNS_PATH = "models/feature_columns.pkl"

if not all(os.path.exists(p) for p in [MODEL_PATH, SCALER_PATH, COLUMNS_PATH]):
    raise RuntimeError("Model files not found. Run prepare_api_assets.py first.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_columns = joblib.load(COLUMNS_PATH)

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.get("/")
def read_root():
    return {"message": "Telecom Churn Prediction API is running"}

@app.post("/predict")
def predict(data: CustomerData):
    try:
        
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])
        
       
        input_df['SeniorCitizen'] = input_df['SeniorCitizen'].astype('object')
        
        
        input_df_encoded = pd.get_dummies(input_df)
        
        final_df = pd.DataFrame(0, index=[0], columns=feature_columns)
        
        for col in input_df_encoded.columns:
            if col in final_df.columns:
                final_df[col] = input_df_encoded[col]

        cat_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 
                    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
                    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
        
        for col in cat_cols:
            val = input_dict[col]
            dummy_name = f"{col}_{val}"
            if dummy_name in final_df.columns:
                final_df[dummy_name] = 1
        
       
        num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        final_df[num_cols] = scaler.transform(final_df[num_cols])
        
        
        prediction = model.predict(final_df)[0]
        probability = model.predict_proba(final_df)[0][1]
        
        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(float(probability), 4),
            "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.3 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
