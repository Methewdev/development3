
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

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
.stApp{background:#050816;}
[data-testid="stSidebar"]{background:#111827;}
div[data-testid="metric-container"]{
background:#1E293B;border-radius:15px;padding:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= DUMMY MODEL =================
# Ganti dengan model Sentimen & Emosi Anda

def predict_sentiment(text):
    text = str(text).lower()
    if any(w in text for w in ["bagus","baik","mantap","cepat"]):
        return "positive",0.98
    elif any(w in text for w in ["buruk","jelek","error","lambat","gagal"]):
        return "negative",0.99
    return "neutral",0.95

def predict_emotion(text):
    text = str(text).lower()
    if "marah" in text or "kesal" in text:
        return "anger"
    if "takut" in text:
        return "fear"
    if "senang" in text or "bahagia" in text:
        return "happy"
    if "cinta" in text:
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

    if total == 0:
        positive = negative = neutral = 0
    else:
        positive = len(df[df["sentiment"]=="positive"])
        negative = len(df[df["sentiment"]=="negative"])
        neutral = len(df[df["sentiment"]=="neutral"])

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("Positif", positive)
    c3.metric("Negatif", negative)
    c4.metric("Netral", neutral)

    if total == 0:
        st.info("Belum ada hasil Bulk CSV. Silakan upload data terlebih dahulu.")
    else:
        left,right = st.columns([2,1])

        with left:
            sentiment_count = df["sentiment"].value_counts().reset_index()
            sentiment_count.columns=["sentiment","jumlah"]

            fig = px.bar(sentiment_count,x="sentiment",y="jumlah")
            st.plotly_chart(fig,use_container_width=True)

        with right:
            fig2 = px.pie(sentiment_count,names="sentiment",values="jumlah",hole=.6)
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

    uploaded_file = st.file_uploader(
        "Upload CSV / XLSX",
        type=["csv", "xlsx"]
    )

    if uploaded_file:

        try:

            # ==========================
            # XLSX
            # ==========================
            if uploaded_file.name.endswith(".xlsx"):

                df = pd.read_excel(
                    uploaded_file
                )

            else:

                # ==========================
                # AUTO DETECT CSV
                # ==========================

                encodings = [
                    "utf-8",
                    "utf-8-sig",
                    "latin1",
                    "cp1252",
                    "ISO-8859-1"
                ]

                separators = [
                    ",",
                    ";"
                ]

                df = None

                for enc in encodings:

                    for sep in separators:

                        try:

                            uploaded_file.seek(0)

                            temp_df = pd.read_csv(
                                uploaded_file,
                                encoding=enc,
                                sep=sep,
                                engine="python",
                                on_bad_lines="skip"
                            )

                            if len(temp_df.columns) > 1:

                                df = temp_df
                                break

                        except Exception:
                            continue

                    if df is not None:
                        break

                if df is None:

                    st.error(
                        "❌ File tidak dapat dibaca."
                    )

                    st.stop()

            # ==========================
            # TAMPILKAN DATA
            # ==========================

            st.success(
                f"✅ Dataset berhasil dibaca ({len(df)} baris)"
            )

            st.dataframe(
                df.head()
            )

            text_col = st.selectbox(
                "Pilih Kolom Ulasan",
                df.columns
            )

            if st.button(
                "🚀 Proses Analisis"
            ):

                sentiments = []
                emotions = []
                scores = []
                emotion_scores = []

                progress = st.progress(0)

                total_rows = len(df)

                for idx, text in enumerate(df[text_col]):

                    sentiment, score = predict_sentiment(
                        str(text)
                    )

                    emotion, emotion_score = predict_emotion(
                        str(text)
                    )

                    sentiments.append(
                        sentiment
                    )

                    emotions.append(
                        emotion
                    )

                    scores.append(
                        score
                    )

                    emotion_scores.append(
                        emotion_score
                    )

                    progress.progress(
                        (idx + 1) / total_rows
                    )

                df["sentiment"] = sentiments
                df["emotion"] = emotions
                df["score"] = scores
                df["emotion_score"] = emotion_scores

                st.session_state.bulk_result = df

                st.session_state.bulk_history.append(
                    {
                        "datetime":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "rows":
                        len(df)
                    }
                )

                st.success(
                    "✅ Analisis selesai"
                )

                st.dataframe(df)

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

# ================= STATISTIK =================
elif menu == "Statistik":

    st.title("📈 Statistik")

    df = st.session_state.bulk_result

    if len(df) == 0:
        st.warning("Belum ada hasil Bulk CSV.")
    else:
        col1,col2 = st.columns(2)

        with col1:
            fig1 = px.pie(df,names="sentiment",hole=.5,title="Distribusi Sentimen")
            st.plotly_chart(fig1,use_container_width=True)

        with col2:
            fig2 = px.histogram(df,x="emotion",color="emotion",title="Distribusi Emosi")
            st.plotly_chart(fig2,use_container_width=True)

# ================= RIWAYAT =================
elif menu == "Riwayat":

    st.title("🕒 Riwayat Upload")

    if len(st.session_state.bulk_history) == 0:
        st.warning("Belum ada riwayat upload.")
    else:
        history_df = pd.DataFrame(st.session_state.bulk_history)
        st.dataframe(history_df,use_container_width=True)
