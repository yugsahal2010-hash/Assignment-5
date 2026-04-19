from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import WinProbabilityInput, WinProbabilityResponse, ErrorResponse
from services import calculate_win_probability

app = FastAPI(title="Win Probability Label API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "Online", "api": "Win Probability Engine"}


@app.post(
    "/api/predict/",
    response_model=WinProbabilityResponse,
    responses={400: {"model": ErrorResponse}}
)
def predict(input_data: WinProbabilityInput):
    return calculate_win_probability(input_data.model_dump())
