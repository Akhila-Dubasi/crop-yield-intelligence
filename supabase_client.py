import os
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client():
    supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    supabase_key = st.secrets.get("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError("Supabase credentials missing")

    client = create_client(supabase_url, supabase_key)

    # 🔥 VERY IMPORTANT: attach auth session if exists
    session = st.session_state.get("supabase_session")
    if session:
        client.auth.set_session(
            session.access_token,
            session.refresh_token
        )

    return client

supabase = get_supabase_client()
