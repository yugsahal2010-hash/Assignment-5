from fastapi import HTTPException


def calculate_win_probability(data: dict) -> dict:
    target = data["target"]
    current_score = data["current_score"]
    balls_bowled = data["balls_bowled"]
    total_overs = data["total_overs"]
    wickets_fallen = data["wickets_fallen"]

    # --- Validation ---
    if total_overs <= 0:
        raise HTTPException(status_code=400, detail="Total overs must be > 0.")
    if not (0 <= wickets_fallen <= 10):
        raise HTTPException(status_code=400, detail="Wickets must be 0-10.")
    if not (0 <= balls_bowled <= (total_overs * 6)):
        raise HTTPException(status_code=400, detail="Invalid balls bowled count.")

    # --- Math ---
    runs_required = target - current_score
    balls_remaining = (total_overs * 6) - balls_bowled
    wickets_in_hand = 10 - wickets_fallen

    # --- Edge Case: Match Concluded ---
    if balls_remaining <= 0 or balls_bowled == 0 or runs_required <= 0:
        return {
            "runs_needed": max(0, runs_required),
            "balls_remaining": max(0, balls_remaining),
            "required_run_rate": 0.0,
            "win_probability_score": 100.0 if runs_required <= 0 else 0.0,
            "prediction": "Match Concluded"
        }

    # --- Core Engine ---
    required_run_rate = (runs_required * 6) / balls_remaining
    current_run_rate = (current_score * 6) / balls_bowled

    rrr_ratio = current_run_rate / required_run_rate
    resource_factor = (balls_remaining / (total_overs * 6)) * (wickets_in_hand / 10)

    win_probability = rrr_ratio * resource_factor * 100

    if win_probability > 80: prediction = "High Chance"
    elif win_probability > 40: prediction = "Medium Chance"
    else: prediction = "Low Chance"

    return {
        "runs_needed": runs_required,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(required_run_rate, 2),
        "win_probability_score": round(win_probability, 2),
        "prediction": prediction
    }
