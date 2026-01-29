from supabase_client import supabase
from uuid import UUID

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
        "user_id": UUID(user_id),   # ✅ ENSURE UUID TYPE
        "state_name": state,
        "crop": crop,
        "season": season,
        "year": int(year),
        "predicted_yield": float(predicted_yield),
        "confidence_level": confidence_level,
    }

    return supabase.table("user_predictions").insert(data).execute()


def get_user_history(user_id):
    return (
        supabase
        .table("user_predictions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )
