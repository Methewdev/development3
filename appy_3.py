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

st.title("📊 Analisis Emosi & Sarkasme Nasabah")

st.markdown("""
Prototype Analisis Emosi dan Sarkasme  
berbasis IndoBERT Transformer
""")

# =====================================================
# LOAD MODEL HUGGINGFACE
# =====================================================

MODEL_NAME = "envidevelopment/model3"

# =====================================================
# EMOTION LABEL
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
        device=0 if torch.cuda.is_available() else -1
    )

    return classifier

# =====================================================
# MODEL LOADING
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
        "color": "#FF4B4B",
        "message": "Nasabah mengalami emosi marah"
    },

    "frustrasi": {
        "emoji": "😤",
        "color": "#FF9800",
        "message": "Nasabah menunjukkan frustrasi"
    },

    "cemas": {
        "emoji": "😰",
        "color": "#8E44AD",
        "message": "Nasabah merasa cemas"
    },

    "senang": {
        "emoji": "😊",
        "color": "#00C853",
        "message": "Nasabah merasa senang"
    },

    "puas": {
        "emoji": "😌",
        "color": "#03A9F4",
        "message": "Nasabah merasa puas"
    },

    "netral": {
        "emoji": "😐",
        "color": "#607D8B",
        "message": "Nasabah menunjukkan emosi netral"
    }
}

# =====================================================
# CLEANING TEXT
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

        # =====================================================
        # HANDLE LABEL
        # =====================================================

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

        return (
            emotion,
            score
        )

    except Exception as e:

        st.error(
            f"❌ Error prediksi model: {e}"
        )

        return (
            "netral",
            0.0
        )

# =====================================================
# HYBRID SARCASM DETECTION
# =====================================================

def detect_sarcasm(text):

    text = clean_text(text)

    # =====================================================
    # POSITIVE WORDS
    # =====================================================

    positive_words = [
        "bagus",
        "mantap",
        "keren",
        "hebat",
        "cepat",
        "terima kasih",
        "luar biasa",
        "modern",
        "canggih",
        "top"
    ]

    # =====================================================
    # NEGATIVE WORDS
    # =====================================================

    negative_words = [
        "gagal",
        "error",
        "maintenance",
        "lemot",
        "pending",
        "gangguan",
        "force close",
        "tidak bisa",
        "lambat",
        "timeout",
        "loading terus",
        "saldo hilang"
    ]

    pos_found = any(
        word in text for word in positive_words
    )

    neg_found = any(
        word in text for word in negative_words
    )

    # =====================================================
    # CONTRADICTION DETECTION
    # =====================================================

    if pos_found and neg_found:

        return True

    # =====================================================
    # SARCASM PATTERN
    # =====================================================

    sarcasm_patterns = [

        r"bagus.*gagal",

        r"mantap.*error",

        r"keren.*maintenance",

        r"terima kasih.*error",

        r"cepat.*lemot",

        r"modern.*lemot",

        r"canggih.*gangguan"
    ]

    for pattern in sarcasm_patterns:

        if re.search(pattern, text):

            return True

    return False

# =====================================================
# SENTIMENT DETECTION
# =====================================================

def detect_sentiment(emotion):

    positive_emotions = [
        "senang",
        "puas"
    ]

    negative_emotions = [
        "marah",
        "frustrasi",
        "cemas"
    ]

    if emotion in positive_emotions:

        return "Positif"

    elif emotion in negative_emotions:

        return "Negatif"

    else:

        return "Netral"

# =====================================================
# INPUT
# =====================================================

st.markdown("### ✍️ Masukkan Ulasan Nasabah")

text = st.text_area(
    "",
    height=150,
    placeholder="Contoh: Bagus banget aplikasinya transfer gagal terus..."
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
        # RESULT HEADER
        # =====================================================

        st.markdown("---")

        st.markdown("## 📌 Hasil Analisis")

        # =====================================================
        # EMOTION CARD
        # =====================================================

        st.markdown(
            f"""
            <div style="
                background-color:{style['color']};
                padding:25px;
                border-radius:15px;
                text-align:center;
                color:white;
                margin-bottom:20px;
            ">

                <h1>
                    {style['emoji']} {emotion.upper()}
                </h1>

                <p style="
                    font-size:18px;
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
                    background-color:#FF5252;
                    padding:15px;
                    border-radius:10px;
                    color:white;
                    text-align:center;
                    font-size:20px;
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
                    background-color:#00C853;
                    padding:15px;
                    border-radius:10px;
                    color:white;
                    text-align:center;
                    font-size:20px;
                    font-weight:bold;
                ">
                    ✅ Tidak Mengandung Sarkasme
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # CLEANED TEXT
        # =====================================================

        st.markdown("### 🧹 Hasil Cleaning Text")

        st.code(
            clean_text(text)
        )

# =====================================================
# SAMPLE TEXT
# =====================================================

st.markdown("---")

st.subheader("📌 Contoh Ulasan")

samples = [

    "Bagus banget aplikasinya transfer gagal terus",

    "Mantap maintenance tiap malam",

    "Aplikasi sangat membantu transaksi",

    "Saya takut saldo hilang",

    "Login cepat dan aman",

    "Terima kasih Livin error terus",

    "Keren banget maintenance tiap gajian",

    "Aplikasi modern dengan nuansa warnet tahun 2000-an",

    "Transfer cepat sekali sampai besok belum masuk"
]

for s in samples:

    st.code(s)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking | IndoBERT Transformer"
)
