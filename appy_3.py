import streamlit as st
import pandas as pd

from utils import (
    predict_sentiment,
    predict_emotion
)

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# ====================================
# CSS
# ====================================

st.markdown("""
<style>

.stApp{
    background-color:#020817;
    color:white;
}

.card{
    background:#13203b;
    padding:20px;
    border-radius:15px;
    text-align:center;
}

.result-box{
    padding:15px;
    border-radius:10px;
    margin-bottom:10px;
}

.blue{
    background:#1e3a8a;
}

.green{
    background:#166534;
}

.yellow{
    background:#854d0e;
}

.red{
    background:#7f1d1d;
}

</style>
""", unsafe_allow_html=True)

# ====================================
# SIDEBAR
# ====================================

with st.sidebar:

    st.markdown("# 🧠 Emotion AI")

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

# ====================================
# DASHBOARD
# ====================================

st.title("📊 Dashboard Analisis Emosi")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown("""
    <div class='card'>
        <h4>Total</h4>
        <h1>0</h1>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='card'>
        <h4>😊 Positif</h4>
        <h1>0</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='card'>
        <h4>😡 Negatif</h4>
        <h1>0</h1>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='card'>
        <h4>😐 Netral</h4>
        <h1>0</h1>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class='card'>
        <h4>🧠 Sarkasme</h4>
        <h1>0</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")

left,right = st.columns([2,1])

with left:

    review = st.text_area(
        "✍ Input Ulasan",
        height=220,
        placeholder="Masukkan ulasan nasabah..."
    )

    analyze = st.button(
        "🔍 Analisis Sekarang",
        use_container_width=True
    )

with right:

    st.subheader("📌 Hasil")

    emotion_placeholder = st.empty()
    sentiment_placeholder = st.empty()
    confidence_placeholder = st.empty()
    sarcasm_placeholder = st.empty()

# ====================================
# ANALYSIS
# ====================================

if analyze:

    if review.strip():

        sentiment = predict_sentiment(review)
        emotion = predict_emotion(review)

        emotion_placeholder.markdown(f"""
        <div class='result-box blue'>
        😡 Emosi : <b>{emotion['label']}</b>
        </div>
        """, unsafe_allow_html=True)

        sentiment_placeholder.markdown(f"""
        <div class='result-box green'>
        💬 Sentimen : <b>{sentiment['label']}</b>
        </div>
        """, unsafe_allow_html=True)

        confidence_placeholder.markdown(f"""
        <div class='result-box yellow'>
        🎯 Confidence : <b>{emotion['score']}%</b>
        </div>
        """, unsafe_allow_html=True)

        sarcasm_placeholder.markdown(f"""
        <div class='result-box red'>
        🧠 Sarkasme : <b>Tidak Terdeteksi</b>
        </div>
        """, unsafe_allow_html=True)
