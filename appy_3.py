import streamlit as st
import re
from transformers import pipeline

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Analisis Emosi & Sarkasme",
    page_icon="📊",
    layout="centered"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 18px;
    font-weight: bold;
}

.stTextArea textarea {
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Analisis Emosi & Sarkasme Nasabah")

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

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

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

    pos_found = any(
        word in text
        for word in positive_words
    )

    neg_found = any(
        word in text
        for word in negative_words
    )

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
# INPUT
# =====================================================

st.subheader("✍️ Masukkan Ulasan Nasabah")

text = st.text_area(
    "",
    height=180,
    placeholder="Contoh: Bagus banget aplikasinya transfer gagal terus"
)

# =====================================================
# BUTTON
# =====================================================

if st.button("🔍 Analisis Sekarang"):

    if text.strip() == "":

        st.warning(
            "⚠️ Masukkan ulasan terlebih dahulu"
        )

    else:

        with st.spinner("🔄 Sedang menganalisis..."):

            cleaned = clean_text(text)

            result = classifier(cleaned)

            raw_label = result[0]["label"]

            confidence = result[0]["score"]

            label = label_mapping.get(
                raw_label,
                "netral"
            )

            style = emotion_styles[label]

            sentiment = detect_sentiment(label)

            is_sarcasm = detect_sarcasm(text)

        # =====================================================
        # HASIL ANALISIS
        # =====================================================

        st.markdown("---")

        st.subheader("📌 Hasil Analisis")

        st.info(
            f"{style['emoji']} EMOSI : {label.upper()}"
        )

        st.write(style["message"])

        # =====================================================
        # METRICS
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🎯 Confidence",
                f"{confidence*100:.2f}%"
            )

        with col2:

            st.metric(
                "💬 Sentimen",
                sentiment
            )

        # =====================================================
        # SARCASM
        # =====================================================

        st.subheader(
            "🧠 Hasil Deteksi Sarkasme"
        )

        if is_sarcasm:

            st.error(
                "⚠️ Sarkasme Terdeteksi"
            )

        else:

            st.success(
                "✅ Tidak Mengandung Sarkasme"
            )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking"
)
