# db.py
from typing import List, Dict

def save_prediction(
    user_id: str,
    state: str,
    crop: str,
    season: str,
    year: int,
    predicted_yield: float,
    confidence: str
):
    from supabase_client import supabase  # ✅ IMPORT INSIDE FUNCTION

    data = {
        "user_id": user_id,
        "state_name": state,
        "crop": crop,
        "season": season,
        "year": year,
        "predicted_yield": predicted_yield,
        "confidence_level": confidence
    }

    response = supabase.table("user_predictions").insert(data).execute()
    return response


def get_user_history(user_id: str) -> List[Dict]:
    from supabase_client import supabase  # ✅ IMPORT INSIDE FUNCTION

    response = (
        supabase
        .table("user_predictions")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data if response.data else []
