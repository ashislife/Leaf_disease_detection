from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from PIL import Image
import numpy as np
import tensorflow as tf
import uvicorn
from typing import Dict, Any
import io
import json
import os

# Model configuration
MODEL_PATH = "saved_models/1"


CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]  # Index 0, 1, 2

# Lifespan events for modern FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load model
    try:
        app.state.model = tf.saved_model.load(MODEL_PATH)
        app.state.predict_fn = app.state.model.signatures['serving_default']
        print("✅ Model loaded successfully!")
        print(f"✅ Available classes: {CLASS_NAMES}")
        print(f"✅ Class mapping: 0={CLASS_NAMES[0]}, 1={CLASS_NAMES[1]}, 2={CLASS_NAMES[2]}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        raise e
    yield
    # Shutdown: Cleanup if needed
    print("Shutting down...")

app = FastAPI(
    title="Tomato Disease Classification API",
    description="API for classifying tomato plant diseases", 
    version="1.0.0",
    lifespan=lifespan
)

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    image = image.resize((256, 256))
    img_array = np.array(image, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.post("/predict", response_model=Dict[str, Any])
async def predict(file: UploadFile = File(..., description="Image of tomato plant leaf")):
    """Predict tomato disease from uploaded image"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        processed_image = preprocess_image(image)
        input_tensor = tf.constant(processed_image, dtype=tf.float32)
        
        predictions = app.state.predict_fn(input_tensor)
        output = list(predictions.values())[0].numpy()
        pred_values = output[0]
        
        class_idx = np.argmax(pred_values)
        confidence = float(np.max(pred_values))
        
        # ✅ DEBUG: Print actual values for verification
        print(f"🔍 Raw predictions: {pred_values}")
        print(f"🔍 Predicted index: {class_idx}")
        print(f"🔍 Predicted class: {CLASS_NAMES[class_idx]}")
        print(f"🔍 Confidence: {confidence:.4f}")
        
        # ✅ Create response with CORRECTED class names
        response = {
            "status": "success",
            "prediction": {
                "class": CLASS_NAMES[class_idx],
                "confidence": confidence,
                "class_id": int(class_idx)
            },
            "all_predictions": {
                "early_blight": float(pred_values[0]),
                "late_blight": float(pred_values[1]), 
                "healthy": float(pred_values[2])
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": hasattr(app.state, 'model')}

@app.get("/classes")
async def get_classes():
    return {"classes": CLASS_NAMES}

@app.get("/class-mapping")
async def get_class_mapping():
    """Returns detailed class mapping for verification"""
    mapping = {i: class_name for i, class_name in enumerate(CLASS_NAMES)}
    return {"class_mapping": mapping}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8003, reload=True)