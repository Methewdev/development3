import streamlit as st
from transformers import pipeline

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_models():

    sentiment_pipe = pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

    emotion_pipe = pipeline(
        "text-classification",
        model="USERNAME/MODEL_EMOTION"
    )

    return sentiment_pipe, emotion_pipe


sentiment_pipe, emotion_pipe = load_models()

# =====================================================
# MAPPING EMOSI
# SESUAIKAN JIKA URUTAN BERBEDA
# =====================================================

EMOTION_MAP = {
    "LABEL_0": "😡 Anger",
    "LABEL_1": "😨 Fear",
    "LABEL_2": "😊 Joy",
    "LABEL_3": "😢 Sadness",
    "LABEL_4": "😐 Neutral"
}

# =====================================================
# SESSION
# =====================================================

if "total" not in st.session_state:
    st.session_state.total = 0

if "positive" not in st.session_state:
    st.session_state.positive = 0

if "negative" not in st.session_state:
    st.session_state.negative = 0

if "neutral" not in st.session_state:
    st.session_state.neutral = 0

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#020817;
}

.card{
    background:#13203b;
    padding:20px;
    border-radius:18px;
    border:1px solid #24324f;
    text-align:center;
}

.result-box{
    padding:15px;
    border-radius:12px;
    margin-bottom:10px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🧠 Emotion AI")

    st.caption(
        "Analisis Sentimen dan Emosi"
    )

    st.divider()

    st.radio(
        "MENU",
        [
            "Dashboard",
            "Analisis Satuan",
            "Bulk CSV",
            "Statistik",
            "Riwayat"
        ]
    )

# =====================================================
# HEADER
# =====================================================

st.title("📊 Dashboard Analisis Emosi")
st.caption("Prototype Analisis Sentimen dan Emosi")

# =====================================================
# DASHBOARD CARD
# =====================================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='card'>
    <h4>Total</h4>
    <h2>{st.session_state.total}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='card'>
    <h4>😊 Positif</h4>
    <h2>{st.session_state.positive}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='card'>
    <h4>😡 Negatif</h4>
    <h2>{st.session_state.negative}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='card'>
    <h4>😐 Netral</h4>
    <h2>{st.session_state.neutral}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =====================================================
# INPUT
# =====================================================

left,right = st.columns([2,1])

with left:

    text = st.text_area(
        "✍ Input Ulasan",
        height=250,
        placeholder="Masukkan ulasan pengguna..."
    )

    analyze = st.button(
        "🔍 Analisis Sekarang",
        use_container_width=True
    )

with right:

    st.subheader("📌 Hasil")

# =====================================================
# ANALISIS
# =====================================================

if analyze:

    if text.strip():

        # ------------------------
        # SENTIMENT
        # ------------------------

        sent_result = sentiment_pipe(text)[0]

        sent_label = sent_result["label"].lower()
        sent_score = sent_result["score"]

        sentiment_translate = {
            "positive": "😊 Positif",
            "negative": "😡 Negatif",
            "neutral": "😐 Netral"
        }

        sentiment_display = sentiment_translate.get(
            sent_label,
            sent_label
        )

        # ------------------------
        # EMOTION
        # ------------------------

        emo_result = emotion_pipe(text)[0]

        emo_raw = emo_result["label"]

        emotion_display = EMOTION_MAP.get(
            emo_raw,
            emo_raw
        )

        emotion_score = emo_result["score"]

        # ------------------------
        # COUNTER
        # ------------------------

        st.session_state.total += 1

        if sent_label == "positive":
            st.session_state.positive += 1

        elif sent_label == "negative":
            st.session_state.negative += 1

        else:
            st.session_state.neutral += 1

        # ------------------------
        # OUTPUT
        # ------------------------

        st.success(
            f"💬 Sentimen : {sentiment_display}"
        )

        st.info(
            f"😡 Emosi : {emotion_display}"
        )

        st.warning(
            f"🎯 Confidence : {emotion_score:.2%}"
        )

        # ------------------------
        # DEBUG
        # ------------------------

        with st.expander("Debug Model"):

            st.write("Raw Sentiment")
            st.json(sent_result)

            st.write("Raw Emotion")
            st.json(emo_result)

    else:

        st.warning(
            "Masukkan teks terlebih dahulu"
        )
