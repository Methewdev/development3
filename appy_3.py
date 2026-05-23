import streamlit as st
import pandas as pd
import re

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
# DUMMY DATA
# =====================================================

dummy_history = pd.DataFrame({
    "Tanggal": [
        "31 Mei 2026",
        "30 Mei 2026",
        "29 Mei 2026"
    ],
    "Ulasan": [
        "Aplikasi bagus tapi sering error",
        "Transfer cepat dan mudah",
        "Maintenance terus sangat mengganggu"
    ],
    "Emosi": [
        "Frustrasi",
        "Senang",
        "Marah"
    ],
    "Confidence": [
        "98.22%",
        "99.01%",
        "97.65%"
    ],
    "Sentimen": [
        "Negatif",
        "Positif",
        "Negatif"
    ],
    "Sarkasme": [
        "Ya",
        "Tidak",
        "Tidak"
    ]
})

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"] {
    background-color: #050816;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Hide Streamlit Menu */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* =====================================================
SIDEBAR
===================================================== */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #081028 0%,
        #09142d 100%
    );
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] * {
    color: white;
}

/* =====================================================
TITLE
===================================================== */

.main-title {
    font-size: 38px;
    font-weight: 700;
    color: white;
    margin-bottom: 5px;
}

.sub-title {
    color: #9ca3af;
    margin-bottom: 30px;
}

/* =====================================================
CARDS
===================================================== */

.card {

    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.90)
    );

    border: 1px solid rgba(255,255,255,0.08);

    padding: 25px;

    border-radius: 24px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.4);

    transition: 0.3s;

}

.card:hover {
    transform: translateY(-5px);
}

.card-title {
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 10px;
}

.card-value {
    font-size: 42px;
    font-weight: bold;
    color: white;
}

/* =====================================================
CONTENT BOX
===================================================== */

.content-box {

    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.90)
    );

    border: 1px solid rgba(255,255,255,0.08);

    padding: 25px;

    border-radius: 24px;

    margin-top: 20px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.3);

}

/* =====================================================
RESULT ITEM
===================================================== */

.result-item {

    background: #111827;

    padding: 18px;

    border-radius: 18px;

    margin-bottom: 15px;

    border: 1px solid rgba(255,255,255,0.05);

}

/* =====================================================
BUTTON
===================================================== */

.stButton button {

    width: 100%;
    height: 55px;

    border: none;

    border-radius: 18px;

    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

    color: white;

    font-size: 18px;
    font-weight: 600;

}

.stButton button:hover {

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    );

    color: white;

}

/* =====================================================
TEXT AREA
===================================================== */

textarea {

    background-color: #0f172a !important;

    color: white !important;

    border-radius: 20px !important;

    border: 1px solid rgba(255,255,255,0.1) !important;

}

/* =====================================================
UPLOAD FILE
===================================================== */

[data-testid="stFileUploader"] {

    background: #111827;

    border-radius: 20px;

    padding: 20px;

    border: 1px dashed rgba(255,255,255,0.2);

}

/* =====================================================
DATAFRAME
===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);

}

</style>
""", unsafe_allow_html=True)

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
        "🏠 Dashboard",
        "✍️ Analisis Satuan",
        "📂 Bulk CSV",
        "📈 Statistik",
        "📜 Riwayat"
    ]
)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
Dashboard Analisis Emosi
</div>

<div class="sub-title">
Prototype Analisis Emosi & Sarkasme berbasis Transformer
</div>
""", unsafe_allow_html=True)

# =====================================================
# METRIC CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="card">
        <div class="card-title">
        📊 Total Analisis
        </div>

        <div class="card-value">
        1,250
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
        <div class="card-title">
        😊 Positif
        </div>

        <div class="card-value">
        760
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">
        <div class="card-title">
        😡 Negatif
        </div>

        <div class="card-value">
        390
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="card">
        <div class="card-title">
        🧠 Sarkasme
        </div>

        <div class="card-value">
        100
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

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
            "Emosi": [
                "Senang",
                "Puas",
                "Netral",
                "Marah",
                "Frustrasi",
                "Cemas"
            ],
            "Jumlah": [
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

        if st.button("✍️ Analisis Satuan"):
            st.success("Menu Analisis Satuan dipilih")

        if st.button("📂 Upload CSV"):
            st.success("Menu Upload CSV dipilih")

        if st.button("📈 Statistik"):
            st.success("Menu Statistik dipilih")

        if st.button("⬇️ Export Laporan"):
            st.success("Export berhasil")

# =====================================================
# ANALISIS SATUAN
# =====================================================

elif menu == "✍️ Analisis Satuan":

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

        emotion = "MARAH"
        confidence = "99.86%"
        sentiment = "Negatif"
        sarcasm = "Tidak"

        if analyze:

            text_lower = text.lower()

            if "bagus" in text_lower:
                emotion = "SENANG"
                sentiment = "Positif"

            if "error" in text_lower:
                emotion = "FRUSTRASI"
                sentiment = "Negatif"

            if "gagal" in text_lower:
                emotion = "MARAH"
                sentiment = "Negatif"

        st.markdown(f"""
        <div class="content-box">

            <h2>📌 Hasil Analisis</h2>

            <div class="result-item">
                <h3>😡 Emosi</h3>
                <p>{emotion}</p>
            </div>

            <div class="result-item">
                <h3>🎯 Confidence</h3>
                <p>{confidence}</p>
            </div>

            <div class="result-item">
                <h3>💬 Sentimen</h3>
                <p>{sentiment}</p>
            </div>

            <div class="result-item">
                <h3>🧠 Sarkasme</h3>
                <p>{sarcasm}</p>
            </div>

        </div>
        """, unsafe_allow_html=True)

# =====================================================
# BULK CSV
# =====================================================

elif menu == "📂 Bulk CSV":

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

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.success(
            "✅ File berhasil diupload"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        if st.button("🚀 Mulai Analisis"):

            results = []

            for i in range(len(df)):

                text = str(df.iloc[i,0])

                emotion = "Netral"
                sentiment = "Netral"

                if "bagus" in text.lower():
                    emotion = "Senang"
                    sentiment = "Positif"

                elif "error" in text.lower():
                    emotion = "Frustrasi"
                    sentiment = "Negatif"

                elif "gagal" in text.lower():
                    emotion = "Marah"
                    sentiment = "Negatif"

                results.append({
                    "Text": text,
                    "Emosi": emotion,
                    "Sentimen": sentiment
                })

            result_df = pd.DataFrame(results)

            st.success(
                "✅ Analisis selesai"
            )

            st.dataframe(
                result_df,
                use_container_width=True
            )

# =====================================================
# STATISTIK
# =====================================================

elif menu == "📈 Statistik":

    st.markdown("""
    <div class="content-box">
        <h2>📈 Statistik Analisis</h2>
    </div>
    """, unsafe_allow_html=True)

    stats_data = pd.DataFrame({

        "Hari": [
            "Sen",
            "Sel",
            "Rab",
            "Kam",
            "Jum"
        ],

        "Positif": [
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

elif menu == "📜 Riwayat":

    st.markdown("""
    <div class="content-box">
        <h2>📜 Riwayat Analisis</h2>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        dummy_history,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "© 2026 Emotion AI Dashboard"
)
