import streamlit as st
import re

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Analisis Emosi & Sarkasme Livin",
    page_icon="📊",
    layout="centered"
)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Analisis Emosi & Sarkasme Nasabah Livin")

st.markdown("""
Prototype Analisis Emosi dan Sarkasme  
berbasis NLP sesuai proposal tesis
""")

# =====================================================
# CLEANING
# =====================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"[^a-zA-Z0-9\s!?]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

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
        "cepat"
    ]

    negative_words = [
        "gagal",
        "error",
        "lemot",
        "maintenance",
        "pending",
        "lambat"
    ]

    pos_found = any(
        word in text for word in positive_words
    )

    neg_found = any(
        word in text for word in negative_words
    )

    if pos_found and neg_found:

        return True

    return False

# =====================================================
# EMOTION PREDICTION
# =====================================================

def predict_emotion(text):

    text = clean_text(text)

    # =====================================================
    # SARCASM
    # =====================================================

    if detect_sarcasm(text):

        return "frustrasi", 0.95

    # =====================================================
    # NEGATIVE
    # =====================================================

    negative_words = [
        "gagal",
        "error",
        "lemot",
        "kecewa",
        "maintenance",
        "marah",
        "pending"
    ]

    if any(word in text for word in negative_words):

        return "marah", 0.90

    # =====================================================
    # FEAR
    # =====================================================

    fear_words = [
        "takut",
        "cemas",
        "khawatir"
    ]

    if any(word in text for word in fear_words):

        return "cemas", 0.88

    # =====================================================
    # POSITIVE
    # =====================================================

    positive_words = [
        "bagus",
        "cepat",
        "mantap",
        "membantu",
        "keren",
        "hebat"
    ]

    if any(word in text for word in positive_words):

        return "senang", 0.92

    # =====================================================
    # DEFAULT
    # =====================================================

    return "netral", 0.80

# =====================================================
# EMOTION STYLE
# =====================================================

emotion_styles = {
    "marah": {
        "emoji": "😡",
        "color": "#FF4B4B"
    },

    "frustrasi": {
        "emoji": "😤",
        "color": "#FF8C00"
    },

    "cemas": {
        "emoji": "😰",
        "color": "#8A2BE2"
    },

    "senang": {
        "emoji": "😊",
        "color": "#00C853"
    },

    "netral": {
        "emoji": "😐",
        "color": "#808080"
    }
}

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

        # =====================================================
        # PREDICTION
        # =====================================================

        emotion, confidence = predict_emotion(
            text
        )

        is_sarcasm = detect_sarcasm(
            text
        )

        # =====================================================
        # STYLE
        # =====================================================

        emoji = emotion_styles[emotion]["emoji"]

        color = emotion_styles[emotion]["color"]

        # =====================================================
        # RESULT HEADER
        # =====================================================

        st.markdown("---")

        st.markdown("## 📌 Hasil Analisis")

        # =====================================================
        # EMOTION DISPLAY
        # =====================================================

        st.markdown(
            f"""
            <div style="
                background-color:{color};
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:white;
            ">
                <h1>
                    {emoji} {emotion.upper()}
                </h1>
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

            st.error(
                "⚠️ Sarkasme Terdeteksi"
            )

        else:

            st.success(
                "✅ Tidak Mengandung Sarkasme"
            )

        # =====================================================
        # CLEAN TEXT
        # =====================================================

        st.markdown("### 📝 Hasil Cleaning")

        st.code(
            clean_text(text)
        )

# =====================================================
# SAMPLE
# =====================================================

st.markdown("---")

st.subheader("📌 Contoh Kalimat Sarkasme")

samples = [
    "Bagus banget aplikasinya transfer gagal terus",
    "Mantap maintenance tiap malam",
    "Keren login 2 jam gagal",
    "Cepat banget errornya muncul terus"
]

for s in samples:

    st.code(s)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Prototype Analisis Emosi & Sarkasme | Tesis NLP Mobile Banking"
)
