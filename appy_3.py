import streamlit as st
from transformers import pipeline

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_models():

    sentiment_model = pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

    emotion_model = pipeline(
        "text-classification",
        model="USERNAME/emotion_model"
    )

    return sentiment_model, emotion_model

sentiment_pipe, emotion_pipe = load_models()

# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_sentiment(text):

    result = sentiment_pipe(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }


def predict_emotion(text):

    result = emotion_pipe(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }

# =========================================================
# SESSION STATE
# =========================================================

if "total" not in st.session_state:
    st.session_state.total = 0

if "positif" not in st.session_state:
    st.session_state.positif = 0

if "negatif" not in st.session_state:
    st.session_state.negatif = 0

if "netral" not in st.session_state:
    st.session_state.netral = 0

if "sarkasme" not in st.session_state:
    st.session_state.sarkasme = 0

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp{
    background:#020817;
    color:white;
}

section[data-testid="stSidebar"]{
    background:#010B20;
}

.card{
    background:#13203b;
    padding:20px;
    border-radius:18px;
    border:1px solid #2d3b55;
}

.result-box{
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
    color:white;
}

.blue{
    background:#1E3A8A;
}

.green{
    background:#166534;
}

.yellow{
    background:#854D0E;
}

.red{
    background:#7F1D1D;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("# 🧠 Emotion AI")
    st.caption("Dashboard Analisis Emosi & Sentimen")

    menu = st.radio(
        "MENU",
        [
            "Dashboard",
            "Analisis Satuan",
            "Bulk CSV",
            "Statistik",
            "Riwayat"
        ]
    )

# =========================================================
# HEADER
# =========================================================

st.title("📊 Dashboard Analisis Emosi")
st.caption("Prototype Analisis Emosi berbasis Hugging Face")

# =========================================================
# CARD DASHBOARD
# =========================================================

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='card'>
    <h4>📊 Total</h4>
    <h1>{st.session_state.total}</h1>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card'>
    <h4>😊 Positif</h4>
    <h1>{st.session_state.positif}</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card'>
    <h4>😡 Negatif</h4>
    <h1>{st.session_state.negatif}</h1>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='card'>
    <h4>😐 Netral</h4>
    <h1>{st.session_state.netral}</h1>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='card'>
    <h4>🧠 Sarkasme</h4>
    <h1>{st.session_state.sarkasme}</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================================================
# INPUT & RESULT
# =========================================================

left,right = st.columns([2,1])

with left:

    text = st.text_area(
        "✍ Input Ulasan",
        placeholder="Masukkan ulasan pengguna...",
        height=220
    )

    analyze = st.button(
        "🔍 Analisis Sekarang",
        use_container_width=True
    )

with right:

    st.subheader("📌 Hasil")

    emotion_box = st.empty()
    sentiment_box = st.empty()
    confidence_box = st.empty()
    sarcasm_box = st.empty()

# =========================================================
# PROCESS
# =========================================================

if analyze:

    if text.strip():

        sentiment = predict_sentiment(text)
        emotion = predict_emotion(text)

        st.session_state.total += 1

        if sentiment["label"].lower() == "positive":
            st.session_state.positif += 1

        elif sentiment["label"].lower() == "negative":
            st.session_state.negatif += 1

        else:
            st.session_state.netral += 1

        emotion_box.markdown(f"""
        <div class='result-box blue'>
        😡 Emosi : <b>{emotion['label']}</b>
        </div>
        """, unsafe_allow_html=True)

        sentiment_box.markdown(f"""
        <div class='result-box green'>
        💬 Sentimen : <b>{sentiment['label']}</b>
        </div>
        """, unsafe_allow_html=True)

        confidence_box.markdown(f"""
        <div class='result-box yellow'>
        🎯 Confidence : <b>{emotion['score']}%</b>
        </div>
        """, unsafe_allow_html=True)

        sarcasm_box.markdown(f"""
        <div class='result-box red'>
        🧠 Sarkasme : <b>Tidak Terdeteksi</b>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Masukkan teks terlebih dahulu")
