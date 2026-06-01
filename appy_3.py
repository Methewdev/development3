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

    sentiment_model = pipeline(
        "text-classification",
        model="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

    emotion_model = pipeline(
        "text-classification",
        model="envidevelopment/emotion_model"
    )

    return sentiment_model, emotion_model


sentiment_pipe, emotion_pipe = load_models()

# =====================================================
# SESSION STATE
# =====================================================

for key in ["total", "positive", "negative", "neutral"]:
    if key not in st.session_state:
        st.session_state[key] = 0

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#020817;
}

.card{
    background:#13203b;
    padding:20px;
    border-radius:15px;
    border:1px solid #2d3b55;
}

.result-box{
    padding:15px;
    border-radius:12px;
    color:white;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# PREDICT FUNCTION
# =====================================================

def predict_sentiment(text):

    result = sentiment_pipe(text)[0]

    label = result["label"].lower()

    score = round(result["score"] * 100, 2)

    return label, score


def predict_emotion(text):

    result = emotion_pipe(text)[0]

    label = result["label"]

    score = round(result["score"] * 100, 2)

    return label, score

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🧠 Emotion AI")
    st.caption("Dashboard Analisis Emosi & Sentimen")

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
# CARD
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
# LAYOUT
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

    result_container = st.empty()

# =====================================================
# ANALISIS
# =====================================================

if analyze:

    if text.strip():

        sentiment_label, sentiment_score = predict_sentiment(text)

        emotion_label, emotion_score = predict_emotion(text)

        st.session_state.total += 1

        if sentiment_label == "positive":
            st.session_state.positive += 1

        elif sentiment_label == "negative":
            st.session_state.negative += 1

        else:
            st.session_state.neutral += 1

        sentiment_translate = {
            "positive": "Positif",
            "negative": "Negatif",
            "neutral": "Netral"
        }

        sentiment_display = sentiment_translate.get(
            sentiment_label,
            sentiment_label
        )

        with result_container.container():

            st.success(
                f"💬 Sentimen : {sentiment_display}"
            )

            st.info(
                f"😡 Emosi : {emotion_label}"
            )

            st.warning(
                f"🎯 Confidence : {sentiment_score}%"
            )

            # DEBUG
            with st.expander("Debug Model"):

                st.write("Sentiment Raw")

                st.json(
                    sentiment_pipe(text)[0]
                )

                st.write("Emotion Raw")

                st.json(
                    emotion_pipe(text)[0]
                )

    else:
        st.warning("Masukkan teks terlebih dahulu")
