import streamlit as st
import torch
import re

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Analisis Emosi Livin",
    layout="centered"
)

st.title("📊 Analisis Emosi Nasabah Livin")

# =====================================================
# LOAD MODEL
# =====================================================

@st.cache_resource
def load_model():

    tokenizer = AutoTokenizer.from_pretrained(
        "./model"
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        "./model"
    )

    return tokenizer, model

tokenizer, model = load_model()

emotion_classes = [
    "cemas",
    "frustrasi",
    "marah",
    "netral",
    "puas",
    "senang"
]

# =====================================================
# CLEANING
# =====================================================

def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

# =====================================================
# PREDICT
# =====================================================

def predict_emotion(text):

    cleaned = clean_text(text)

    inputs = tokenizer(
        cleaned,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():

        outputs = model(**inputs)

    probs = torch.softmax(
        outputs.logits,
        dim=1
    )

    prediction = torch.argmax(
        probs,
        dim=1
    ).item()

    confidence = probs[0][prediction].item()

    emotion = emotion_classes[prediction]

    return emotion, confidence

# =====================================================
# INPUT
# =====================================================

text = st.text_area(
    "Masukkan ulasan nasabah"
)

# =====================================================
# BUTTON
# =====================================================

if st.button("Analisis"):

    emotion, confidence = predict_emotion(
        text
    )

    st.success(
        f"Emosi: {emotion}"
    )

    st.metric(
        "Confidence",
        f"{confidence*100:.2f}%"
    )
