import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#050816;
}

[data-testid="stSidebar"]{
    background:linear-gradient(
    180deg,
    #0F172A 0%,
    #111827 100%);
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

div[data-testid="metric-container"]{
    background:linear-gradient(
    135deg,
    #111827,
    #1E293B);

    border-radius:18px;
    padding:15px;
    border:1px solid rgba(255,255,255,0.08);
}

.stTextArea textarea{
    background:#111827 !important;
    color:white !important;
}

.card{
    background:linear-gradient(
    135deg,
    #111827,
    #1E293B);

    border-radius:18px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.08);
}

.big-title{
    font-size:32px;
    font-weight:700;
    color:white;
}

.sub-title{
    color:#94A3B8;
    font-size:14px;
}

div.stButton > button{
    background:
    linear-gradient(
    90deg,
    #7C3AED,
    #EC4899);

    color:white;
    border:none;
    border-radius:12px;
    height:50px;
    width:100%;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# DUMMY MODEL
# GANTI DENGAN MODEL SENTIMEN & EMOSI ANDA
# =====================================================

def predict_sentiment(text):

    text = text.lower()

    if any(word in text for word in [
        "bagus",
        "mantap",
        "cepat",
        "baik",
        "memuaskan"
    ]):
        return "positive",0.98

    elif any(word in text for word in [
        "lambat",
        "buruk",
        "jelek",
        "error",
        "gagal"
    ]):
        return "negative",0.99

    else:
        return "neutral",0.95


def predict_emotion(text):

    text = text.lower()

    if "marah" in text or "kesal" in text:
        return "anger"

    elif "takut" in text:
        return "fear"

    elif "senang" in text or "bagus" in text:
        return "happy"

    elif "cinta" in text:
        return "love"

    else:
        return "sadness"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2103/2103832.png",
        width=90
    )

    st.markdown("### MENU")

    menu = st.radio(
        "",
        [
            "Dashboard",
            "Analisis Satuan",
            "Bulk CSV",
            "Statistik",
            "Riwayat"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    total = len(st.session_state.history)

    positive = 0
    negative = 0
    neutral = 0

    if total > 0:

        df = pd.DataFrame(
            st.session_state.history
        )

        positive = len(
            df[df["sentiment"]=="positive"]
        )

        negative = len(
            df[df["sentiment"]=="negative"]
        )

        neutral = len(
            df[df["sentiment"]=="neutral"]
        )

    col1,col2 = st.columns([4,1])

    with col1:

        st.markdown("""
        <div class='big-title'>
        Selamat datang kembali, Admin 👋
        </div>

        <div class='sub-title'>
        Pantau dan analisis sentimen dari data ulasan dengan mudah
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.date_input("", value=date.today())

    st.write("")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("📊 Total Analisis", total)
    c2.metric("😊 Positif", positive)
    c3.metric("😡 Negatif", negative)
    c4.metric("😐 Netral", neutral)

    st.write("")

    # =====================================
    # DASHBOARD KOSONG
    # =====================================

    if total == 0:

        st.warning(
            "Belum ada data analisis. "
            "Silakan lakukan analisis terlebih dahulu."
        )

        col1,col2 = st.columns([2,1])

        with col1:

            review = st.text_area(
                "Masukkan Ulasan",
                height=180,
                placeholder="Contoh: Pelayanan sangat baik dan respons cepat!"
            )

        with col2:

            st.markdown("""
            <div class='card'>
            <h3>Insights</h3>

            Belum ada data untuk ditampilkan.

            Mulai analisis untuk melihat insight.
            </div>
            """, unsafe_allow_html=True)

    # =====================================
    # DASHBOARD ADA DATA
    # =====================================

    else:

        left,right = st.columns([2,1])

        with left:

            sentiment_count = (
                df["sentiment"]
                .value_counts()
                .reset_index()
            )

            sentiment_count.columns = [
                "sentiment",
                "jumlah"
            ]

            fig = px.bar(
                sentiment_count,
                x="sentiment",
                y="jumlah",
                title="Tren Sentimen"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#111827",
                plot_bgcolor="#111827"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with right:

            fig2 = px.pie(
                sentiment_count,
                names="sentiment",
                values="jumlah",
                hole=0.7
            )

            fig2.update_layout(
                template="plotly_dark",
                paper_bgcolor="#111827"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        st.write("")

        col1,col2 = st.columns([2,1])

        with col1:

            review = st.text_area(
                "Masukkan Ulasan",
                height=180
            )

        with col2:

            positive_pct = round(
                positive/total*100,
                2
            )

            st.markdown(f"""
            <div class='card'>
            <h3>Insights</h3>

            Mayoritas ulasan bersifat
            <b>Positif ({positive_pct}%)</b>

            </div>
            """, unsafe_allow_html=True)

    st.write("")

    col1,col2 = st.columns(2)

    with col1:

        if st.button("🔍 Analisis Sekarang"):

            if review:

                sentiment,score = predict_sentiment(review)

                emotion = predict_emotion(review)

                st.session_state.history.append({

                    "datetime":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    "text":review,
                    "sentiment":sentiment,
                    "emotion":emotion,
                    "score":score
                })

                st.success(
                    "Analisis berhasil"
                )

                st.rerun()

    with col2:

        if st.button(
            "🔄 Refresh Dashboard"
        ):

            st.session_state.history = []

            st.rerun()

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    text = st.text_area(
        "Masukkan Ulasan",
        height=250
    )

    if st.button("Analisis"):

        if text:

            sentiment,score = predict_sentiment(text)

            emotion = predict_emotion(text)

            c1,c2,c3 = st.columns(3)

            c1.metric(
                "Sentimen",
                sentiment.upper()
            )

            c2.metric(
                "Emosi",
                emotion.upper()
            )

            c3.metric(
                "Confidence",
                f"{score*100:.2f}%"
            )

# =====================================================
# BULK CSV
# =====================================================

elif menu == "Bulk CSV":

    st.title("📂 Bulk CSV")

    file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        st.dataframe(df.head())

        st.success(
            f"{len(df)} data berhasil dibaca"
        )

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

    st.title("📈 Statistik")

    if len(st.session_state.history)==0:

        st.warning(
            "Belum ada data statistik"
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        fig = px.histogram(
            df,
            x="emotion",
            color="emotion"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "Riwayat":

    st.title("🕒 Riwayat")

    if len(st.session_state.history)==0:

        st.warning(
            "Belum ada riwayat"
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "⬇ Download Riwayat",
            df.to_csv(index=False),
            file_name="riwayat.csv"
        )
