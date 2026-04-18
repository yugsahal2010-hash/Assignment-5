from fastapi import HTTPException

# --- 1. Innings Summary Logic ---
def get_innings_summary_data():
    # Placeholder for your data aggregation logic
    return {"status": "Innings Data Ready"}

# --- 2. Match State Logic ---
def get_match_state_data():
    return {"match": "India vs Pakistan", "status": "Live"}

# --- 3. Required Run Rate Logic ---
def calculate_rrr(target: int, current_score: int, balls_remaining: int) -> dict:
    if target <= 0:
        raise HTTPException(status_code=400, detail="Not a chase situation.")
    
    runs_needed = max(0, target - current_score)
    rrr = round((runs_needed / (balls_remaining / 6)), 2) if balls_remaining > 0 else 0.0
    
    return {
        "target": target,
        "current_score": current_score,
        "runs_needed": runs_needed,
        "balls_remaining": balls_remaining,
        "required_run_rate": rrr
    }

# --- 4. Win Probability Engine Logic (The Redesigned Formula) ---
def calculate_win_probability(target: int, current_score: int, balls_bowled: int, 
                              total_overs: int, wickets_fallen: int) -> dict:
    
    # --- Validation Layer ---
    if total_overs <= 0:
        raise HTTPException(status_code=400, detail="Total overs must be > 0.")
    if not (0 <= wickets_fallen <= 10):
        raise HTTPException(status_code=400, detail="Wickets must be 0-10.")
    if not (0 <= balls_bowled <= (total_overs * 6)):
        raise HTTPException(status_code=400, detail="Invalid balls bowled count.")

    # --- Math Layer ---
    runs_required = target - current_score
    balls_remaining = (total_overs * 6) - balls_bowled
    wickets_in_hand = 10 - wickets_fallen
    
    # Edge Case: Match Concluded
    if balls_remaining <= 0 or balls_bowled == 0 or runs_required <= 0:
        return {
            "runs_needed": max(0, runs_required),
            "balls_remaining": max(0, balls_remaining),
            "required_run_rate": 0.0,
            "win_probability_score": 100.0 if runs_required <= 0 else 0.0,
            "prediction": "Match Concluded"
        }

    # --- Core Engine (Your Formula) ---
    required_run_rate = (runs_required * 6) / balls_remaining
    current_run_rate = (current_score * 6) / balls_bowled
    
    rrr_ratio = current_run_rate / required_run_rate
    resource_factor = (balls_remaining / (total_overs * 6)) * (wickets_in_hand / 10)
    
    win_probability = (rrr_ratio * resource_factor * 100)
    
    # Classification
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