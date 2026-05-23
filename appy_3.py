import streamlit as st
import pandas as pd
import chardet
import plotly.express as px

from io import StringIO

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
    background:#050816;
}

/* =====================================================
MENU STYLE
===================================================== */

div[role="radiogroup"] > label{

    background:#111827;

    padding:12px;

    border-radius:14px;

    margin-bottom:10px;

    border:1px solid rgba(255,255,255,0.05);

    transition:0.3s;

}

div[role="radiogroup"] > label:hover{

    background:#1e293b;

    transform:translateX(5px);

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

/* =====================================================
TEXT
===================================================== */

h1, h2, h3, h4{
    color:white !important;
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

with st.sidebar:

    st.markdown("""

    <div style="
        background: linear-gradient(
            145deg,
            rgba(17,24,39,0.95),
            rgba(30,41,59,0.90)
        );
        padding:25px;
        border-radius:25px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:20px;
    ">

    <h1 style="
        color:white;
        font-size:36px;
        margin-bottom:10px;
    ">
    🧠 Emotion AI
    </h1>

    <p style="
        color:#94a3b8;
        font-size:14px;
    ">
    Dashboard Analisis Emosi & Sarkasme
    </p>

    </div>

    """, unsafe_allow_html=True)

    # =============================================
    # MENU
    # =============================================

    menu = st.radio(

        "📌 MENU",

        [

            "🏠 Dashboard",

            "✍️ Analisis Satuan",

            "📂 Bulk CSV",

            "📈 Statistik",

            "🕘 Riwayat"

        ]

    )

    st.markdown("---")

    # =============================================
    # REFRESH BUTTON
    # =============================================

    if st.button("🔄 Refresh Dashboard"):

        st.session_state.result_df = None

        st.success(
            "✅ Dashboard berhasil direset"
        )

        st.rerun()

# =====================================================
# HEADER
# =====================================================

st.title("📊 Dashboard Analisis Emosi")

st.caption(
    "Prototype Analisis Emosi & Sarkasme berbasis AI"
)

# =====================================================
# METRIC DATA
# =====================================================

total_data = 0
positif = 0
negatif = 0
netral = 0
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

    netral = len(
        df_metric[
            df_metric["Sentimen"] == "Netral"
        ]
    )

    sarkasme = len(
        df_metric[
            df_metric["Sarkasme"] == "Ya"
        ]
    )

# =====================================================
# METRIC CARDS
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    with st.container(border=True):

        st.markdown("### 📊 Total ")
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

        st.markdown("### 😐 Netral")
        st.markdown(f"# {netral}")

with col5:

    with st.container(border=True):

        st.markdown("### 🧠 Sarkasme")
        st.markdown(f"# {sarkasme}")

# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

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

        fig = px.bar(

            emotion_count,

            x="Emosi",

            y="Jumlah",

            text="Jumlah",

            title="Distribusi Emosi",

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0b1120",

            plot_bgcolor="#0b1120",

            font_color="white",

            title_font_size=24,

            xaxis_title="Kategori Emosi",

            yaxis_title="Jumlah Data",

            height=500

        )

        st.plotly_chart(
            fig,
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

elif menu == "✍️ Analisis Satuan":

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

elif menu == "📂 Bulk CSV":

    st.subheader("📂 Upload CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            raw_data = uploaded_file.read()

            detected = chardet.detect(raw_data)

            encoding = detected["encoding"]

            st.info(f"Encoding terdeteksi : {encoding}")

            decoded_data = raw_data.decode(
                encoding,
                errors="ignore"
            )

            try:

                df = pd.read_csv(
                    StringIO(decoded_data),
                    sep=";"
                )

            except:

                df = pd.read_csv(
                    StringIO(decoded_data),
                    sep=","
                )

            df = df.dropna(
                axis=1,
                how="all"
            )

            st.success(
                "✅ File berhasil diupload"
            )

            st.write("### Preview Dataset")

            st.dataframe(
                df.head(),
                use_container_width=True
            )

            st.write(
                f"Jumlah Data : {len(df)}"
            )

            selected_column = st.selectbox(
                "Pilih Kolom Ulasan",
                df.columns
            )

            if st.button("🚀 Mulai Analisis"):

                results = []

                progress = st.progress(0)

                total = len(df)

                for i in range(total):

                    text = str(
                        df[selected_column].iloc[i]
                    )

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

                st.session_state.result_df = result_df

                st.success(
                    "✅ Analisis selesai"
                )

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

                fig = px.bar(

                    emotion_count,

                    x="Emosi",

                    y="Jumlah",

                    text="Jumlah",

                    title="Distribusi Emosi",

                    template="plotly_dark"

                )

                fig.update_layout(

                    paper_bgcolor="#0b1120",

                    plot_bgcolor="#0b1120",

                    font_color="white",

                    title_font_size=24,

                    xaxis_title="Kategori Emosi",

                    yaxis_title="Jumlah Data",

                    height=500

                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("📋 Hasil Analisis")

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

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

            st.code(str(e))

# =====================================================
# STATISTIK
# =====================================================

elif menu == "📈 Statistik":

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

        fig = px.bar(

            statistik,

            x="Emosi",

            y="Jumlah",

            text="Jumlah",

            title="Statistik Emosi",

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0b1120",

            plot_bgcolor="#0b1120",

            font_color="white",

            height=500

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "🕘 Riwayat":

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
