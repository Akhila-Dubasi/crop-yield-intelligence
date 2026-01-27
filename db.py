from supabase_client import supabase

def save_prediction(
    user_id,
    state,
    crop,
    season,
    year,
    predicted_yield,
    confidence_level
):
    data = {
        "user_id": user_id,              # 🔥 REQUIRED for RLS
        "state_name": state,
        "crop": crop,
        "season": season,
        "year": int(year),
        "predicted_yield": float(predicted_yield),
        "confidence_level": confidence_level,
    }

    response = supabase.table("user_predictions").insert(data).execute()
    return response


def get_user_history(user_id):
    response = (
        supabase
        .table("user_predictions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data
