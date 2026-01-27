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
        # 🔥 MUST be string UUID for RLS to pass
        "user_id": str(user_id),

        "state_name": state,
        "crop": crop,
        "season": season,
        "year": int(year),
        "predicted_yield": float(predicted_yield),
        "confidence_level": confidence_level,
    }

    response = supabase.table("user_predictions").insert(data).execute()
    return response.data


def get_user_history(user_id):
    response = (
        supabase
        .table("user_predictions")
        .select("*")
        .eq("user_id", str(user_id))   # 🔥 MUST be string
        .order("created_at", desc=True)
        .execute()
    )
    return response.data
