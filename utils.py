from transformers import pipeline

# Sentiment
sentiment_pipe = pipeline(
    "text-classification",
    model="w11wo/indonesian-roberta-base-sentiment-classifier"
)

# Emotion
emotion_pipe = pipeline(
    "text-classification",
    model="USERNAME/emotion_model"
)

def predict_sentiment(text):

    result = sentiment_pipe(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }


def predict_emotion(text):

    result = emotion_pipe(text)[0]

    return {
        "label": result["label"],
        "score": round(result["score"] * 100, 2)
    }
