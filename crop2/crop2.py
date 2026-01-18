import streamlit as st
import numpy as np
import joblib

# Load model and encoder
model = joblib.load("crop2\crop_model.pkl")
le = joblib.load("crop2\label_encoder.pkl")

# App Title
st.set_page_config(page_title="Crop Recommendation System", page_icon="🌱", layout="centered")
st.title("🌾 Farmer's Crop Recommendation System")
st.markdown("👨‍🌾 Enter your soil and weather details to get the **best crop suggestion** for your farm!")

# Input sliders
st.subheader("📊 Soil Nutrients")
N = st.slider("🌱 Nitrogen (N)", 0, 150, 50)
P = st.slider("🌿 Phosphorus (P)", 0, 150, 50)
K = st.slider("🌾 Potassium (K)", 0, 200, 50)

st.subheader("🌤 Weather Conditions")
temperature = st.slider("🌡 Temperature (°C)", 0, 50, 25)
humidity = st.slider("💧 Humidity (%)", 0, 100, 50)
ph = st.slider("⚖ Soil pH", 0.0, 14.0, 6.5)
rainfall = st.slider("🌧 Rainfall (mm)", 0, 300, 100)

# Predict button
if st.button("🔍 Recommend Crop"):
    sample = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(sample)
    crop_name = le.inverse_transform(prediction)[0]
    st.success(f"🌾 Recommended Crop for You: **{crop_name}**")

# Footer
st.markdown("---")
st.markdown("✨ Developed to help farmers make better decisions for sustainable farming 🌍")
