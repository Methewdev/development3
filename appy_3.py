import streamlit as st
import requests
import re

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
# HUGGINGFACE CONFIG
# =====================================================

API_URL = "https://api-inference.huggingface.co/models/envidevelopment/model3"

# =====================================================
# GANTI DENGAN TOKEN HUGGINGFACE ANDA
# =====================================================

HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxx"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

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
# QUERY MODEL
# =====================================================

def query_model(payload):

    try:

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        # =====================================================
        # STATUS CODE
        # =====================================================

        if response.status_code != 200:

            st.error(
                f"❌ API Error: {response.status_code}"
            )

            st.code(response.text)

            return None

        # =====================================================
        # EMPTY RESPONSE
        # =====================================================

        if response.text.strip() == "":

            st.error(
                "❌ Response kosong dari HuggingFace"
            )

            return None

        # =====================================================
        # CONVERT JSON
        # =====================================================

        try:

            result = response.json()

        except Exception:

            st.error(
                "❌ Response bukan JSON valid"
            )

            st.code(response.text)

            return None

        # =====================================================
        # HANDLE MODEL ERROR
        # =====================================================

        if isinstance(result, dict):

            if "error" in result:

                st.error(
                    f"❌ HuggingFace Error: {result['error']}"
                )

                return None

        return result

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timeout. Model mungkin masih loading."
        )

        return None

    except Exception as e:

        st.error(
            f"❌ Request Error: {str(e)}"
        )

        return None

# =====================================================
# PREDICTION
# =====================================================

def predict_emotion(text):

    cleaned = clean_text(text)

    output = query_model({
        "inputs": cleaned
    })

    # =====================================================
    # FAILED RESPONSE
    # =====================================================

    if output is None:

        return (
            "netral",
            0.0
        )

    try:

        prediction = output[0]

        # =====================================================
        # IF LIST
        # =====================================================

        if isinstance(prediction, list):

            prediction = prediction[0]

        label = prediction["label"]

        score = prediction["score"]

        # =====================================================
        # LABEL HANDLING
        # =====================================================

        if label in emotion_classes:

            emotion = label

        else:

            label_id = int(
                label.split("_")[-1]
            )

            emotion = emotion_classes[label_id]

        return (
            emotion,
            score
        )

    except Exception as e:

        st.error(
            "❌ Format output model tidak sesuai"
        )

        st.write(output)

        return (
            "netral",
            0.0
        )

# =====================================================
# SARCASM DETECTION
# =====================================================

def detect_sarcasm(text, emotion):

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
        "pending"
    ]

    pos_found = any(
        word in text for word in positive_words
    )

    neg_found = any(
        word in text for word in negative_words
    )

    negative_emotion = emotion in [
        "marah",
        "frustrasi"
    ]

    # =====================================================
    # IMPLICIT SARCASM
    # =====================================================

    if pos_found and neg_found and negative_emotion:

        return True

    return False

# =====================================================
# INPUT
# =====================================================

st.markdown("### ✍️ Masukkan Ulasan Nasabah")

text = st.text_area(
    "",
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
            "Menganalisis emosi..."
        ):

            emotion, confidence = predict_emotion(
                text
            )

            is_sarcasm = detect_sarcasm(
                text,
                emotion
            )

        style = emotion_styles[emotion]

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
        # CONFIDENCE
        # =====================================================

        st.metric(
            "🎯 Confidence Score",
            f"{confidence*100:.2f}%"
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
        # CLEANING RESULT
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

    "Login cepat dan aman"
]

for s in samples:

    st.code(s)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi & Sarkasme Mobile Banking | IndoBERT Transformer"
)
