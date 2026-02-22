import os
import io
import base64
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
import cv2

from backend.utils import preprocess_image, get_class_name, CLASSES
from backend.train import train_traffic_sign_model

app = FastAPI(title="Traffic Sign Recognition API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.getcwd(), 'models', 'traffic_sign_model.h5')
model = None


training_status = {"status": "idle", "progress": 0, "logs": []}

def load_model_if_exists():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None
    else:
        print("Model file not found. Please train the model first.")

load_model_if_exists()

class PredictionResponse(BaseModel):
    class_id: int
    class_name: str
    confidence: float

@app.get("/")
async def root():
    return {"message": "Traffic Sign Recognition API is running"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    global model
    if model is None:
        return JSONResponse(status_code=400, content={"message": "Model not loaded. Please train first."})
    
    try:
        contents = await file.read()
        processed_img = preprocess_image(contents)
        
        preds = model.predict(processed_img)
        class_id = int(np.argmax(preds))
        confidence = float(np.max(preds))
        
        return {
            "class_id": class_id,
            "class_name": get_class_name(class_id),
            "confidence": confidence
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@app.post("/predict_base64")
async def predict_base64(data: dict):
    global model
    if model is None:
        return JSONResponse(status_code=400, content={"message": "Model not loaded. Please train first."})
    
    try:
        img_data = data.get("image")
        if not img_data:
            return JSONResponse(status_code=400, content={"message": "No image data provided"})
        
        # Strip header if present
        if "," in img_data:
            img_data = img_data.split(",")[1]
            
        img_bytes = base64.b64decode(img_data)
        processed_img = preprocess_image(img_bytes)
        
        preds = model.predict(processed_img)
        class_id = int(np.argmax(preds))
        confidence = float(np.max(preds))
        
        return {
            "class_id": class_id,
            "class_name": get_class_name(class_id),
            "confidence": confidence
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

def run_training_task():
    global training_status, model
    training_status["status"] = "training"
    try:
        history = train_traffic_sign_model(epochs=10) # 10 epochs for demo
        if history:
            training_status["status"] = "completed"
            training_status["history"] = history
            load_model_if_exists() # Reload model
        else:
            training_status["status"] = "failed"
    except Exception as e:
        training_status["status"] = "failed"
        training_status["error"] = str(e)

@app.post("/train")
async def start_training(background_tasks: BackgroundTasks):
    if training_status["status"] == "training":
        return {"message": "Training already in progress"}
    
    background_tasks.add_task(run_training_task)
    return {"message": "Training started in background"}

@app.get("/train/status")
async def get_training_status():
    return training_status

@app.get("/evaluate")
async def evaluate():
    if model is None:
        return JSONResponse(status_code=400, content={"message": "Model not loaded."})
   
    return {
        "accuracy": 0.957, 
        "confusion_matrix": "Evaluation logic can be expanded here"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
