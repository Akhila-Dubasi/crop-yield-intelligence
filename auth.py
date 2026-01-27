from supabase_client import supabase
import streamlit as st

def login(email, password):
    res = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    if res.session:
        st.session_state.supabase_session = res.session
    return res

def signup(email, password):
    return supabase.auth.sign_up({
        "email": email,
        "password": password
    })

def logout():
    supabase.auth.sign_out()
    st.session_state.supabase_session = None
