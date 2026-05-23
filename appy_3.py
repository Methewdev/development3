import streamlit as st
import pandas as pd

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Emotion AI Dashboard",
    page_icon="🧠",
    layout="wide"
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
    background:#081028;
}

[data-testid="stSidebar"] *{
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
BUTTON
===================================================== */

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

st.sidebar.title("🧠 Emotion AI")

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

st.title("📊 Dashboard Analisis Emosi")

st.caption(
    "Prototype Analisis Emosi & Sarkasme"
)

# =====================================================
# METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Analisis",
        "1,250"
    )

with col2:
    st.metric(
        "😊 Positif",
        "760"
    )

with col3:
    st.metric(
        "😡 Negatif",
        "390"
    )

with col4:
    st.metric(
        "🧠 Sarkasme",
        "100"
    )

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.subheader("📈 Distribusi Emosi")

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

    uploaded_file = st.file_uploader(
        "📂 Upload CSV",
        type=["csv"]
    )

    if uploaded_file:

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

# =====================================================
# STATISTIK
# =====================================================

elif menu == "Statistik":

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
