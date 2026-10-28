import os
import json
from flask import Flask, jsonify, request
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

app = Flask("Sentiment Analyzer")
sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze/<text> to get the sentiment"


@app.get('/analyze/<path:input_txt>')
def analyze_sentiment(input_txt):
    scores = sia.polarity_scores(input_txt)
    compound = scores['compound']
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])

    # Standard VADER sentiment classification
    if compound >= 0.05:
        res = "positive"
    elif compound <= -0.05:
        res = "negative"
    else:
        res = "neutral"

    # Fallback to direct polarity component comparison if needed
    if compound == 0.0:
        if neg > pos and neg > neu:
            res = "negative"
        elif neu > neg and neu > pos:
            res = "neutral"
        elif pos > neg and pos > neu:
            res = "positive"

    return jsonify({"sentiment": res})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
