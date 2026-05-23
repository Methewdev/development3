import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
from transformers import pipeline

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dashboard Analisis Emosi",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.title("📊 Dashboard Analisis Emosi & Sarkasme")

st.caption(
    "Prototype Analisis Emosi berbasis IndoBERT Transformer"
)

# =====================================================
# MODEL
# =====================================================

MODEL_NAME = "envidevelopment/model3"

# =====================================================
# LABEL MAPPING
# =====================================================

label_mapping = {
    "LABEL_0": "cemas",
    "LABEL_1": "frustrasi",
    "LABEL_2": "marah",
    "LABEL_3": "netral",
    "LABEL_4": "puas",
    "LABEL_5": "senang"
}

# =====================================================
# EMOTION STYLE
# =====================================================

emotion_styles = {

    "marah": {
        "emoji": "😡",
        "message": "Nasabah mengalami emosi marah"
    },

    "frustrasi": {
        "emoji": "😤",
        "message": "Nasabah menunjukkan frustrasi"
    },

    "cemas": {
        "emoji": "😰",
        "message": "Nasabah merasa cemas"
    },

    "senang": {
        "emoji": "😊",
        "message": "Nasabah merasa senang"
    },

    "puas": {
        "emoji": "😌",
        "message": "Nasabah merasa puas"
    },

    "netral": {
        "emoji": "😐",
        "message": "Nasabah menunjukkan emosi netral"
    }
}

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():

    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME
    )

    return classifier

# =====================================================
# LOAD MODEL
# =====================================================

with st.spinner("🔄 Loading Model..."):

    try:

        classifier = load_model()

        st.success("✅ Model berhasil dimuat")

    except Exception as e:

        st.error("❌ Gagal memuat model")
        st.error(str(e))
        st.stop()

# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"@\w+", "", text)

    text = re.sub(
        r"[^a-zA-Z0-9\s!?]",
        " ",
        text
    )

    text = re.sub(r"\s+", " ", text).strip()

    return text

# =====================================================
# DETECT SARCASM
# =====================================================

def detect_sarcasm(text):

    text = clean_text(text)

    positive_words = [
        "bagus",
        "mantap",
        "keren",
        "hebat",
        "cepat"
    ]

    negative_words = [
        "gagal",
        "error",
        "maintenance",
        "lemot",
        "pending",
        "gangguan"
    ]

    pos_found = any(word in text for word in positive_words)

    neg_found = any(word in text for word in negative_words)

    return pos_found and neg_found

# =====================================================
# DETECT SENTIMENT
# =====================================================

def detect_sentiment(emotion):

    if emotion in ["senang", "puas"]:
        return "Positif"

    elif emotion in ["marah", "frustrasi", "cemas"]:
        return "Negatif"

    return "Netral"

# =====================================================
# ANALYZE FUNCTION
# =====================================================

def analyze_text(text):

    cleaned = clean_text(text)

    result = classifier(cleaned)

    raw_label = result[0]["label"]

    confidence = result[0]["score"]

    emotion = label_mapping.get(raw_label, "netral")

    sentiment = detect_sentiment(emotion)

    sarcasm = detect_sarcasm(text)

    return {
        "text": text,
        "emotion": emotion,
        "confidence": round(confidence * 100, 2),
        "sentiment": sentiment,
        "sarcasm": sarcasm
    }

# =====================================================
# MENU
# =====================================================

menu = st.sidebar.radio(
    "📌 Pilih Mode",
    [
        "Analisis Satuan",
        "Analisis Bulk CSV"
    ]
)

# =====================================================
# SINGLE ANALYSIS
# =====================================================

if menu == "Analisis Satuan":

    st.subheader("✍️ Input Ulasan")

    text = st.text_area(
        "",
        height=200,
        placeholder="Contoh: Bagus banget aplikasinya transfer gagal terus"
    )

    if st.button("🔍 Analisis Sekarang"):

        if text.strip() == "":

            st.warning("⚠️ Masukkan ulasan terlebih dahulu")

        else:

            with st.spinner("🔄 Sedang menganalisis..."):

                result = analyze_text(text)

            emotion = result["emotion"]

            style = emotion_styles[emotion]

            st.markdown("---")

            st.subheader("📌 Hasil Analisis")

            st.success(
                f"{style['emoji']} Emosi : {emotion.upper()}"
            )

            st.write(style["message"])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🎯 Confidence",
                    f"{result['confidence']}%"
                )

            with col2:
                st.metric(
                    "💬 Sentimen",
                    result["sentiment"]
                )

            with col3:
                st.metric(
                    "🧠 Sarkasme",
                    "Ya" if result["sarcasm"] else "Tidak"
                )

# =====================================================
# BULK ANALYSIS
# =====================================================

elif menu == "Analisis Bulk CSV":

    st.subheader("📂 Upload CSV")

    uploaded_file = st.file_uploader(
        "Upload file CSV",
        type=["csv"]
    )

    st.info(
        "CSV harus memiliki kolom bernama: text"
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.subheader("📄 Preview Data")

        st.dataframe(df.head())

        if st.button("🚀 Proses Bulk Analisis"):

            results = []

            progress = st.progress(0)

            total = len(df)

            for i, row in enumerate(df.itertuples()):

                text = str(row.text)

                result = analyze_text(text)

                results.append(result)

                progress.progress((i + 1) / total)

            result_df = pd.DataFrame(results)

            st.success("✅ Analisis selesai")

            # =====================================================
            # DASHBOARD METRICS
            # =====================================================

            st.subheader("📊 Dashboard Statistik")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Data",
                    len(result_df)
                )

            with col2:
                st.metric(
                    "Positif",
                    len(
                        result_df[
                            result_df["sentiment"] == "Positif"
                        ]
                    )
                )

            with col3:
                st.metric(
                    "Negatif",
                    len(
                        result_df[
                            result_df["sentiment"] == "Negatif"
                        ]
                    )
                )

            with col4:
                st.metric(
                    "Sarkasme",
                    len(
                        result_df[
                            result_df["sarcasm"] == True
                        ]
                    )
                )

            # =====================================================
            # CHART
            # =====================================================

            st.subheader("📈 Distribusi Emosi")

            emotion_counts = result_df["emotion"].value_counts()

            fig, ax = plt.subplots(figsize=(8, 5))

            emotion_counts.plot(
                kind="bar",
                ax=ax
            )

            plt.xticks(rotation=0)

            st.pyplot(fig)

            # =====================================================
            # TABLE RESULT
            # =====================================================

            st.subheader("📋 Hasil Lengkap")

            st.dataframe(
                result_df,
                use_container_width=True
            )

            # =====================================================
            # DOWNLOAD
            # =====================================================

            csv = result_df.to_csv(index=False)

            st.download_button(
                label="⬇️ Download Hasil CSV",
                data=csv,
                file_name="hasil_analisis.csv",
                mime="text/csv"
            )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking"
)
