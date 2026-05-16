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

.main {
    background-color: #0E1117;
}

.stTextArea textarea {
    font-size: 18px;
    border-radius: 12px;
}

.stButton button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    border-radius: 12px;
    background-color: #03A9F4;
    color: white;
    border: none;
}

.stButton button:hover {
    background-color: #0288D1;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 style='text-align:center;color:white;'>
📊 Analisis Emosi & Sarkasme Nasabah
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center;font-size:18px;color:gray;'>
Prototype Analisis Emosi berbasis IndoBERT Transformer
</p>
""", unsafe_allow_html=True)

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

with st.spinner("🔄 Loading IndoBERT Model..."):

    try:

        classifier = load_model()

        st.success("✅ Model berhasil dimuat")

    except Exception as e:

        st.error("❌ Gagal memuat model")

        st.code(str(e))

        st.stop()

# =====================================================
# EMOTION STYLE
# =====================================================

emotion_styles = {

    "marah": {
        "emoji": "😡",
        "color": "#E53935",
        "message": "Nasabah mengalami emosi marah"
    },

    "frustrasi": {
        "emoji": "😤",
        "color": "#FB8C00",
        "message": "Nasabah menunjukkan frustrasi"
    },

    "cemas": {
        "emoji": "😰",
        "color": "#8E24AA",
        "message": "Nasabah merasa cemas"
    },

    "senang": {
        "emoji": "😊",
        "color": "#43A047",
        "message": "Nasabah merasa senang"
    },

    "puas": {
        "emoji": "😌",
        "color": "#039BE5",
        "message": "Nasabah merasa puas"
    },

    "netral": {
        "emoji": "😐",
        "color": "#546E7A",
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
        "cepat",
        "modern",
        "canggih"
    ]

    negative_words = [
        "gagal",
        "error",
        "maintenance",
        "lemot",
        "pending",
        "gangguan",
        "timeout",
        "saldo hilang"
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
# SENTIMENT
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

st.markdown("### ✍️ Masukkan Ulasan Nasabah")

text = st.text_area(
    "",
    height=170,
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
        # RESULT
        # =====================================================

        st.markdown("---")

        html_card = f"""
        <div style="
            background-color:{style['color']};
            padding:35px;
            border-radius:20px;
            text-align:center;
            color:white;
            margin-top:20px;
            margin-bottom:25px;
        ">

            <h1 style="color:white;">
                {style['emoji']} {label.upper()}
            </h1>

            <p style="
                font-size:20px;
                color:white;
            ">
                {style['message']}
            </p>

        </div>
        """

        st.markdown(
            html_card,
            unsafe_allow_html=True
        )

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

        st.markdown("### 🧠 Hasil Deteksi Sarkasme")

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
