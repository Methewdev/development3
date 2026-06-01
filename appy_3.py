import streamlit as st
import pandas as pd
from transformers import pipeline

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_models():

    sentiment_model = pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

    emotion_model = pipeline(
        "text-classification",
        model="USERNAME/MODEL_EMOTION"
    )

    return sentiment_model, emotion_model


sentiment_pipe, emotion_pipe = load_models()

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "total": 0,
    "positive": 0,
    "negative": 0,
    "neutral": 0,
    "history": [],
    "input_text": "",
    "sentiment_result": "-",
    "emotion_result": "-",
    "confidence_result": "-"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

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
    border-radius:15px;
    padding:20px;
    text-align:center;
    border:1px solid #24324f;
}

.result-card{
    background:#13203b;
    border-radius:12px;
    padding:15px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# EMOTION MAP
# =====================================================

EMOTION_MAP = {
    "LABEL_0": "😡 Anger",
    "LABEL_1": "😨 Fear",
    "LABEL_2": "😊 Joy",
    "LABEL_3": "😢 Sadness",
    "LABEL_4": "😐 Neutral"
}

# =====================================================
# FUNCTIONS
# =====================================================

def predict_emotion(text):

    result = emotion_pipe(text)[0]

    raw_label = result["label"]
    score = float(result["score"])

    # Mapping manual
    emotion_map = {
        "LABEL_0": "😡 Anger",
        "LABEL_1": "😨 Fear",
        "LABEL_2": "😊 Joy",
        "LABEL_3": "😢 Sadness",
        "LABEL_4": "😐 Neutral"
    }

    emotion_label = emotion_map.get(
        raw_label,
        raw_label
    )

    return emotion_label, score
# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🧠 Emotion AI")

    st.caption(
        "Sentiment & Emotion Analysis"
    )

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True
    ):

        st.session_state.total = 0
        st.session_state.positive = 0
        st.session_state.negative = 0
        st.session_state.neutral = 0

        st.session_state.history = []

        st.session_state.input_text = ""

        st.session_state.sentiment_result = "-"
        st.session_state.emotion_result = "-"
        st.session_state.confidence_result = "-"

        st.rerun()

# =====================================================
# TITLE
# =====================================================

st.title("📊 Dashboard Analisis Emosi")
st.caption(
    "Prototype Sentiment & Emotion Classification"
)

# =====================================================
# DASHBOARD
# =====================================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
    <h4>Total</h4>
    <h2>{st.session_state.total}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
    <h4>😊 Positif</h4>
    <h2>{st.session_state.positive}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
    <h4>😡 Negatif</h4>
    <h2>{st.session_state.negative}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
    <h4>😐 Netral</h4>
    <h2>{st.session_state.neutral}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =====================================================
# MAIN
# =====================================================

left,right = st.columns([2,1])

with left:

    st.subheader("✍ Input Ulasan")

    text = st.text_area(
        "",
        key="input_text",
        height=250,
        placeholder="Masukkan ulasan pengguna..."
    )

    c1,c2 = st.columns(2)

    with c1:
        analyze = st.button(
            "🔍 Analisis",
            use_container_width=True
        )

    with c2:
        clear = st.button(
            "🗑️ Clear Input",
            use_container_width=True
        )

with right:

    st.subheader("📌 Hasil")

    st.success(
        f"💬 Sentimen : {st.session_state.sentiment_result}"
    )

    st.info(
        f"😡 Emosi : {st.session_state.emotion_result}"
    )

    st.warning(
        f"🎯 Confidence : {st.session_state.confidence_result}"
    )

# =====================================================
# CLEAR INPUT
# =====================================================

if clear:

    st.session_state.input_text = ""

    st.session_state.sentiment_result = "-"
    st.session_state.emotion_result = "-"
    st.session_state.confidence_result = "-"

    st.rerun()

# =====================================================
# ANALYSIS
# =====================================================

if analyze:

    if text.strip():

        sentiment, sentiment_score = predict_sentiment(text)

        emotion, emotion_score, raw_label = predict_emotion(text)

        st.session_state.sentiment_result = sentiment
        st.session_state.emotion_result = emotion
        st.session_state.confidence_result = (
            f"{emotion_score:.2%}"
        )

        st.session_state.total += 1

        if "Positif" in sentiment:
            st.session_state.positive += 1

        elif "Negatif" in sentiment:
            st.session_state.negative += 1

        else:
            st.session_state.neutral += 1

        st.session_state.history.append({
            "Text": text,
            "Sentiment": sentiment,
            "Emotion": emotion,
            "Confidence": round(
                emotion_score * 100,
                2
            )
        })

        st.rerun()

# =====================================================
# HISTORY
# =====================================================

if len(st.session_state.history) > 0:

    st.divider()

    st.subheader("📜 Riwayat Analisis")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

# =====================================================
# DEBUG
# =====================================================

with st.expander("⚙️ Debug Model"):

    st.write(
        "Emotion Model Labels:"
    )

    try:
        st.write(
            emotion_pipe.model.config.id2label
        )
    except:
        st.write(
            "id2label tidak ditemukan"
        )

    st.write(
        "Emotion Mapping:"
    )

    st.json(
        EMOTION_MAP
    )
