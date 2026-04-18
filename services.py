def get_win_prediction_data():
    # This is the "internal" data point
    # In the future, you can swap this to fetch from your database
    match_data = {
        "target": 160,
        "current_score": 100,
        "balls_bowled": 60,
        "total_overs": 20,
        "wickets_fallen": 3
    }
    
    # Mathematical logic
    runs_required = match_data["target"] - match_data["current_score"]
    balls_remaining = (match_data["total_overs"] * 6) - match_data["balls_bowled"]
    wickets_in_hand = 10 - match_data["wickets_fallen"]
    
    required_run_rate = (runs_required * 6) / balls_remaining if balls_remaining > 0 else 0
    current_run_rate = (match_data["current_score"] * 6) / match_data["balls_bowled"] if match_data["balls_bowled"] > 0 else 0
    
    rrr_ratio = current_run_rate / required_run_rate if required_run_rate > 0 else 0
    resource_factor = (balls_remaining / (match_data["total_overs"] * 6)) * (wickets_in_hand / 10)
    
    win_probability = (rrr_ratio * resource_factor * 100)
    
    # Categorization
    if win_probability > 80: prediction = "High Chance"
    elif win_probability > 40: prediction = "Medium Chance"
    else: prediction = "Low Chance"
    
    return {
        "runs_needed": runs_required,
        "balls_remaining": balls_remaining,
        "required_run_rate": round(required_run_rate, 2),
        "prediction": prediction
    }