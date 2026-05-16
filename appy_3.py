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

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

.stTextArea textarea {
    font-size: 18px !important;
    border-radius: 15px !important;
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    border: none;
    background-color: #03A9F4;
    color: white;
    font-size: 18px;
    font-weight: bold;
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
<h1 style="
    text-align:center;
    color:white;
">
📊 Analisis Emosi & Sarkasme Nasabah
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
">
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

        st.error(str(e))

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
        "saldo hilang",
        "loading terus"
    ]

    pos_found = any(
        word in text
        for word in positive_words
    )

    neg_found = any(
        word in text
        for word in negative_words
    )

    if pos_found and neg_found:
        return True

    sarcasm_patterns = [

        r"bagus.*gagal",

        r"mantap.*error",

        r"keren.*maintenance",

        r"cepat.*lemot",

        r"modern.*lemot",

        r"canggih.*gangguan"
    ]

    for pattern in sarcasm_patterns:

        if re.search(pattern, text):

            return True

    return False

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

st.markdown("""
<h3 style="color:white;">
✍️ Masukkan Ulasan Nasabah
</h3>
""", unsafe_allow_html=True)

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
        # RESULT TITLE
        # =====================================================

        st.markdown("---")

        st.markdown("""
        <h2 style="
            text-align:center;
            color:white;
        ">
            📌 Hasil Analisis
        </h2>
        """, unsafe_allow_html=True)

        # =====================================================
        # EMOTION CARD
        # =====================================================

        card_html = f"""
        <div style="
            background-color:{style['color']};
            padding:35px;
            border-radius:25px;
            text-align:center;
            margin-top:20px;
            margin-bottom:25px;
            color:white;
        ">

            <div style="
                font-size:60px;
                margin-bottom:10px;
            ">
                {style['emoji']}
            </div>

            <div style="
                font-size:40px;
                font-weight:bold;
                margin-bottom:10px;
                color:white;
            ">
                {label.upper()}
            </div>

            <div style="
                font-size:20px;
                color:white;
            ">
                {style['message']}
            </div>

        </div>
        """

        st.markdown(
            card_html,
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
        # SARCASM RESULT
        # =====================================================

        st.markdown("""
        <h3 style="color:white;">
        🧠 Hasil Deteksi Sarkasme
        </h3>
        """, unsafe_allow_html=True)

        if is_sarcasm:

            sarcasm_html = """
            <div style="
                background-color:#E53935;
                padding:20px;
                border-radius:15px;
                color:white;
                text-align:center;
                font-size:24px;
                font-weight:bold;
                margin-top:10px;
            ">
                ⚠️ Sarkasme Terdeteksi
            </div>
            """

        else:

            sarcasm_html = """
            <div style="
                background-color:#43A047;
                padding:20px;
                border-radius:15px;
                color:white;
                text-align:center;
                font-size:24px;
                font-weight:bold;
                margin-top:10px;
            ">
                ✅ Tidak Mengandung Sarkasme
            </div>
            """

        st.markdown(
            sarcasm_html,
            unsafe_allow_html=True
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<p style="
    text-align:center;
    color:gray;
">
Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking
</p>
""", unsafe_allow_html=True)
