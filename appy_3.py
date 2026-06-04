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

def load_models():

   def load_models():

    try:

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

    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
        def load_models():

    sentiment_tokenizer = AutoTokenizer.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    sentiment_model = AutoModelForSequenceClassification.from_pretrained(
        "envidevelopment/sentiment_model"
    )

    return sentiment_tokenizer, sentiment_model
       sentiment_tokenizer, sentiment_model = load_models()
