import streamlit as st
import numpy as np
import joblib
import datetime

# -------------------------------
# Load Saved Model & Encoders
# -------------------------------
model = joblib.load("crop3\weather_model.pkl")
label_encoder = joblib.load("crop3\weather_encoder.pkl")
scaler = joblib.load("crop3\weather_scaler.pkl")
columns = joblib.load("crop3\weather_columns.pkl")

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🌦 Farmer Weather Predictor", page_icon="🌾", layout="centered")

st.title("🌦 Smart Weather Prediction for Farmers")
st.write("👨‍🌾 Enter your farm’s conditions below and get weather prediction.")

# Farmer-friendly inputs
precipitation = st.slider("💧 Rainfall (mm)", 0.0, 100.0, 10.0)
temp_max = st.slider("🌡 Maximum Temperature (°C)", -5.0, 45.0, 25.0)
temp_min = st.slider("🌡 Minimum Temperature (°C)", -10.0, 35.0, 15.0)
wind = st.slider("🍃 Wind Speed (m/s)", 0.0, 15.0, 2.0)

# Date input (for month, day, season features)
date_input = st.date_input("📅 Select Date", datetime.date.today())
year = date_input.year
month = date_input.month
day = date_input.day
day_of_week = date_input.weekday()  # 0=Mon
season = (month % 12) // 3 + 1

temp_range = temp_max - temp_min

features = np.array([[precipitation, temp_max, temp_min, wind,
                      year, month, day, day_of_week, season, temp_range]])



# Scale numeric values
features_scaled = scaler.transform(features)

# Ensure same feature order
if len(columns) == features_scaled.shape[1]:
    pass
else:
    st.error("⚠ Feature mismatch! Please retrain with correct feature list.")

# -------------------------------
# Prediction
# -------------------------------
if st.button("🌾 Predict Weather"):
    prediction = model.predict(features_scaled)
    weather_class = label_encoder.inverse_transform(prediction)[0]

    # Farmer-friendly messages
    st.success(f"🌤 Predicted Weather: **{weather_class}**")

    if weather_class.lower() in ["rain", "drizzle"]:
        st.info("💡 Suggestion: Keep your crops covered and ensure good drainage.")
    elif weather_class.lower() in ["sun", "clear"]:
        st.info("💡 Suggestion: Great day for sowing and outdoor farm work.")
    elif weather_class.lower() in ["snow"]:
        st.warning("⚠ Snow expected. Protect sensitive crops.")
    elif weather_class.lower() in ["fog"]:
        st.warning("⚠ Low visibility, plan accordingly.")
    else:
        st.info("💡 Normal conditions for farming.")
