import streamlit as st
import re
import torch

from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Analisis Emosi & Sarkasme",
    page_icon="📊",
    layout="centered"
)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<h1 style="
    text-align:center;
">
    📊 Analisis Emosi & Sarkasme Nasabah
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    text-align:center;
    font-size:18px;
    color:gray;
">
Prototype Analisis Emosi dan Sarkasme
berbasis IndoBERT Transformer
</p>
""", unsafe_allow_html=True)

# =====================================================
# MODEL
# =====================================================

MODEL_NAME = "envidevelopment/model3"

# =====================================================
# EMOTION LABELS
# =====================================================

emotion_classes = [
    "cemas",
    "frustrasi",
    "marah",
    "netral",
    "puas",
    "senang"
]

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME
    )

    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        truncation=True,
        max_length=128,
        device=-1
    )

    return classifier

# =====================================================
# LOAD MODEL UI
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
# PREDICT EMOTION
# =====================================================

def predict_emotion(text):

    cleaned = clean_text(text)

    try:

        result = classifier(cleaned)

        prediction = result[0]

        label = prediction["label"]

        score = prediction["score"]

        # ==============================
        # HANDLE LABEL
        # ==============================

        if label in emotion_classes:

            emotion = label

        else:

            try:

                label_id = int(
                    label.split("_")[-1]
                )

                emotion = emotion_classes[label_id]

            except:

                emotion = "netral"

        return emotion, score

    except Exception as e:

        st.error(
            f"❌ Error prediksi model: {e}"
        )

        return "netral", 0.0

# =====================================================
# SARCASM DETECTION
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

    positive = [
        "senang",
        "puas"
    ]

    negative = [
        "marah",
        "frustrasi",
        "cemas"
    ]

    if emotion in positive:

        return "Positif"

    elif emotion in negative:

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

        with st.spinner(
            "🔄 Sedang menganalisis..."
        ):

            emotion, confidence = predict_emotion(
                text
            )

            sentiment = detect_sentiment(
                emotion
            )

            is_sarcasm = detect_sarcasm(
                text
            )

        style = emotion_styles.get(
            emotion,
            emotion_styles["netral"]
        )

        # =====================================================
        # RESULT TITLE
        # =====================================================

        st.markdown("---")

        st.markdown("""
        <h2 style="
            text-align:center;
            margin-bottom:20px;
        ">
            📌 Hasil Analisis
        </h2>
        """, unsafe_allow_html=True)

        # =====================================================
        # EMOTION CARD
        # =====================================================

        st.markdown(
            f"""
            <div style="
                background-color:{style['color']};
                padding:30px;
                border-radius:20px;
                text-align:center;
                color:white;
                margin-bottom:25px;
            ">

                <h1>
                    {style['emoji']} {emotion.upper()}
                </h1>

                <p style="
                    font-size:20px;
                ">
                    {style['message']}
                </p>

            </div>
            """,
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

        st.markdown("### 🧠 Hasil Deteksi Sarkasme")

        if is_sarcasm:

            st.markdown(
                """
                <div style="
                    background-color:#E53935;
                    padding:18px;
                    border-radius:12px;
                    color:white;
                    text-align:center;
                    font-size:22px;
                    font-weight:bold;
                ">
                    ⚠️ Sarkasme Terdeteksi
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div style="
                    background-color:#43A047;
                    padding:18px;
                    border-radius:12px;
                    color:white;
                    text-align:center;
                    font-size:22px;
                    font-weight:bold;
                ">
                    ✅ Tidak Mengandung Sarkasme
                </div>
                """,
                unsafe_allow_html=True
            )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking | IndoBERT Transformer"
)
