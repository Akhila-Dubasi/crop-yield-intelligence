import pandas as pd
import numpy as np
import os
import joblib

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../data/crop_production.csv")
MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "encoders.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
df = pd.read_csv(DATA_PATH)

# --------------------------------------------------
# RENAME COLUMNS (CRITICAL FIX)
# --------------------------------------------------
df = df.rename(columns={"Crop_Year": "Year"})

# Keep only required columns
df = df[[
    "State_Name",
    "Crop",
    "Season",
    "Year",
    "Area",
    "Production"
]]

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------
df = df.dropna(subset=["Area", "Production"])
df = df[(df["Area"] > 0) & (df["Production"] >= 0)]

# --------------------------------------------------
# TARGET ENGINEERING
# --------------------------------------------------
df["Yield"] = df["Production"] / df["Area"]

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=["Yield"])

# --------------------------------------------------
# OUTLIER REMOVAL (IQR)
# --------------------------------------------------
Q1 = df["Yield"].quantile(0.25)
Q3 = df["Yield"].quantile(0.75)
IQR = Q3 - Q1

df = df[
    (df["Yield"] >= Q1 - 1.5 * IQR) &
    (df["Yield"] <= Q3 + 1.5 * IQR)
]

# --------------------------------------------------
# ENCODE CATEGORICAL VARIABLES
# --------------------------------------------------
encoders = {}

for col in ["State_Name", "Crop", "Season"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col.lower()] = le

# --------------------------------------------------
# SCALE NUMERICAL FEATURES
# --------------------------------------------------
scaler = StandardScaler()
df[["Year", "Area"]] = scaler.fit_transform(df[["Year", "Area"]])

# --------------------------------------------------
# TRAIN / TEST SPLIT (TIME-AWARE)
# --------------------------------------------------
split_year = df["Year"].quantile(0.8)

train_df = df[df["Year"] <= split_year]
test_df  = df[df["Year"] > split_year]

X_train = train_df[["State_Name", "Crop", "Season", "Year", "Area"]]
y_train = train_df["Yield"]

X_test = test_df[["State_Name", "Crop", "Season", "Year", "Area"]]
y_test = test_df["Yield"]

# --------------------------------------------------
# MODEL
# --------------------------------------------------
model = XGBRegressor(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.5,
    reg_lambda=1.0,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# EVALUATION
# --------------------------------------------------
y_pred = model.predict(X_test)

print("✅ Model Evaluation")
print(f"MAE (Yield per hectare): {mean_absolute_error(y_test, y_pred):.4f}")
print(f"R² Score: {r2_score(y_test, y_pred):.4f}")

# --------------------------------------------------
# SAVE ARTIFACTS
# --------------------------------------------------
MODEL_VERSION = "v2.1-yield-shap-confidence"

joblib.dump(
    {
        "model": model,
        "version": MODEL_VERSION
    },
    MODEL_PATH
)

joblib.dump(encoders, ENCODER_PATH)
joblib.dump(scaler, SCALER_PATH)

print("✅ Model saved with version:", MODEL_VERSION)

joblib.dump(encoders, ENCODER_PATH)
joblib.dump(scaler, SCALER_PATH)
print("✅ Model saved with version:", MODEL_VERSION)
print("✅ Improved model, encoders, and scaler saved")
