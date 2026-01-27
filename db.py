import os
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import shap

from supabase_client import supabase
from auth import signup, login, logout
from db import save_prediction, get_user_history

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Crop Yield Intelligence Platform",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# CACHED LOADERS (🔥 CRITICAL FIX)
# --------------------------------------------------
@st.cache_resource(show_spinner="Loading model...")
def load_model_bundle():
    return joblib.load(os.path.join(BASE_DIR, "model", "crop_model.pkl"))

@st.cache_resource(show_spinner=False)
def load_encoders():
    return joblib.load(os.path.join(BASE_DIR, "model", "encoders.pkl"))

@st.cache_resource(show_spinner=False)
def load_scaler():
    return joblib.load(os.path.join(BASE_DIR, "model", "scaler.pkl"))

@st.cache_resource(show_spinner="Preparing explanation engine...")
def load_explainer(model):
    return shap.TreeExplainer(model)

# --------------------------------------------------
# LOAD ONCE (FROM CACHE)
# --------------------------------------------------
model_bundle = load_model_bundle()
model = model_bundle["model"]
MODEL_VERSION = model_bundle["version"]

encoders = load_encoders()
scaler = load_scaler()

# ❗ explainer is loaded lazily later

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

session = supabase.auth.get_session()
if session and session.user:
    st.session_state.user = session.user

# ==================================================
# AUTH
# ==================================================
if st.session_state.user is None:
    st.title("🌾 Crop Yield Intelligence Platform")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = login(email, password)
            if res and res.user:
                st.session_state.user = res.user
                st.rerun()

    with tab2:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            signup(new_email, new_password)
            st.success("Account created. Please login.")

    st.stop()

# ==================================================
# DASHBOARD
# ==================================================
user = st.session_state.user

st.sidebar.success(f"Logged in as\n{user.email}")
st.sidebar.caption(f"Model version: {MODEL_VERSION}")

if st.sidebar.button("Logout"):
    logout()
    st.session_state.user = None
    st.rerun()

st.title("🌱 Crop Yield Prediction Dashboard")

# --------------------------------------------------
# INPUTS
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    state = st.selectbox("State", sorted(encoders["state_name"].classes_))
    crop = st.selectbox("Crop", sorted(encoders["crop"].classes_))
    season = st.selectbox("Season", sorted(encoders["season"].classes_))
    year = st.number_input("Year", 2000, 2035, 2025)

with col2:
    area = st.number_input("Area (hectares)", min_value=0.1, value=2.0)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("Predict Yield"):
    state_enc = encoders["state_name"].transform([state])[0]
    crop_enc = encoders["crop"].transform([crop])[0]
    season_enc = encoders["season"].transform([season])[0]

    year_scaled, area_scaled = scaler.transform([[year, area]])[0]

    X = np.array([[state_enc, crop_enc, season_enc, year_scaled, area_scaled]])

    # --- Prediction with uncertainty
    preds = [
        model.predict(X, iteration_range=(0, i + 1))[0]
        for i in range(min(100, model.n_estimators))
    ]

    preds = np.array(preds)
    mean_yield = max(0, preds.mean())
    std = preds.std()

    total_production = mean_yield * area

    # --- Confidence label
    cv = std / mean_yield if mean_yield > 0 else 1.0
    confidence = "High" if cv < 0.2 else "Medium" if cv < 0.5 else "Low"

    save_prediction(
        user.id,
        state,
        crop,
        season,
        year,
        round(float(total_production), 2),
        confidence
    )

    st.success(f"🌾 Yield: {mean_yield:.2f} t/ha")
    st.info(f"📦 Total Production: {total_production:.2f} tonnes")
    st.warning(f"🔍 Prediction Confidence: {confidence}")

    # --------------------------------------------------
    # EXPLANATION SECTION (LAZY LOAD)
    # --------------------------------------------------
    st.subheader("🧠 Model Explanation")

    explainer = load_explainer(model)
    shap_values = explainer.shap_values(X)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Feature Importance (Global)")
        fi_df = pd.DataFrame({
            "Feature": ["State", "Crop", "Season", "Year", "Area"],
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.bar_chart(fi_df.set_index("Feature"))

    with col_b:
        st.markdown("### SHAP Explanation (This Prediction)")
        shap_df = pd.DataFrame({
            "Feature": ["State", "Crop", "Season", "Year", "Area"],
            "Impact": shap_values[0]
        }).sort_values(by="Impact", key=abs, ascending=False)

        st.bar_chart(shap_df.set_index("Feature"))

# --------------------------------------------------
# HISTORY
# --------------------------------------------------
st.subheader("📊 Prediction History")

history = get_user_history(user.id)
if history:
    st.dataframe(pd.DataFrame(history), use_container_width=True)
