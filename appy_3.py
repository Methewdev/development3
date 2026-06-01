import streamlit as st
import pandas as pd
import plotly.express as px
import torch
from datetime import datetime

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from streamlit_option_menu import option_menu

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="Sentiment & Emotion Analysis",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#0E1117;
}

[data-testid="stSidebar"]{
    background-color:#1E1E1E;
}

div[data-testid="metric-container"]{
    background:#262730;
    border:1px solid #404040;
    padding:15px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD MODEL
# ==========================================================

@st.cache_resource
def load_sentiment_model():

    return pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier",
        truncation=True
    )


@st.cache_resource
def load_emotion_model():

    EMOTION_MODEL_PATH = "models/emotion_model"

    tokenizer = AutoTokenizer.from_pretrained(
        EMOTION_MODEL_PATH
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        EMOTION_MODEL_PATH
    )

    return tokenizer, model


sentiment_model = load_sentiment_model()

emotion_ready = True

try:

    tokenizer, emotion_model = load_emotion_model()

except:

    emotion_ready = False


emotion_labels = {
    0: "anger",
    1: "fear",
    2: "happy",
    3: "love",
    4: "sadness"
}

# ==========================================================
# SESSION STATE
# ==========================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================================
# FUNCTION
# ==========================================================

def predict_sentiment(text):

    result = sentiment_model(text)[0]

    return (
        result["label"],
        float(result["score"])
    )


def predict_emotion(text):

    if not emotion_ready:
        return "unknown"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    )

    with torch.no_grad():

        outputs = emotion_model(**inputs)

        prediction = torch.argmax(
            outputs.logits,
            dim=1
        ).item()

    return emotion_labels[prediction]


def save_history(text, sentiment, emotion, score):

    st.session_state.history.append({
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text,
        "sentiment": sentiment,
        "emotion": emotion,
        "score": score
    })


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2103/2103832.png",
        width=80
    )

    selected = option_menu(
        menu_title="MENU",
        options=[
            "Dashboard",
            "Analisis Satuan",
            "Bulk CSV",
            "Statistik",
            "Riwayat"
        ],
        icons=[
            "house-fill",
            "chat-dots-fill",
            "file-earmark-spreadsheet-fill",
            "bar-chart-fill",
            "clock-history"
        ],
        default_index=0
    )

# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "Dashboard":

    st.title("📊 Dashboard")

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
                history["sentiment"].str.lower()
                == "positive"
            ]
        )

        negative = len(
            history[
                history["sentiment"].str.lower()
                == "negative"
            ]
        )

        neutral = len(
            history[
                history["sentiment"].str.lower()
                == "neutral"
            ]
        )

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Analisis", total)
    c2.metric("😊 Positif", positive)
    c3.metric("😡 Negatif", negative)
    c4.metric("😐 Netral", neutral)

    st.divider()

    text = st.text_area(
        "Masukkan Ulasan",
        height=200
    )

    col1,col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Analisis Sekarang",
            use_container_width=True
        ):

            if text:

                sentiment, score = predict_sentiment(text)

                emotion = predict_emotion(text)

                save_history(
                    text,
                    sentiment,
                    emotion,
                    score
                )

                st.success("Analisis berhasil")

    with col2:

        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True
        ):

            st.session_state.history = []

            st.rerun()

# ==========================================================
# ANALISIS SATUAN
# ==========================================================

elif selected == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    text = st.text_area(
        "Masukkan Teks",
        height=250
    )

    if st.button("Analisis"):

        if text:

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
                round(score,4)
            )

# ==========================================================
# BULK CSV
# ==========================================================

elif selected == "Bulk CSV":

    st.title("📂 Bulk CSV Analysis")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.dataframe(df.head())

        selected_col = st.selectbox(
            "Pilih Kolom Teks",
            df.columns
        )

        if st.button("🚀 Proses Analisis"):

            sentiments = []
            emotions = []
            scores = []

            progress = st.progress(0)

            total_rows = len(df)

            for idx, text in enumerate(
                df[selected_col]
            ):

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
                    (idx + 1) / total_rows
                )

            df["sentiment"] = sentiments
            df["emotion"] = emotions
            df["score"] = scores

            st.success("Selesai")

            st.dataframe(df)

            csv = df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇ Download Hasil",
                csv,
                "hasil_analisis.csv",
                "text/csv"
            )

# ==========================================================
# STATISTIK
# ==========================================================

elif selected == "Statistik":

    st.title("📈 Statistik")

    if len(st.session_state.history) == 0:

        st.warning(
            "Belum ada data."
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        col1,col2 = st.columns(2)

        with col1:

            fig1 = px.pie(
                df,
                names="sentiment",
                title="Distribusi Sentimen",
                hole=0.4
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

# ==========================================================
# RIWAYAT
# ==========================================================

elif selected == "Riwayat":

    st.title("🕒 Riwayat Analisis")

    if len(st.session_state.history) == 0:

        st.warning(
            "Belum ada riwayat analisis"
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download Riwayat",
            csv,
            "riwayat.csv",
            "text/csv"
        )

        if st.button(
            "🗑 Hapus Riwayat"
        ):

            st.session_state.history = []

            st.rerun()
