import streamlit as st
import pandas as pd
import plotly.express as px
import torch
from datetime import datetime
from pathlib import Path

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#030B1B;
}

[data-testid="stSidebar"]{
    background-color:#111827;
}

div[data-testid="metric-container"]{
    background:#132447;
    border-radius:15px;
    padding:15px;
    border:1px solid #274472;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:50px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD SENTIMENT MODEL
# =====================================================

@st.cache_resource
def load_sentiment_model():

    return pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier",
        truncation=True
    )

# =====================================================
# LOAD EMOTION MODEL
# =====================================================

@st.cache_resource
def load_emotion_model():

    MODEL_PATH = "models/emotion_model"

    if not Path(MODEL_PATH).exists():
        return None, None

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH
    )

    return tokenizer, model


sentiment_model = load_sentiment_model()

tokenizer, emotion_model = load_emotion_model()

emotion_ready = emotion_model is not None

emotion_labels = {
    0:"anger",
    1:"fear",
    2:"happy",
    3:"love",
    4:"sadness"
}

# =====================================================
# SESSION
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# FUNCTIONS
# =====================================================

def predict_sentiment(text):

    result = sentiment_model(text)[0]

    return (
        result["label"],
        float(result["score"])
    )


def predict_emotion(text):

    if not emotion_ready:
        return "Model Belum Tersedia"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():

        outputs = emotion_model(**inputs)

        pred = torch.argmax(
            outputs.logits,
            dim=1
        ).item()

    return emotion_labels.get(
        pred,
        "unknown"
    )


def save_history(text,sentiment,emotion,score):

    st.session_state.history.append({
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
        "sentiment": sentiment,
        "emotion": emotion,
        "score": score
    })

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🧠 Emotion AI")

    menu = st.radio(
        "MENU",
        [
            "Dashboard",
            "Analisis Satuan",
            "Bulk CSV",
            "Statistik",
            "Riwayat"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("📊 Dashboard Analisis Emosi")

    history = pd.DataFrame(
        st.session_state.history
    )

    total = len(history)

    positive = 0
    negative = 0
    neutral = 0

    if total > 0:

        positive = len(
            history[
                history["sentiment"].str.lower()=="positive"
            ]
        )

        negative = len(
            history[
                history["sentiment"].str.lower()=="negative"
            ]
        )

        neutral = len(
            history[
                history["sentiment"].str.lower()=="neutral"
            ]
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total",total)
    c2.metric("😊 Positif",positive)
    c3.metric("😡 Negatif",negative)
    c4.metric("😐 Netral",neutral)

    st.divider()

    col1,col2 = st.columns([2,1])

    with col1:

        text = st.text_area(
            "Masukkan Ulasan",
            height=250
        )

        if st.button("🔍 Analisis Sekarang"):

            if text.strip():

                with st.spinner("Menganalisis..."):

                    sentiment, score = predict_sentiment(text)

                    emotion = predict_emotion(text)

                    save_history(
                        text,
                        sentiment,
                        emotion,
                        score
                    )

                st.success("Analisis selesai")

    with col2:

        st.subheader("📌 Hasil")

        if len(st.session_state.history):

            last = st.session_state.history[-1]

            st.metric(
                "Sentimen",
                last["sentiment"]
            )

            st.metric(
                "Emosi",
                last["emotion"]
            )

            st.metric(
                "Confidence",
                f"{last['score']*100:.2f}%"
            )

    st.divider()

    if st.button("🔄 Refresh Dashboard"):

        st.session_state.history = []

        st.rerun()

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    text = st.text_area(
        "Masukkan Teks",
        height=250
    )

    if st.button("Analisis"):

        if text.strip():

            sentiment, score = predict_sentiment(text)

            emotion = predict_emotion(text)

            save_history(
                text,
                sentiment,
                emotion,
                score
            )

            c1,c2,c3 = st.columns(3)

            c1.metric(
                "Sentimen",
                sentiment
            )

            c2.metric(
                "Emosi",
                emotion
            )

            c3.metric(
                "Confidence",
                f"{score*100:.2f}%"
            )

# =====================================================
# BULK CSV
# =====================================================

elif menu == "Bulk CSV":

    st.title("📂 Bulk CSV")

    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded:

        df = pd.read_csv(uploaded)

        st.dataframe(df.head())

        text_col = st.selectbox(
            "Pilih Kolom Teks",
            df.columns
        )

        if st.button("🚀 Proses"):

            sentiments = []
            emotions = []
            scores = []

            progress = st.progress(0)

            total_rows = len(df)

            for i,text in enumerate(df[text_col]):

                sentiment, score = predict_sentiment(
                    str(text)
                )

                emotion = predict_emotion(
                    str(text)
                )

                sentiments.append(sentiment)
                emotions.append(emotion)
                scores.append(score)

                progress.progress(
                    (i+1)/total_rows
                )

            df["sentiment"] = sentiments
            df["emotion"] = emotions
            df["score"] = scores

            st.success("Selesai")

            st.dataframe(df)

            st.download_button(
                "⬇ Download CSV",
                df.to_csv(index=False),
                "hasil_analisis.csv",
                "text/csv"
            )

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

    st.title("📈 Statistik")

    if len(st.session_state.history)==0:

        st.warning("Belum ada data")

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        col1,col2 = st.columns(2)

        with col1:

            fig1 = px.pie(
                df,
                names="sentiment",
                hole=0.4,
                title="Distribusi Sentimen"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with col2:

            fig2 = px.histogram(
                df,
                x="emotion",
                title="Distribusi Emosi"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "Riwayat":

    st.title("🕒 Riwayat")

    if len(st.session_state.history)==0:

        st.warning(
            "Belum ada riwayat"
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "⬇ Download Riwayat",
            df.to_csv(index=False),
            "riwayat.csv",
            "text/csv"
        )

        if st.button("🗑 Hapus Riwayat"):

            st.session_state.history = []

            st.rerun()
