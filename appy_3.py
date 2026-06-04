import streamlit as st
import pandas as pd
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

# =====================
# PAGE CONFIG
# =====================

st.set_page_config(
    page_title="Emotion AI",
    layout="wide"
)

# =====================
# LOAD MODEL
# =====================

@st.cache_resource
def load_models():

    sentiment_tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    sentiment_model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    emotion_tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/emotion_model"
    )

    emotion_model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/emotion_model"
    )

    return (
        sentiment_tokenizer,
        sentiment_model,
        emotion_tokenizer,
        emotion_model
    )

(
    sentiment_tokenizer,
    sentiment_model,
    emotion_tokenizer,
    emotion_model
) = load_models()
