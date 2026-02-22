from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = ["Negative", "Neutral", "Positive"]

def predict_sentiment(text: str):
    encoded = tokenizer(text, return_tensors="pt", truncation=True)
    output = model(**encoded)
    scores = torch.softmax(output.logits, dim=1)[0]

    sentiment_id = torch.argmax(scores).item()
    confidence = round(scores[sentiment_id].item(), 3)

    return LABELS[sentiment_id], confidence
