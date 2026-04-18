from pydantic import BaseModel, Field

class WinProbabilityResponse(BaseModel):
    runs_needed: int
    balls_remaining: int
    required_run_rate: float
    win_probability_score: float
    prediction: str


class ErrorResponse(BaseModel):
    detail: str    