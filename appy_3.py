import streamlit as st
import pandas as pd
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#020B1C;
}

[data-testid="stSidebar"]{
    background-color:#081224;
}

.metric-card{
    background:#0C1D38;
    padding:15px;
    border-radius:12px;
}

h1,h2,h3,h4,h5,h6{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "bulk_result" not in st.session_state:
    st.session_state.bulk_result = None

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource(show_spinner=False)
def load_sentiment_model():

    tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    model.eval()

    return tokenizer, model


@st.cache_resource(show_spinner=False)
def load_emotion_model():

    tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/emotion_model"
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/emotion_model"
    )

    model.eval()

    return tokenizer, model


# =====================================================
# PREDICT SENTIMENT
# =====================================================

def predict_sentiment(text):

    tokenizer, model = load_sentiment_model()

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(
        outputs.logits,
        dim=1
    ).item()

    label_map = {
        0: "Negatif",
        1: "Netral",
        2: "Positif"
    }

    return label_map.get(pred, "Unknown")


# =====================================================
# PREDICT EMOTION
# =====================================================

def predict_emotion(text):

    tokenizer, model = load_emotion_model()

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(
        outputs.logits,
        dim=1
    ).item()

    emotion_map = {
        0: "Anger",
        1: "Fear",
        2: "Happy",
        3: "Love",
        4: "Sadness"
    }

    return emotion_map.get(pred, "Unknown")


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

    if st.session_state.bulk_result is not None:

        df = st.session_state.bulk_result

        total = len(df)

        positif = len(
            df[df["Sentiment"] == "Positif"]
        )

        negatif = len(
            df[df["Sentiment"] == "Negatif"]
        )

        netral = len(
            df[df["Sentiment"] == "Netral"]
        )

    else:

        total = 0
        positif = 0
        negatif = 0
        netral = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("Positif", positif)
    col3.metric("Negatif", negatif)
    col4.metric("Netral", netral)

    st.info(
        "Belum ada hasil Bulk CSV. Silakan upload data terlebih dahulu."
        if total == 0
        else "Data Bulk CSV berhasil diproses."
    )

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    st.title("🔍 Analisis Satuan")

    text = st.text_area(
        "Masukkan Ulasan"
    )

    if st.button("Analisis"):

        if not text.strip():

            st.warning(
                "Masukkan teks terlebih dahulu"
            )

        else:

            try:

                with st.spinner(
                    "Memuat model..."
                ):

                    sentiment = predict_sentiment(
                        text
                    )

                    emotion = predict_emotion(
                        text
                    )

                c1, c2 = st.columns(2)

                with c1:
                    st.success(
                        f"Sentimen : {sentiment}"
                    )

                with c2:
                    st.info(
                        f"Emosi : {emotion}"
                    )

            except Exception as e:

                st.error(
                    f"Gagal memuat model : {e}"
                )

# =====================================================
# BULK CSV
# =====================================================

elif menu == "Bulk CSV":

    st.title("📂 Bulk CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(
                uploaded_file
            )

            st.write(
                "Preview Data"
            )

            st.dataframe(
                df.head()
            )

            text_column = st.selectbox(
                "Pilih Kolom Teks",
                df.columns
            )

            if st.button(
                "Proses Analisis"
            ):

                sentiments = []
                emotions = []

                progress = st.progress(
                    0
                )

                for i, text in enumerate(
                    df[text_column]
                ):

                    try:

                        sentiment = predict_sentiment(
                            text
                        )

                        emotion = predict_emotion(
                            text
                        )

                    except:

                        sentiment = "Error"
                        emotion = "Error"

                    sentiments.append(
                        sentiment
                    )

                    emotions.append(
                        emotion
                    )

                    progress.progress(
                        (i + 1)
                        / len(df)
                    )

                df["Sentiment"] = sentiments
                df["Emotion"] = emotions

                st.session_state.bulk_result = df

                st.success(
                    "Analisis selesai"
                )

                st.dataframe(
                    df.head()
                )

                csv = df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇ Download Hasil",
                    csv,
                    file_name="hasil_analisis.csv",
                    mime="text/csv"
                )

        except Exception as e:

            st.error(str(e))
