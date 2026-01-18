import streamlit as st
import numpy as np
import joblib


model = joblib.load("crop4/combined_crop_model.pkl")
scaler = joblib.load("crop4/scaler.pkl")
weather_encoder = joblib.load("crop4/weather_encoder.pkl")

st.set_page_config(page_title="फसल शिफारस प्रणाली", page_icon="🌾", layout="centered")

st.title("🌾 शेतकरी फसल शिफारस प्रणाली")
st.write("आपल्या जमिनीची, हवामानाची माहिती, क्षेत्रफळ व प्रदेश द्या आणि कोणती फसल लावावी व किती उत्पादन मिळेल ते जाणून घ्या ✅")


st.subheader("📍 प्रदेशाची माहिती")
regions = ["विदर्भ", "मराठवाडा", "पश्चिम महाराष्ट्र", "उत्तर महाराष्ट्र", "कोकण", "पंजाब", "उत्तर प्रदेश", "मध्य प्रदेश", "बिहार", "इतर"]
region = st.selectbox("आपला प्रदेश निवडा:", regions)


st.subheader("🪴 मातीची माहिती")
N = st.slider("नायट्रोजन (N)", 0, 150, 50)
P = st.slider("फॉस्फरस (P)", 0, 150, 50)
K = st.slider("पोटॅशियम (K)", 0, 200, 50)
ph = st.slider("pH मूल्य", 0.0, 14.0, 6.5)
rainfall = st.slider("पावसाचे प्रमाण (mm)", 0.0, 300.0, 100.0)


st.subheader("🌦️ हवामानाची माहिती")
temperature = st.slider("तापमान (°C)", 0.0, 50.0, 25.0)
humidity = st.slider("आर्द्रता (%)", 0, 100, 60)
precipitation = st.slider("पाऊस (mm/day)", 0.0, 50.0, 5.0)
wind = st.slider("वाऱ्याचा वेग (m/s)", 0.0, 15.0, 2.0)


weather_options = {
    "sun": "☀️ उन्हाळी",
    "rain": "🌧️ पावसाळी",
    "drizzle": "🌦️ रिमझिम",
    "fog": "🌫️ धुके",
    "snow": "❄️ बर्फाळ",
}
weather_choice = st.radio("हवामानाची स्थिती निवडा:", list(weather_options.values()))

# Encode selected weather
weather_key = list(weather_options.keys())[list(weather_options.values()).index(weather_choice)]
weather_encoded = weather_encoder.transform([weather_key])[0]


st.subheader("🌍 शेताचे क्षेत्रफळ")
area = st.slider("आपल्या शेताचे क्षेत्रफळ (हेक्टर मध्ये)", min_value=0.1, step=0.1)


yield_reference = {
    "rice": 3.5,
    "wheat": 3.2,
    "maize": 4.0,
    "cotton": 2.0,
    "sugarcane": 70.0,
    "barley": 2.5,
    "chickpea": 1.8,
    "banana": 30.0,
    "lentil": 1.5,
    "groundnut": 2.0,
    "soybean": 2.8,
    
}


if st.button("👉 फसल जाणून घ्या"):
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall,
                          precipitation, wind, temperature, weather_encoded]])
    
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]

    st.success(f"🌱 शिफारस केलेली फसल: **{prediction}**")
    st.write(f"📍 प्रदेश: **{region}**")

    # Estimate Yield
    if prediction in yield_reference:
        estimated_yield = yield_reference[prediction] * area
        st.info(f"🌍 अंदाजे उत्पादन: **{estimated_yield:.2f} टन** (क्षेत्रफळ: {area} हेक्टर)")
    else:
        st.warning("📊 या पिकासाठी उत्पादन डेटा उपलब्ध नाही.")
