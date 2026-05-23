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
    font-family: 'Segoe UI', sans-serif;
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

    font-size:24px;

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
            1,250
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

    left, right = st.columns([2,1])

    # =================================================
    # LEFT
    # =================================================

    with left:

        st.markdown("""
        <div class="content-box">
            <h2>📈 Distribusi Emosi</h2>
        </div>
        """, unsafe_allow_html=True)

        chart_data = pd.DataFrame({

            "Emosi":[
                "Senang",
                "Puas",
                "Netral",
                "Marah",
                "Frustrasi",
                "Cemas"
            ],

            "Jumlah":[
                480,
                280,
                200,
                150,
                90,
                50
            ]

        })

        st.bar_chart(
            chart_data.set_index("Emosi")
        )

    # =================================================
    # RIGHT
    # =================================================

    with right:

        st.markdown("""
        <div class="content-box">
            <h2>⚡ Quick Action</h2>
        </div>
        """, unsafe_allow_html=True)

        st.button("✍️ Analisis Satuan")

        st.button("📂 Upload CSV")

        st.button("📈 Lihat Statistik")

        st.button("⬇️ Export Laporan")

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "Analisis Satuan":

    left, right = st.columns([2,1])

    # =================================================
    # INPUT
    # =================================================

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

    # =================================================
    # RESULT
    # =================================================

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
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.success("✅ File berhasil diupload")

        st.dataframe(
            df,
            use_container_width=True
        )

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

    st.markdown("""
    <div class="content-box">
        <h2>📈 Statistik Analisis</h2>
    </div>
    """, unsafe_allow_html=True)

    stats_data = pd.DataFrame({

        "Hari":[
            "Sen",
            "Sel",
            "Rab",
            "Kam",
            "Jum"
        ],

        "Positif":[
            120,
            150,
            130,
            170,
            200
        ]

    })

    st.line_chart(
        stats_data.set_index("Hari")
    )

# =====================================================
# RIWAYAT
# =====================================================

elif menu == "Riwayat":

    st.markdown("""
    <div class="content-box">
        <h2>📜 Riwayat Analisis</h2>
    </div>
    """, unsafe_allow_html=True)

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
