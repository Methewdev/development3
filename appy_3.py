import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Dashboard Analisis Emosi",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: 'Poppins', sans-serif;
    background-color:#f4f7fc;
}

/* MAIN */

.main{
    background:#f4f7fc;
}

/* HIDE STREAMLIT */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* SIDEBAR */

[data-testid="stSidebar"]{
    background:#111827;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* CARD */

.card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 5px 20px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

.card h3{
    color:#777;
    margin-bottom:10px;
}

.card h1{
    font-size:38px;
}

/* RESULT */

.result-box{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0 5px 20px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

.result-item{
    background:#f4f7fc;
    padding:15px;
    border-radius:15px;
    margin-bottom:15px;
}

/* TEXT AREA */

textarea{
    border-radius:15px !important;
}

/* BUTTON */

.stButton button{
    width:100%;
    height:55px;
    border:none;
    border-radius:15px;
    background:#2563eb;
    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton button:hover{
    background:#1d4ed8;
    color:white;
}

/* TABLE */

[data-testid="stDataFrame"]{
    border-radius:15px;
    overflow:hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📊 Emotion AI")

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Analisis Satuan",
        "Bulk CSV",
        "Statistik"
    ]
)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Dashboard Analisis Emosi")

st.caption(
    "Prototype Analisis Emosi & Sarkasme Nasabah"
)

# =====================================================
# DASHBOARD CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="card">
        <h3>Total Data</h3>
        <h1>1,250</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="card">
        <h3>Positif</h3>
        <h1>760</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="card">
        <h3>Negatif</h3>
        <h1>390</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="card">
        <h3>Sarkasme</h3>
        <h1>100</h1>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# CONTENT
# =====================================================

left, right = st.columns([2,1])

# =====================================================
# LEFT CONTENT
# =====================================================

with left:

    st.markdown("""
    <div class="card">
        <h2>✍️ Analisis Ulasan</h2>
    </div>
    """, unsafe_allow_html=True)

    text = st.text_area(
        "",
        height=220,
        placeholder="Masukkan ulasan nasabah..."
    )

    analyze = st.button("🔍 Analisis Sekarang")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h2>📂 Upload CSV</h2>
        <p>Upload file CSV untuk analisis bulk</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["csv"]
    )

# =====================================================
# RIGHT CONTENT
# =====================================================

with right:

    st.markdown("""
    <div class="result-box">
        <h2>📌 Hasil Analisis</h2>

        <div class="result-item">
            <h3>😡 Emosi</h3>
            <p>MARAH</p>
        </div>

        <div class="result-item">
            <h3>🎯 Confidence</h3>
            <p>99.86%</p>
        </div>

        <div class="result-item">
            <h3>💬 Sentimen</h3>
            <p>Negatif</p>
        </div>

        <div class="result-item">
            <h3>🧠 Sarkasme</h3>
            <p>Tidak Terdeteksi</p>
        </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# TABLE RESULT
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h2>📋 Hasil Analisis Bulk</h2>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DUMMY DATA
# =====================================================

data = {
    "No": [1,2,3],
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
}

df = pd.DataFrame(data)

st.dataframe(
    df,
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "Prototype Analisis Emosi, Sentimen & Sarkasme Mobile Banking"
)
