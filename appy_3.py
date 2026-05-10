import streamlit as st
import requests
import re

# =====================================================
# CONFIG
# =====================================================

API_URL = "https://api-inference.huggingface.co/models/envidevelopment/model2"

headers = {
    "Authorization": "Bearer HF_TOKEN_ANDA"
}

# =====================================================
# PAGE
# =====================================================

st.set_page_config(
    page_title="Analisis Emosi Livin",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Analisis Emosi & Sarkasme")

st.markdown("""
Analisis emosi nasabah mobile banking
berbasis IndoBERT Transformer
""")

# =====================================================
# CLEANING
# =====================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# =====================================================
# QUERY API
# =====================================================

def query(payload):

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload
    )

    return response.json()

# =====================================================
# PREDICT
# =====================================================

emotion_classes = [
    "cemas",
    "frustrasi",
    "marah",
    "netral",
    "puas",
    "senang"
]

def predict_emotion(text):

    cleaned = clean_text(text)

    output = query({
        "inputs": cleaned
    })

    label = output[0][0]["label"]

    score = output[0][0]["score"]

    label_id = int(
        label.split("_")[-1]
    )

    emotion = emotion_classes[label_id]

    return emotion, score

# =====================================================
# STYLE
# =====================================================

emotion_styles = {

    "marah": {
        "emoji": "😡",
        "color": "#FF4B4B"
    },

    "frustrasi": {
        "emoji": "😤",
        "color": "#FF9800"
    },

    "cemas": {
        "emoji": "😰",
        "color": "#8E44AD"
    },

    "senang": {
        "emoji": "😊",
        "color": "#00C853"
    },

    "puas": {
        "emoji": "😌",
        "color": "#03A9F4"
    },

    "netral": {
        "emoji": "😐",
        "color": "#607D8B"
    }
}

# =====================================================
# INPUT
# =====================================================

text = st.text_area(
    "Masukkan ulasan nasabah"
)

# =====================================================
# BUTTON
# =====================================================

if st.button("🔍 Analisis"):

    if text.strip() == "":

        st.warning(
            "Masukkan ulasan terlebih dahulu"
        )

    else:

        emotion, confidence = predict_emotion(
            text
        )

        style = emotion_styles[emotion]

        st.markdown("---")

        st.markdown("## 📌 Hasil Analisis")

        st.markdown(
            f"""
            <div style="
                background-color:{style['color']};
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:white;
            ">
                <h1>
                    {style['emoji']} {emotion.upper()}
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            "🎯 Confidence Score",
            f"{confidence*100:.2f}%"
        )
