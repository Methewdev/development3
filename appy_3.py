
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

st.set_page_config(page_title="Emotion AI Dashboard", page_icon="🧠", layout="wide")

# ================= SESSION =================
if "single_result" not in st.session_state:
    st.session_state.single_result = None
if "bulk_result" not in st.session_state:
    st.session_state.bulk_result = pd.DataFrame()
if "bulk_history" not in st.session_state:
    st.session_state.bulk_history = []

# ================= LOAD EMOTION MODEL =================
@st.cache_resource
def load_emotion_model():
    MODEL_PATH = "model3"   # folder model Anda

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    model.eval()
    return tokenizer, model

# Aktifkan jika folder model3 tersedia
# emotion_tokenizer, emotion_model = load_emotion_model()

# ================= DEMO SENTIMENT =================
def predict_sentiment(text):
    text = str(text).lower()

    if any(x in text for x in ["bagus","mantap","baik","hebat","puas"]):
        return "positive", 0.98

    if any(x in text for x in ["buruk","gagal","error","lambat","kecewa"]):
        return "negative", 0.98

    return "neutral", 0.95

# ================= EMOTION =================
def predict_emotion(text):

    # HAPUS BAGIAN INI JIKA MODEL SUDAH AKTIF
    text = str(text).lower()

    if "marah" in text or "kesal" in text:
        return "anger",0.95
    if "takut" in text or "cemas" in text:
        return "fear",0.95
    if "senang" in text or "bahagia" in text or "bagus" in text:
        return "happy",0.95
    if "cinta" in text or "sayang" in text:
        return "love",0.95

    return "sadness",0.95

    """
    # AKTIFKAN SAAT MODEL SUDAH ADA

    inputs = emotion_tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )

    with torch.no_grad():
        outputs = emotion_model(**inputs)

        probs = F.softmax(outputs.logits, dim=1)

        pred = torch.argmax(
            probs,
            dim=1
        ).item()

        confidence = probs[0,pred].item()

    emotion = emotion_model.config.id2label[pred]

    return emotion, confidence
    """

# ================= FILE LOADER =================
def load_file(uploaded_file):

    if uploaded_file.name.lower().endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    encodings = [
        "latin1",
        "cp1252",
        "ISO-8859-1",
        "utf-8",
        "utf-8-sig"
    ]

    separators = [";", ","]

    for enc in encodings:
        for sep in separators:

            try:

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    encoding=enc,
                    sep=sep,
                    engine="python",
                    on_bad_lines="skip"
                )

                if len(df.columns) > 1:
                    return df

            except Exception:
                pass

    raise Exception("File tidak dapat dibaca")

# ================= SIDEBAR =================
with st.sidebar:

    menu = st.radio(
        "Menu",
        ["Dashboard","Analisis Satuan","Bulk CSV","Statistik","Riwayat"]
    )

    if st.button("🔄 Refresh Dashboard"):
        st.session_state.bulk_result = pd.DataFrame()
        st.session_state.bulk_history = []
        st.session_state.single_result = None
        st.rerun()

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    df = st.session_state.bulk_result

    if len(df) == 0:
        st.info("Belum ada data hasil Bulk CSV")
        st.stop()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total", len(df))
    c2.metric("Positif", len(df[df["sentiment"]=="positive"]))
    c3.metric("Negatif", len(df[df["sentiment"]=="negative"]))
    c4.metric("Netral", len(df[df["sentiment"]=="neutral"]))

    if "emotion" in df.columns:

        emo = df["emotion"].value_counts().to_dict()

        e1,e2,e3,e4,e5 = st.columns(5)

        e1.metric("😊 Happy", emo.get("happy",0))
        e2.metric("😡 Anger", emo.get("anger",0))
        e3.metric("😨 Fear", emo.get("fear",0))
        e4.metric("😢 Sadness", emo.get("sadness",0))
        e5.metric("❤️ Love", emo.get("love",0))

# ================= ANALISIS SATUAN =================
elif menu == "Analisis Satuan":

    st.title("📝 Analisis Satuan")

    b1,b2 = st.columns(2)

    with b1:
        analisis = st.button("🔍 Analisis")

    with b2:
        refresh = st.button("🔄 Refresh Analisis")

    if refresh:
        st.session_state.single_result = None
        st.rerun()

    text = st.text_area("Masukkan Ulasan", height=200)

    if analisis and text.strip():

        sentiment, score = predict_sentiment(text)
        emotion, emotion_score = predict_emotion(text)

        st.session_state.single_result = {
            "text": text,
            "sentiment": sentiment,
            "emotion": emotion,
            "score": score,
            "emotion_score": emotion_score
        }

    if st.session_state.single_result:

        r = st.session_state.single_result

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Sentimen", r["sentiment"].upper())
        c2.metric("Emosi", r["emotion"].upper())
        c3.metric("Conf. Sentimen", f"{r['score']*100:.2f}%")
        c4.metric("Conf. Emosi", f"{r['emotion_score']*100:.2f}%")

# ================= BULK CSV =================
elif menu == "Bulk CSV":

    st.title("📂 Bulk CSV")

    uploaded_file = st.file_uploader(
        "Upload CSV/XLSX",
        type=["csv","xlsx"]
    )

    if uploaded_file:

        df = load_file(uploaded_file)

        st.dataframe(df.head())

        text_col = "content" if "content" in df.columns else st.selectbox(
            "Pilih Kolom Ulasan",
            df.columns
        )

        if st.button("🚀 Proses Analisis"):

            sentiments=[]
            emotions=[]
            scores=[]
            emotion_scores=[]

            for txt in df[text_col]:

                s,sc = predict_sentiment(str(txt))
                e,es = predict_emotion(str(txt))

                sentiments.append(s)
                emotions.append(e)
                scores.append(sc)
                emotion_scores.append(es)

            df["sentiment"] = sentiments
            df["emotion"] = emotions
            df["score"] = scores
            df["emotion_score"] = emotion_scores

            st.session_state.bulk_result = df

            st.session_state.bulk_history.append({
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "rows": len(df)
            })

            st.success("Analisis selesai")
            st.dataframe(df)

# ================= STATISTIK =================
elif menu == "Statistik":

    df = st.session_state.bulk_result

    if len(df):

        st.plotly_chart(
            px.pie(df,names="sentiment"),
            use_container_width=True
        )

# ================= RIWAYAT =================
elif menu == "Riwayat":

    st.dataframe(
        pd.DataFrame(st.session_state.bulk_history),
        use_container_width=True
    )
