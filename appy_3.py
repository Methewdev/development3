import streamlit as st
import pandas as pd
import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#020B1C;
}

[data-testid="stSidebar"]{
    background-color:#09152D;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DEVICE
# =====================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

# =====================================================
# MODEL LOADER
# =====================================================

@st.cache_resource
def load_sentiment_model():

    tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model


@st.cache_resource
def load_emotion_model():

    tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/emotion_model"
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/emotion_model"
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model

# =====================================================
# PREDICTION
# =====================================================

def predict_sentiment(text):

    tokenizer, model = load_sentiment_model()

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(
        outputs.logits,
        dim=1
    )

    confidence = torch.max(
        probs
    ).item()

    pred = torch.argmax(
        probs,
        dim=1
    ).item()

    label_map = {
        0: "Negatif",
        1: "Netral",
        2: "Positif"
    }

    return (
        label_map.get(pred, "Unknown"),
        round(confidence * 100, 2)
    )

def predict_emotion(text):

    tokenizer, model = load_emotion_model()

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    probs = F.softmax(
        outputs.logits,
        dim=1
    )

    confidence = torch.max(
        probs
    ).item()

    pred = torch.argmax(
        probs,
        dim=1
    ).item()

    emotion_map = {
        0: "😡 Anger",
        1: "😨 Fear",
        2: "😊 Happy",
        3: "❤️ Love",
        4: "😢 Sadness"
    }

    return (
        emotion_map.get(pred, "Unknown"),
        round(confidence * 100, 2)
    )

# =====================================================
# SESSION
# =====================================================

if "result_df" not in st.session_state:
    st.session_state.result_df = None

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🧠 Emotion AI")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Analisis Satuan",
        "Bulk CSV"
    ]
)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("📊 Dashboard")

    total = 0
    positif = 0
    negatif = 0
    netral = 0

    if st.session_state.result_df is not None:

        df = st.session_state.result_df

        total = len(df)

        positif = len(
            df[df["Sentiment"]=="Positif"]
        )

        negatif = len(
            df[df["Sentiment"]=="Negatif"]
        )

        netral = len(
            df[df["Sentiment"]=="Netral"]
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total", total)
    c2.metric("Positif", positif)
    c3.metric("Negatif", negatif)
    c4.metric("Netral", netral)

    st.info(
        "Belum ada hasil Bulk CSV."
        if total == 0
        else "Data berhasil diproses."
    )

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

st.title("🔍 Analisis Sentimen & Emosi")

text = st.text_area(
    "Masukkan Ulasan",
    height=180,
    placeholder="Contoh: Aplikasi sangat membantu dan mudah digunakan"
)

if st.button("🚀 Analisis"):

    if not text.strip():

        st.warning(
            "Masukkan teks terlebih dahulu"
        )

    else:

        try:

            with st.spinner(
                "🧠 AI sedang menganalisis..."
            ):

                sentiment, sentiment_score = predict_sentiment(
                    text
                )

                emotion, emotion_score = predict_emotion(
                    text
                )

            st.markdown("## 📋 Hasil Analisis")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Sentimen",
                    sentiment
                )

            with c2:
                st.metric(
                    "Confidence",
                    f"{sentiment_score:.2f}%"
                )

            with c3:
                st.metric(
                    "Emosi",
                    emotion
                )

            with c4:
                st.metric(
                    "Confidence",
                    f"{emotion_score:.2f}%"
                )

            st.markdown("---")

            st.subheader("📈 Tingkat Keyakinan Model")

            st.write(
                f"Sentiment Confidence : {sentiment_score:.2f}%"
            )

            st.progress(
                sentiment_score / 100
            )

            st.write(
                f"Emotion Confidence : {emotion_score:.2f}%"
            )

            st.progress(
                emotion_score / 100
            )

        except Exception as e:

            st.error(
                f"Error : {e}"
            )
