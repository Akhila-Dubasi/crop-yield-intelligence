from supabase_client import supabase

def save_prediction(user_id, state, crop, season, year, predicted_yield, confidence):
    supabase.table("user_predictions").insert({
        "user_id": user_id,
        "state_name": state,
        "crop": crop,
        "season": season,
        "year": year,
        "predicted_yield": predicted_yield,
        "confidence_level": confidence
    }).execute()


def get_user_history(user_id):
    res = (
        supabase.table("user_predictions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data
