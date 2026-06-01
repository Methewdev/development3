
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Emotion AI Dashboard", page_icon="🧠", layout="wide")

# ================= SESSION =================
if "single_result" not in st.session_state:
    st.session_state.single_result = None

if "bulk_result" not in st.session_state:
    st.session_state.bulk_result = pd.DataFrame()

if "bulk_history" not in st.session_state:
    st.session_state.bulk_history = []

# ================= CSS =================
st.markdown("""
<style>
.stApp {background:#050816;}
[data-testid="stSidebar"] {background:#111827;}
div[data-testid="metric-container"]{
background:#1E293B;
border:1px solid #334155;
border-radius:15px;
padding:15px;
}
</style>
""", unsafe_allow_html=True)

# ================= DUMMY MODEL =================
# GANTI DENGAN MODEL SENTIMEN & EMOSI ASLI

def predict_sentiment(text):
    text = str(text).lower()

    positive_words = ["bagus","mantap","baik","cepat","hebat","keren","puas","memuaskan"]
    negative_words = ["buruk","jelek","error","lambat","gagal","kecewa"]

    if any(w in text for w in positive_words):
        return "positive", 0.98

    if any(w in text for w in negative_words):
        return "negative", 0.99

    return "neutral", 0.95


def predict_emotion(text):
    text = str(text).lower()

    happy_words = [
        "bagus","mantap","baik","hebat","keren",
        "senang","bahagia","puas","memuaskan","suka"
    ]

    anger_words = [
        "marah","kesal","buruk","jelek",
        "lambat","error","gagal","kecewa"
    ]

    fear_words = [
        "takut","cemas","khawatir"
    ]

    love_words = [
        "cinta","sayang"
    ]

    if any(w in text for w in happy_words):
        return "happy"

    if any(w in text for w in anger_words):
        return "anger"

    if any(w in text for w in fear_words):
        return "fear"

    if any(w in text for w in love_words):
        return "love"

    return "sadness"

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🧠 Emotion AI")
    menu = st.radio(
        "Menu",
        ["Dashboard","Analisis Satuan","Bulk CSV","Statistik","Riwayat"]
    )

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    df = st.session_state.bulk_result

    total = len(df)

    if total > 0:
        positive = len(df[df["sentiment"]=="positive"])
        negative = len(df[df["sentiment"]=="negative"])
        neutral = len(df[df["sentiment"]=="neutral"])
    else:
        positive = negative = neutral = 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("Positif", positive)
    c3.metric("Negatif", negative)
    c4.metric("Netral", neutral)

    if total == 0:
        st.info("Dashboard akan terisi setelah proses Bulk CSV.")
    else:
        col1,col2 = st.columns([2,1])

        with col1:
            sent = df["sentiment"].value_counts().reset_index()
            sent.columns = ["sentiment","jumlah"]
            fig = px.bar(sent,x="sentiment",y="jumlah")
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            fig2 = px.pie(sent,names="sentiment",values="jumlah",hole=0.6)
            st.plotly_chart(fig2,use_container_width=True)

        if st.button("🔄 Refresh Dashboard"):
            st.session_state.bulk_result = pd.DataFrame()
            st.session_state.bulk_history = []
            st.rerun()

# ================= ANALISIS SATUAN =================
elif menu == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    text = st.text_area("Masukkan Ulasan", height=200)

    if st.button("🔍 Analisis"):
        if text.strip():
            sentiment, score = predict_sentiment(text)
            emotion = predict_emotion(text)

            st.session_state.single_result = {
                "text": text,
                "sentiment": sentiment,
                "emotion": emotion,
                "score": score
            }

    if st.session_state.single_result:

        result = st.session_state.single_result

        c1,c2,c3 = st.columns(3)

        c1.metric("Sentimen", result["sentiment"].upper())
        c2.metric("Emosi", result["emotion"].upper())
        c3.metric("Confidence", f"{result['score']*100:.2f}%")

        st.text_area("Teks", result["text"], disabled=True)

# ================= BULK CSV =================
elif menu == "Bulk CSV":

    st.title("📂 Bulk CSV")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:

        df = pd.read_csv(file)

        st.dataframe(df.head())

        text_col = st.selectbox("Pilih Kolom Ulasan", df.columns)

        if st.button("🚀 Proses Analisis"):

            sentiments = []
            emotions = []
            scores = []

            progress = st.progress(0)

            for idx, txt in enumerate(df[text_col]):

                sentiment, score = predict_sentiment(str(txt))
                emotion = predict_emotion(str(txt))

                sentiments.append(sentiment)
                emotions.append(emotion)
                scores.append(score)

                progress.progress((idx+1)/len(df))

            df["sentiment"] = sentiments
            df["emotion"] = emotions
            df["score"] = scores

            st.session_state.bulk_result = df

            st.session_state.bulk_history.append({
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows": len(df)
            })

            st.dataframe(df)

# ================= STATISTIK =================
elif menu == "Statistik":

    st.title("📈 Statistik")

    df = st.session_state.bulk_result

    if len(df) == 0:
        st.warning("Belum ada hasil Bulk CSV")
    else:
        col1,col2 = st.columns(2)

        with col1:
            fig1 = px.pie(df,names="sentiment",hole=.5)
            st.plotly_chart(fig1,use_container_width=True)

        with col2:
            fig2 = px.histogram(df,x="emotion",color="emotion")
            st.plotly_chart(fig2,use_container_width=True)

# ================= RIWAYAT =================
elif menu == "Riwayat":

    st.title("🕒 Riwayat Upload")

    if len(st.session_state.bulk_history) == 0:
        st.warning("Belum ada riwayat upload")
    else:
        st.dataframe(pd.DataFrame(st.session_state.bulk_history))
