import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load .env for local development (ignored on Streamlit Cloud)
load_dotenv()

def get_supabase_client():
    """
    Create and return a Supabase client.
    Priority:
    1. Streamlit Cloud secrets
    2. Local .env variables
    """

    # 1️⃣ Streamlit Cloud secrets
    supabase_url = st.secrets.get("SUPABASE_URL", None)
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", None)

    # 2️⃣ Local environment fallback
    if not supabase_url or not supabase_key:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

    # 3️⃣ Final validation
    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "❌ Supabase credentials missing.\n"
            "Add SUPABASE_URL and SUPABASE_ANON_KEY to:\n"
            "• Streamlit Secrets (Cloud)\n"
            "• or .env file (local)"
        )

    return create_client(supabase_url, supabase_key)


# ✅ SINGLE shared client (important)
supabase = get_supabase_client()
