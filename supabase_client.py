import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client() -> Client:
    # Streamlit Cloud secrets first
    supabase_url = st.secrets.get("SUPABASE_URL", None)
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY", None)

    # Local fallback
    if not supabase_url or not supabase_key:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase credentials not found. "
            "Set them in Streamlit Secrets or .env"
        )

    # 🔥 CRITICAL FIX: disable http2
    return create_client(
        supabase_url,
        supabase_key,
        options={
            "schema": "public",
            "headers": {"X-Client-Info": "crop-yield-intelligence"},
            "auth": {"persist_session": True},
            "realtime": {"enabled": False},
            "global": {"http2": False},
        },
    )


supabase = get_supabase_client()
