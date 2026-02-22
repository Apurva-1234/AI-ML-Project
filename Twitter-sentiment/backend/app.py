import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from collections import defaultdict
from storage import predictions, add_prediction

from sentiment import predict_sentiment
from logger import logger
import config

app = FastAPI(title="Twitter Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class TweetInput(BaseModel):
    tweet: str

from rate_limit import is_rate_limited

@app.post("/predict")
def predict(data: TweetInput, request: Request):
    if is_rate_limited(request.client.host):
        raise HTTPException(429, "Too many requests. Please wait a minute.")
        
    start = time.time()

    if not data.tweet.strip():
        raise HTTPException(400, "Empty tweet")

    if len(data.tweet) > config.MAX_TEXT_LENGTH:
        raise HTTPException(400, "Tweet too long")

    try:
        sentiment, confidence = predict_sentiment(data.tweet)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(500, "Prediction failed")

    latency = round((time.time() - start) * 1000, 2)
    add_prediction(sentiment)
    logger.info(
        f"IP={request.client.host} | Sentiment={sentiment} | Confidence={confidence}"
    )

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "latency_ms": latency
    }

@app.get("/stats")
def get_stats():
    buckets = defaultdict(lambda: {"pos": 0, "neu": 0, "neg": 0})

    for p in predictions:
        minute = p["time"].strftime("%H:%M")
        sentiment = p["sentiment"]
        if sentiment == "Positive":
            buckets[minute]["pos"] += 1
        elif sentiment == "Neutral":
            buckets[minute]["neu"] += 1
        else:
            buckets[minute]["neg"] += 1

    response = []
    for time, counts in buckets.items():
        total = counts["pos"] + counts["neu"] + counts["neg"]
        if total == 0:
            continue

        response.append({
            "time": time,
            "positive_count": counts["pos"],
            "neutral_count": counts["neu"],
            "negative_count": counts["neg"],
            "total_count": total,
            "positive_pct": round((counts["pos"] / total) * 100, 2),
            "neutral_pct": round((counts["neu"] / total) * 100, 2),
            "negative_pct": round((counts["neg"] / total) * 100, 2)
        })

    return response


@app.get("/recent")
def get_recent_predictions():
    
    recent = predictions[-10:] if predictions else []
    
    
    formatted_recent = []
    for p in recent:
        formatted_recent.append({
            "time": p["time"].isoformat(),
            "sentiment": p["sentiment"]
        })
    
    return formatted_recent