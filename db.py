from supabase_client import supabase


def save_prediction(user_id, state, crop, season, year, yield_value, confidence):
    response = (
        supabase.table("user_predictions")
        .insert({
            "user_id": user_id,  # 🔑 REQUIRED FOR RLS
            "state": state,
            "crop": crop,
            "season": season,
            "year": year,
            "predicted_yield": yield_value,
            "confidence": confidence
        })
        .execute()
    )
    return response


def get_user_history(user_id):
    response = (
        supabase.table("user_predictions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data
