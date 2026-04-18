from fastapi import FastAPI
from services import get_win_prediction_data

app = FastAPI(title="Win Probability Engine")

@app.get("/")
def home():
    return {"status": "Online", "message": "Engine is running internal heuristics."}

@app.get("/api/predict/")
def predict():
    # No inputs required, it pulls directly from the service
    return get_win_prediction_data()