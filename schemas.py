from pydantic import BaseModel, Field


class WinProbabilityInput(BaseModel):
    target: int
    current_score: int
    balls_bowled: int
    total_overs: int
    wickets_fallen: int


class WinProbabilityResponse(BaseModel):
    runs_needed: int
    balls_remaining: int
    required_run_rate: float
    win_probability_score: float
    prediction: str


class ErrorResponse(BaseModel):
    detail: str
