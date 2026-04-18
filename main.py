from fastapi import FastAPI
from schemas import WinProbabilityResponse, ErrorResponse
from services import calculate_win_probability

app = FastAPI(title="Win Probability Label API")

@app.get("/")
def home():
    return {"status": "Online", "api": "Win Probability Engine"}

@app.get(
    "/api/predict/", 
    response_model=WinProbabilityResponse, 
    responses={400: {"model": ErrorResponse}}
)
def predict(target: int, current_score: int, balls_bowled: int, 
            total_overs: int, wickets_fallen: int):
    return calculate_win_probability(target, current_score, balls_bowled, total_overs, wickets_fallen)