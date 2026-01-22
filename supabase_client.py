import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

# Load local .env (ignored on Streamlit Cloud)
load_dotenv()

@st.cache_resource(show_spinner=False)
def get_supabase_client():
    # Prefer Streamlit Secrets (Cloud)
    supabase_url = st.secrets.get("SUPABASE_URL", None)
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", None)

    # Fallback to local env (for local dev)
    if not supabase_url or not supabase_key:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase credentials missing. "
            "Set SUPABASE_URL and SUPABASE_ANON_KEY in Streamlit Secrets."
        )

    return create_client(supabase_url, supabase_key)

# Initialized once and cached
supabase = get_supabase_client()
