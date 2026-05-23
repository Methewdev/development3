import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE
# =====================================================

if "result_df" not in st.session_state:
    st.session_state.result_df = None

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"]{
    background-color:#050816;
    color:white;
    font-family:'Segoe UI', sans-serif;
}

/* Hide Streamlit */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #081028 0%,
        #09142d 100%
    );
}

[data-testid="stSidebar"] *{
    color:white;
}

/* =====================================================
TITLE
===================================================== */

.main-title{
    font-size:42px;
    font-weight:700;
    color:white;
}

.sub-title{
    color:#94a3b8;
    font-size:18px;
    margin-bottom:30px;
}

/* =====================================================
CARD
===================================================== */

[data-testid="stVerticalBlockBorderWrapper"]{

    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.90)
    );

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.08);

    padding:15px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.4);

}

/* =====================================================
TEXT
===================================================== */

h1, h2, h3, h4{
    color:white !important;
}

/* =====================================================
BUTTON
===================================================== */

.stButton button{

    width:100%;

    height:55px;

    border:none;

    border-radius:16px;

    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

    color:white;

    font-size:18px;

    font-weight:600;

}

.stButton button:hover{

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    );

    color:white;

}

/* =====================================================
TEXT AREA
===================================================== */

textarea{

    background:#0f172a !important;

    color:white !important;

    border-radius:15px !important;

}

/* =====================================================
UPLOAD
===================================================== */

[data-testid="stFileUploader"]{

    background:#111827;

    border-radius:20px;

    padding:20px;

    border:1px dashed rgba(255,255,255,0.2);

}

/* =====================================================
DATAFRAME
===================================================== */

[data-testid="stDataFrame"]{

    border-radius:20px;

    overflow:hidden;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTION ANALISIS
# =====================================================

def analyze_emotion(text):

    text = str(text).lower()

    emotion = "Netral"
    sentiment = "Netral"
    confidence = "98.20%"
    sarcasm = "Tidak"

    if "bagus" in text:
        emotion = "Senang"
        sentiment = "Positif"

    elif "error" in text:
        emotion = "Frustrasi"
        sentiment = "Negatif"

    elif "gagal" in text:
        emotion = "Marah"
        sentiment = "Negatif"

    elif "cepat" in text:
        emotion = "Puas"
        sentiment = "Positif"

    return emotion, sentiment, confidence, sarcasm

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("# 🧠 Emotion AI")

st.sidebar.caption(
    "Analisis Emosi & Sarkasme"
)

menu = st.sidebar.radio(
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

st.markdown(
    '<div class="main-title">Dashboard Analisis Emosi</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Prototype Analisis Emosi & Sarkasme berbasis AI</div>',
    unsafe_allow_html=True
)

# =====================================================
# METRIC CARDS
# =====================================================

total_data = 0
positif = 0
negatif = 0
sarkasme = 0

if st.session_state.result_df is not None:

    df_metric = st.session_state.result_df

    total_data = len(df_metric)

    positif = len(
        df_metric[
            df_metric["Sentimen"] == "Positif"
        ]
    )

    negatif = len(
        df_metric[
            df_metric["Sentimen"] == "Negatif"
        ]
    )

    sarkasme = len(
        df_metric[
            df_metric["Sarkasme"] == "Ya"
        ]
    )

col1, col2, col3, col4 = st.columns(4)

with col1:

    with st.container(border=True):

        st.markdown("### 📊 Total Analisis")
        st.markdown(f"# {total_data}")

with col2:

    with st.container(border=True):

        st.markdown("### 😊 Positif")
        st.markdown(f"# {positif}")

with col3:

    with st.container(border=True):

        st.markdown("### 😡 Negatif")
        st.markdown(f"# {negatif}")

with col4:

    with st.container(border=True):

        st.markdown("### 🧠 Sarkasme")
        st.markdown(f"# {sarkasme}")

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    if st.session_state.result_df is None:

        st.warning(
            "⚠️ Belum ada data bulk yang diproses"
        )

        st.info(
            "Silakan upload CSV pada menu Bulk CSV"
        )

    else:

        result_df = st.session_state.result_df

        st.success(
            "✅ Data bulk berhasil dianalisis"
        )

        # =============================================
        # DISTRIBUSI EMOSI
        # =============================================

        st.subheader("📈 Distribusi Emosi")

        emotion_count = (
            result_df["Emosi"]
            .value_counts()
            .reset_index()
        )

        emotion_count.columns = [
            "Emosi",
            "Jumlah"
        ]

        st.dataframe(
            emotion_count,
            use_container_width=True
        )

        # =============================================
        # HASIL ANALISIS
        # =============================================

        st.subheader("📋 Hasil Analisis")

        st.dataframe(
            result_df,
            use_container_width=True
        )

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    left, right = st.columns([2,1])

    with left:

        text = st.text_area(
            "✍️ Input Ulasan",
            height=250,
            placeholder="Masukkan ulasan nasabah..."
        )

        analyze = st.button(
            "🔍 Analisis Sekarang"
        )

    with right:

        emotion = "-"
        sentiment = "-"
        confidence = "-"
        sarcasm = "-"

        if analyze:

            emotion, sentiment, confidence, sarcasm = analyze_emotion(text)

        st.subheader("📌 Hasil")

        st.info(f"😡 Emosi : {emotion}")

        st.success(f"💬 Sentimen : {sentiment}")

        st.warning(f"🎯 Confidence : {confidence}")

        st.error(f"🧠 Sarkasme : {sarcasm}")

# =====================================================
# BULK CSV
# =====================================================

elif menu == "Bulk CSV":

    st.subheader("📂 Upload CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            # =========================================
            # READ CSV UTF-8
            # =========================================

            try:

                df = pd.read_csv(
                    uploaded_file,
                    encoding="utf-8"
                )

            except:

                try:

                    df = pd.read_csv(
                        uploaded_file,
                        encoding="latin1"
                    )

                except:

                    df = pd.read_csv(
                        uploaded_file,
                        encoding="cp1252"
                    )

            st.success(
                "✅ File berhasil diupload"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # =========================================
            # MULAI ANALISIS
            # =========================================

            if st.button("🚀 Mulai Analisis"):

                results = []

                progress = st.progress(0)

                total = len(df)

                for i in range(total):

                    text = str(df.iloc[i,0])

                    emotion, sentiment, confidence, sarcasm = analyze_emotion(text)

                    results.append({

                        "Text": text,
                        "Emosi": emotion,
                        "Sentimen": sentiment,
                        "Confidence": confidence,
                        "Sarkasme": sarcasm

                    })

                    progress.progress(
                        (i + 1) / total
                    )

                result_df = pd.DataFrame(results)

                # =====================================
                # SAVE SESSION
                # =====================================

                st.session_state.result_df = result_df

                st.success(
                    "✅ Analisis selesai"
                )

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

                # =====================================
                # DOWNLOAD CSV
                # =====================================

                csv = result_df.to_csv(index=False)

                st.download_button(

                    label="⬇️ Download Hasil CSV",

                    data=csv,

                    file_name="hasil_analisis.csv",

                    mime="text/csv"

                )

        except Exception as e:

            st.error(
                "❌ Gagal membaca file CSV"
            )

            st.error(str(e))

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

    st.subheader("📈 Statistik")

    if st.session_state.result_df is None:

        st.warning(
            "⚠️ Belum ada data bulk"
        )

    else:

        result_df = st.session_state.result_df

        statistik = (
            result_df["Emosi"]
            .value_counts()
            .reset_index()
        )

        statistik.columns = [
            "Emosi",
            "Jumlah"
        ]

        st.dataframe(
            statistik,
            use_container_width=True
        )

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "Riwayat":

    st.subheader("📜 Riwayat")

    if st.session_state.result_df is None:

        st.warning(
            "⚠️ Belum ada riwayat bulk"
        )

    else:

        st.dataframe(
            st.session_state.result_df,
            use_container_width=True
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "© 2026 Emotion AI Dashboard"
)
