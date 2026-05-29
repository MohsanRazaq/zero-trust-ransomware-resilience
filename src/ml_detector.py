import pandas as pd
import joblib
from pathlib import Path
from src.logger import write_log

# Point directly to the compiled serialized brain asset in your root folder
MODEL_PATH = Path(__file__).resolve().parent.parent / "ransomware_model.pkl"
model = None

# Open src/ml_detector.py and update your load function:

def load_ml_model():
    global model
    if model is None:
        try:
            if MODEL_PATH.exists():
                model = joblib.load(MODEL_PATH)
                
                # Change print() to write_log() to force it into activity.log
                write_log("[⚙️ ML ENGINE] Machine Learning model brain loaded successfully.")
        except:
            pass

def predict_malicious_intent(velocity, entropy):
    """
    Passes live metrics into the Random Forest model with explicit feature names
    to eliminate runtime alignment warnings.
    """
    global model
    if model is None:
        load_ml_model()
        
    if model is not None:
        try:
            # ◄— Convert the raw 2D list into a structured DataFrame with correct headers
            live_features = pd.DataFrame(
                [[velocity, entropy]], 
                columns=['velocity', 'entropy']
            )
            
            # Query the model with named features
            prediction = model.predict(live_features)
            return bool(prediction[0] == 1)
        except Exception as e:
            write_log(f"[ML LIVE ERROR] Inference execution fault: {e}")
            
    return bool(velocity > 12 and entropy > 6.5)