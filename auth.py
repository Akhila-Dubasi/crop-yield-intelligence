from supabase_client import supabase


def login(email: str, password: str):
    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except Exception:
        # User not found OR wrong password
        return None


def signup(email: str, password: str):
    try:
        return supabase.auth.sign_up({
            "email": email,
            "password": password
        })
    except Exception:
        return None


def logout():
    supabase.auth.sign_out()
