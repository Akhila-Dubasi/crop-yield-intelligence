from supabase_client import supabase

def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

def login(email, password):
    return supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def logout():
    supabase.auth.sign_out()
