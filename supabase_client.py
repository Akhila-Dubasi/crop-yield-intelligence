import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

def get_supabase_client():
    # 1️⃣ Try Streamlit secrets (Cloud)
    supabase_url = st.secrets.get("SUPABASE_URL", None)
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", None)

    # 2️⃣ Fallback to environment variables (local)
    if not supabase_url or not supabase_key:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

    # 3️⃣ Final safety check
    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase credentials not found. "
            "Set them in Streamlit Secrets or .env file."
        )

    return create_client(supabase_url, supabase_key)


# Initialize client safely
supabase = get_supabase_client()
