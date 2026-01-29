# 🌾 Crop Yield Intelligence Platform
https://crop-yield-intelligence-app.streamlit.app/
A full-stack machine learning application that predicts crop yield using historical agricultural data, provides prediction confidence, and enables authenticated users to track their prediction history.

---

## 🚀 Features

- 🔐 Secure user authentication (Supabase)
- 🌱 Crop yield prediction using XGBoost
- 📊 Confidence-aware predictions
- 🧠 Optional model explainability (SHAP)
- 📁 User-specific prediction history
- ☁️ Deployed on Streamlit Cloud

---

## 🛠 Tech Stack

**Frontend**
- Streamlit

**Backend & Auth**
- Supabase (Auth + PostgreSQL + RLS)

**Machine Learning**
- XGBoost
- Scikit-learn
- SHAP (optional explainability)

**Utilities**
- NumPy, Pandas, Joblib

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Akhila-Dubasi/crop-yield-intelligence.git
cd crop-yield-intelligence
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Configure Supabase
Create .env locally or add secrets in Streamlit Cloud:

SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
4️⃣ Run App
streamlit run app.py
🔐 Database Notes
Table: user_predictions

Row Level Security (RLS) enabled

Users can only insert and view their own predictions

📈 Model Details
Algorithm: XGBoost Regressor

Inputs: State, Crop, Season, Year, Area

Output: Predicted Yield + Confidence Label

🌐 Deployment
Deployed using Streamlit Cloud
Supports secure environment variables via Streamlit Secrets.

📜 License
This project is for academic and learning purposes.

👤 Author
Akhila Dubasi
Machine Learning & Full-Stack Development

