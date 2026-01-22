import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load local .env (ignored on Streamlit Cloud)
load_dotenv()

def get_supabase_client():
    # Prefer Streamlit secrets (Cloud)
    supabase_url = st.secrets.get("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY")

    # Fallback to local env
    if not supabase_url or not supabase_key:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase credentials missing. "
            "Set them in Streamlit Secrets or .env file."
        )

    return create_client(supabase_url, supabase_key)

# Initialize once
supabase = get_supabase_client()
