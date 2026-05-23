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

    min-height:180px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.4);

}

.metric-title{

    color:#cbd5e1;

    font-size:22px;

    margin-bottom:20px;

    font-weight:500;

}

.metric-value{

    color:white;

    font-size:54px;

    font-weight:bold;

}

/* =====================================================
CONTENT BOX
===================================================== */

.content-box{

    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.90)
    );

    padding:25px;

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.08);

    margin-top:20px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.3);

}

/* =====================================================
RESULT BOX
===================================================== */

.result-box{

    background:#111827;

    padding:20px;

    border-radius:18px;

    margin-bottom:15px;

    border:1px solid rgba(255,255,255,0.05);

}

.result-title{

    color:#94a3b8;

    margin-bottom:10px;

    font-size:18px;

}

.result-value{

    color:white;

    font-size:24px;

    font-weight:bold;

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
DATAFRAME
===================================================== */

[data-testid="stDataFrame"]{

    border-radius:20px;

    overflow:hidden;

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

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTION
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

    if "error" in text:
        emotion = "Frustrasi"
        sentiment = "Negatif"

    if "gagal" in text:
        emotion = "Marah"
        sentiment = "Negatif"

    if "cepat" in text:
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

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">
            📊 Total Analisis
        </div>

        <div class="metric-value">
            1250
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">
            😊 Positif
        </div>

        <div class="metric-value">
            760
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">
            😡 Negatif
        </div>

        <div class="metric-value">
            390
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">
            🧠 Sarkasme
        </div>

        <div class="metric-value">
            100
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.markdown("""
    <div class="content-box">
        <h2>📊 Dashboard Utama</h2>
        <p>Upload data terlebih dahulu untuk melihat visualisasi</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    left, right = st.columns([2,1])

    with left:

        st.markdown("""
        <div class="content-box">
            <h2>✍️ Input Ulasan</h2>
        </div>
        """, unsafe_allow_html=True)

        text = st.text_area(
            "",
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

        st.markdown("""
        <div class="content-box">
            <h2>📌 Hasil Analisis</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">
            <div class="result-title">
                😡 Emosi
            </div>

            <div class="result-value">
                {emotion}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">
            <div class="result-title">
                💬 Sentimen
            </div>

            <div class="result-value">
                {sentiment}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">
            <div class="result-title">
                🎯 Confidence
            </div>

            <div class="result-value">
                {confidence}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-box">
            <div class="result-title">
                🧠 Sarkasme
            </div>

            <div class="result-value">
                {sarcasm}
            </div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# BULK CSV
# =====================================================

elif menu == "Bulk CSV":

    st.markdown("""
    <div class="content-box">
        <h2>📂 Upload CSV</h2>
        <p>Upload file CSV untuk analisis massal</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.success("✅ File berhasil diupload")

        st.dataframe(
            df,
            use_container_width=True
        )

        if st.button("🚀 Mulai Analisis"):

            results = []

            for i in range(len(df)):

                text = str(df.iloc[i,0])

                emotion, sentiment, confidence, sarcasm = analyze_emotion(text)

                results.append({

                    "Text": text,
                    "Emosi": emotion,
                    "Sentimen": sentiment,
                    "Confidence": confidence,
                    "Sarkasme": sarcasm

                })

            result_df = pd.DataFrame(results)

            st.success("✅ Analisis selesai")

            # =============================================
            # TABEL HASIL
            # =============================================

            st.markdown("""
            <div class="content-box">
                <h2>📋 Hasil Analisis</h2>
            </div>
            """, unsafe_allow_html=True)

            st.dataframe(
                result_df,
                use_container_width=True
            )

            # =============================================
            # DISTRIBUSI EMOSI
            # =============================================

            st.markdown("""
            <div class="content-box">
                <h2>📈 Distribusi Emosi</h2>
            </div>
            """, unsafe_allow_html=True)

            emotion_count = result_df["Emosi"].value_counts()

            emotion_chart = pd.DataFrame({

                "Emosi": emotion_count.index,
                "Jumlah": emotion_count.values

            })

            st.dataframe(
                emotion_chart,
                use_container_width=True
            )

            # =============================================
            # DOWNLOAD CSV
            # =============================================

            csv = result_df.to_csv(index=False)

            st.download_button(

                label="⬇️ Download Hasil CSV",

                data=csv,

                file_name="hasil_analisis.csv",

                mime="text/csv"

            )

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

    st.markdown("""
    <div class="content-box">
        <h2>📈 Statistik Analisis</h2>
        <p>Statistik akan muncul setelah proses bulk CSV</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "Riwayat":

    history = pd.DataFrame({

        "Tanggal":[
            "31 Mei 2026",
            "30 Mei 2026",
            "29 Mei 2026"
        ],

        "Ulasan":[
            "Aplikasi bagus tapi sering error",
            "Transfer cepat dan mudah",
            "Maintenance terus sangat mengganggu"
        ],

        "Emosi":[
            "Frustrasi",
            "Senang",
            "Marah"
        ],

        "Sentimen":[
            "Negatif",
            "Positif",
            "Negatif"
        ]

    })

    st.markdown("""
    <div class="content-box">
        <h2>📜 Riwayat Analisis</h2>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        history,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "© 2026 Emotion AI Dashboard"
)
