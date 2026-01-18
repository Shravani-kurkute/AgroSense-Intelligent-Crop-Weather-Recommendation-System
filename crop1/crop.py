import streamlit as st
import joblib
import numpy as np


model = joblib.load("crop1\RandomForest_crop_yield.pkl")
encoders = joblib.load("crop1\encoders.pkl")
columns = joblib.load("crop1\columns.pkl")

crop_encoder = encoders["crop_encoder"]
state_encoder = encoders["state_encoder"]
season_encoder = encoders["season_encoder"]


def predict_yield(crop, state, season, year, area, production, rainfall, fertilizer, pesticide):
    crop_encoded = crop_encoder.transform([crop])[0]
    state_encoded = state_encoder.transform([state])[0]
    season_encoded = season_encoder.transform([season])[0]

    features = np.array([[crop_encoded, year, season_encoded, state_encoded,
                          area, production, rainfall, fertilizer, pesticide]])
    return model.predict(features)[0]


st.set_page_config(page_title="🌾 Kisan Crop Yield App", layout="centered")

st.title("🌱 किसान पैदावार भविष्यवाणी ऐप")
st.markdown("👉 चित्र देखकर जानकारी भरें और पैदावार जानें!")


st.subheader("🪴 अपनी फसल चुनें")

crop_options = crop_encoder.classes_  # all crop names from encoder



crop = st.radio("👉 अपनी फसल चुनें:", crop_options, horizontal=True)


state = st.selectbox("📍 राज्य चुनें", state_encoder.classes_)


st.subheader("☀️ सीजन चुनें")
season = st.radio(
    "सीजन:", 
    season_encoder.classes_,
    horizontal=True
)


year = st.slider("📅 साल", 1990, 2030, 2024)

st.image("https://cdn-icons-png.flaticon.com/512/4288/4288798.png", width=50)
area = st.slider("🌾 खेत का क्षेत्र (हेक्टेयर)", 0, 20000, 1000, step=100)

st.image("https://cdn-icons-png.flaticon.com/512/2331/2331888.png", width=50)
production = st.slider("🏭 उत्पादन (टन)", 0, 50000, 500, step=100)

st.image("https://cdn-icons-png.flaticon.com/512/414/414974.png", width=50)
rainfall = st.slider("🌧️ वर्षा (मिमी)", 0, 5000, 1200, step=50)

st.image("https://cdn-icons-png.flaticon.com/512/1047/1047711.png", width=50)
fertilizer = st.slider("🧪 खाद (किलो/हेक्टेयर)", 0, 10000, 200, step=50)

st.image("https://cdn-icons-png.flaticon.com/512/4341/4341771.png", width=50)
pesticide = st.slider("🛡️ कीटनाशक (किलो/हेक्टेयर)", 0, 5000, 50, step=10)


if st.button("🔍 पैदावार देखें"):
    prediction = predict_yield(crop, state, season, year, area, production, rainfall, fertilizer, pesticide)
    st.success(f"🌱 अनुमानित पैदावार: **{prediction:.2f} क्विंटल/हेक्टेयर**")
