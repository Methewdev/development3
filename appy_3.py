import streamlit as st
import pandas as pd
import chardet
import plotly.express as px

from io import StringIO
from transformers import pipeline

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
# LOAD MODEL HUGGINGFACE
# =====================================================

@st.cache_resource
def load_model():

    classifier = pipeline(

        task="text-classification",

        model="envidevelopment/model3",

        tokenizer="envidevelopment/model3"

    )

    return classifier

classifier = load_model()

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

/* =====================================================
HIDE STREAMLIT
===================================================== */

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
METRIC CARD
===================================================== */

.metric-card{

    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.90)
    );

    padding:25px;

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.4);

}

.metric-title{

    font-size:22px;
    font-weight:600;
    color:white;

}

.metric-value{

    font-size:50px;
    font-weight:bold;
    color:white;

    margin-top:20px;

}

/* =====================================================
RESULT BOX
===================================================== */

.result-box{

    padding:18px;

    border-radius:16px;

    margin-bottom:15px;

    color:white;

    font-size:18px;

    font-weight:500;

}

.blue{
    background:#1e3a5f;
}

.green{
    background:#14532d;
}

.yellow{
    background:#5b5a1c;
}

.red{
    background:#5b2333;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTION ANALISIS
# =====================================================

def analyze_emotion(text):

    try:

        result = classifier(text)

        label = result[0]["label"].lower()

        score = result[0]["score"]

        confidence = f"{score * 100:.2f}%"

        # =============================================
        # MAPPING LABEL
        # =============================================

        if label == "positive":

            sentiment = "Positif"
            emotion = "Senang"

        elif label == "negative":

            sentiment = "Negatif"
            emotion = "Marah"

        elif label == "neutral":

            sentiment = "Netral"
            emotion = "Netral"

        else:

            sentiment = label
            emotion = label

        # =============================================
        # SARCASM DETECTION
        # =============================================

        sarcasm = "Tidak"

        sarcasm_keywords = [

            "mantap error terus",
            "hebat banget lemot",
            "luar biasa gagal terus"

        ]

        for keyword in sarcasm_keywords:

            if keyword in text.lower():

                sarcasm = "Ya"

        return (

            emotion,
            sentiment,
            confidence,
            sarcasm

        )

    except Exception as e:

        return (

            "Error",
            "Error",
            "0%",
            "Tidak"

        )

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
    Dashboard Analisis Emosi & Sentimen
    </p>

    </div>

    """, unsafe_allow_html=True)

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

    if st.button("🔄 Refresh Dashboard"):

        st.session_state.result_df = None

        st.rerun()

# =====================================================
# HEADER
# =====================================================

st.title("📊 Dashboard Analisis Emosi")

st.caption(
    "Prototype Analisis Emosi berbasis Hugging Face"
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

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📊 Total</div>
        <div class="metric-value">{total_data}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">😊 Positif</div>
        <div class="metric-value">{positif}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">😡 Negatif</div>
        <div class="metric-value">{negatif}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">😐 Netral</div>
        <div class="metric-value">{netral}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🧠 Sarkasme</div>
        <div class="metric-value">{sarkasme}</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    st.subheader("📊 Dashboard")

    if st.session_state.result_df is None:

        st.warning(
            "⚠️ Belum ada data bulk yang diproses"
        )

    else:

        result_df = st.session_state.result_df

        st.success(
            "✅ Data berhasil dianalisis"
        )

        # =============================================
        # CHART
        # =============================================

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

            color="Emosi",

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

        if analyze and text != "":

            emotion, sentiment, confidence, sarcasm = analyze_emotion(text)

        st.subheader("📌 Hasil")

        st.markdown(f"""
        <div class="result-box blue">
        😡 Emosi : {emotion}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box green">
        💬 Sentimen : {sentiment}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box yellow">
        🎯 Confidence : {confidence}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box red">
        🧠 Sarkasme : {sarcasm}
        </div>
        """, unsafe_allow_html=True)

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

            st.dataframe(
                df.head(),
                use_container_width=True
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
            "⚠️ Belum ada data"
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

            color="Emosi",

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
            "⚠️ Belum ada riwayat"
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
