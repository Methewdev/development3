import streamlit as st
import pandas as pd
import plotly.express as px
import torch

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from streamlit_option_menu import option_menu

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#050d1f;
}

.metric-card{
    background:#132447;
    padding:20px;
    border-radius:15px;
    border:1px solid #274472;
}

.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_sentiment_model():

    model = pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier",
        truncation=True
    )

    return model


@st.cache_resource
def load_emotion_model():

    MODEL_PATH = "models/emotion_model"

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH
    )

    return tokenizer, model


sentiment_model = load_sentiment_model()

try:

    tokenizer, emotion_model = load_emotion_model()

    emotion_ready = True

except:

    emotion_ready = False


emotion_labels = {
    0:"Marah",
    1:"Takut",
    2:"Bahagia",
    3:"Suka",
    4:"Sedih"
}

# =====================================================
# PREDICTION
# =====================================================

def predict_sentiment(text):

    result = sentiment_model(text)[0]

    return (
        result["label"],
        float(result["score"])
    )


def predict_emotion(text):

    if not emotion_ready:
        return "Model belum tersedia"

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

    return emotion_labels[pred]

# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🧠 Emotion AI")
    st.caption("Dashboard Analisis Emosi & Sentimen")

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
            "house",
            "chat-dots",
            "file-earmark-spreadsheet",
            "bar-chart",
            "clock-history"
        ],
        default_index=0
    )

# =====================================================
# DASHBOARD
# =====================================================

if selected == "Dashboard":

    st.title("📊 Dashboard Analisis Emosi")

    total = len(st.session_state.history)

    positif = len([
        x for x in st.session_state.history
        if x["sentiment"].lower() == "positive"
    ])

    negatif = len([
        x for x in st.session_state.history
        if x["sentiment"].lower() == "negative"
    ])

    netral = len([
        x for x in st.session_state.history
        if x["sentiment"].lower() == "neutral"
    ])

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total", total)
    c2.metric("😊 Positif", positif)
    c3.metric("😡 Negatif", negatif)
    c4.metric("😐 Netral", netral)

    st.divider()

    col1,col2 = st.columns([3,1])

    with col1:

        text = st.text_area(
            "✍ Input Ulasan",
            height=250,
            placeholder="Masukkan ulasan pengguna..."
        )

        if st.button(
            "🔍 Analisis Sekarang",
            use_container_width=True
        ):

            if text.strip() != "":

                sentiment, score = predict_sentiment(text)

                emotion = predict_emotion(text)

                result = {
                    "text": text,
                    "sentiment": sentiment,
                    "emotion": emotion,
                    "score": score
                }

                st.session_state.history.append(result)

                st.success("Analisis berhasil")

    with col2:

        st.subheader("📌 Hasil")

        if len(st.session_state.history) > 0:

            last = st.session_state.history[-1]

            st.info(f"""
Sentimen : {last['sentiment']}

Emosi : {last['emotion']}

Confidence : {round(last['score'],4)}
""")

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):
        st.session_state.history = []
        st.rerun()

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif selected == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    text = st.text_area(
        "Masukkan Ulasan",
        height=200
    )

    if st.button("Analisis"):

        if text.strip():

            sentiment, score = predict_sentiment(text)

            emotion = predict_emotion(text)

            st.success("Analisis Selesai")

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

# =====================================================
# BULK CSV
# =====================================================

elif selected == "Bulk CSV":

    st.title("📂 Analisis Bulk CSV")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.write("Preview Data")

        st.dataframe(df.head())

        col_name = st.selectbox(
            "Pilih Kolom Ulasan",
            df.columns
        )

        if st.button("🚀 Proses Analisis"):

            sentiments = []
            emotions = []
            scores = []

            progress = st.progress(0)

            total_rows = len(df)

            for idx,text in enumerate(df[col_name]):

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
                    (idx+1)/total_rows
                )

            df["sentiment"] = sentiments
            df["emotion"] = emotions
            df["score"] = scores

            st.success("Selesai")

            st.dataframe(df)

            csv = df.to_csv(
                index=False
            ).encode()

            st.download_button(
                "⬇ Download Hasil",
                csv,
                file_name="hasil_analisis.csv",
                mime="text/csv"
            )

# =====================================================
# STATISTIK
# =====================================================

elif selected == "Statistik":

    st.title("📈 Statistik")

    if len(st.session_state.history) == 0:

        st.warning(
            "Belum ada data analisis."
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

elif selected == "Riwayat":

    st.title("🕒 Riwayat Analisis")

    if len(st.session_state.history) == 0:

        st.warning(
            "Belum ada riwayat."
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
        ).encode()

        st.download_button(
            "⬇ Download Riwayat",
            csv,
            file_name="riwayat.csv",
            mime="text/csv"
        )

        if st.button(
            "🗑 Hapus Riwayat"
        ):
            st.session_state.history = []
            st.rerun()
