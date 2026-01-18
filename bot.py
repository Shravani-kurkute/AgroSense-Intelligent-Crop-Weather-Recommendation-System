import streamlit as st
import numpy as np
import joblib

# Load model and encoders
model = joblib.load("crop4/combined_crop_model.pkl")
scaler = joblib.load("crop4/scaler.pkl")
weather_encoder = joblib.load("crop4/weather_encoder.pkl")

st.set_page_config(page_title="फसल शिफारस चॅटबॉट", page_icon="🤖", layout="centered")
st.title("🤖 शेतकरी फसल शिफारस चॅटबॉट")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "step" not in st.session_state:
    st.session_state.step = 0

# Yield reference (tons/hectare)
yield_reference = {
    "rice": 3.5, "wheat": 3.2, "maize": 4.0,
    "cotton": 2.0, "sugarcane": 70.0, "barley": 2.5,
    "chickpea": 1.8, "banana": 30.0, "lentil": 1.5,
    "groundnut": 2.0, "soybean": 2.8,
}

# Conversation questions (step-by-step)
questions = [
    ("N", "🪴 आपल्या जमिनीत नायट्रोजन (N) किती आहे?", "slider", (0, 200, 50)),
    ("P", "🪴 फॉस्फरस (P) किती आहे?", "slider", (0, 200, 50)),
    ("K", "🪴 पोटॅशियम (K) किती आहे?", "slider", (0, 200, 50)),
    ("ph", "🪴 मातीचा pH किती आहे?", "slider", (3.5, 9.0, 6.5, 0.1)),
    ("rainfall", "🌧️ वार्षिक पावसाचे प्रमाण (mm) किती आहे?", "slider", (0, 500, 200)),
    ("temperature", "🌡️ सरासरी तापमान (°C) किती आहे?", "slider", (0, 50, 25)),
    ("humidity", "💧 आर्द्रता (%) किती आहे?", "slider", (0, 100, 60)),
    ("precipitation", "☔ दैनंदिन पाऊस (mm) किती आहे?", "slider", (0, 100, 10)),
    ("wind", "💨 वाऱ्याचा वेग (m/s) किती आहे?", "slider", (0, 30, 5)),
    ("weather", "🌦️ हवामान निवडा?", "radio", ["sun", "rain", "drizzle", "fog", "snow"]),
    ("area", "🌍 शेताचे क्षेत्रफळ (हेक्टर मध्ये) किती आहे?", "number", (0.1, 1000.0, 1.0, 0.1)),
    ("region", "📍 आपला प्रदेश (उदा. विदर्भ, पंजाब, बिहार) सांगा?", "text", ""),
]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ask next question
step = st.session_state.step
if step < len(questions):
    key, q_text, q_type, params = questions[step]

    with st.chat_message("assistant"):
        st.markdown(q_text)

    answer = None
    if q_type == "slider":
        if len(params) == 3:
            answer = st.slider("तुमचे उत्तर", params[0], params[1], params[2], key=key)
        else:
            answer = st.slider("तुमचे उत्तर", params[0], params[1], params[2], step=params[3], key=key)

    elif q_type == "radio":
        answer = st.radio("तुमचे उत्तर", params, key=key)

    elif q_type == "number":
        answer = st.number_input("तुमचे उत्तर", params[0], params[1], params[2], step=params[3], key=key)

    elif q_type == "text":
        answer = st.text_input("तुमचे उत्तर", key=key)

    if answer is not None and (q_type != "text" or answer.strip() != ""):
        if st.button("पुढे ➡️", key=f"next_{step}"):
            st.session_state.inputs[key] = answer
            st.session_state.messages.append({"role": "assistant", "content": q_text})
            st.session_state.messages.append({"role": "user", "content": str(answer)})
            st.session_state.step += 1
            st.rerun()
else:
    # All inputs done -> Prediction
    inp = st.session_state.inputs
    weather_encoded = weather_encoder.transform([inp["weather"]])[0]

    features = np.array([[inp["N"], inp["P"], inp["K"], inp["temperature"], inp["humidity"],
                          inp["ph"], inp["rainfall"], inp["precipitation"], inp["wind"],
                          inp["temperature"], weather_encoded]])

    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]

    response = f"🌱 शिफारस केलेली फसल: **{prediction}**\n\n📍 प्रदेश: {inp['region']}"
    if prediction in yield_reference:
        est_yield = yield_reference[prediction] * inp["area"]
        response += f"\n\n🌍 अंदाजे उत्पादन: **{est_yield:.2f} टन**"
    else:
        response += "\n\n📊 या पिकासाठी उत्पादन डेटा उपलब्ध नाही."

    with st.chat_message("assistant"):
        st.markdown(response)


