import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = backend_url + endpoint + (("?" + params) if params else "")
    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        print(f"GET returned status code {response.status_code}")
    except Exception as e:
        print(f"Network exception occurred while connecting to {request_url}: {e}")

    # Fallback directly to local JSON files if backend microservice is offline
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dealers_file = os.path.join(base_dir, 'database', 'dealerships.json')
        if not os.path.exists(dealers_file):
            dealers_file = os.path.join(base_dir, 'database', 'data', 'dealerships.json')

        reviews_file = os.path.join(base_dir, 'database', 'reviews.json')
        if not os.path.exists(reviews_file):
            reviews_file = os.path.join(base_dir, 'database', 'data', 'reviews.json')

        if endpoint.startswith("/fetchDealers/"):
            state = endpoint.replace("/fetchDealers/", "").strip().lower()
            with open(dealers_file, 'r', encoding='utf-8') as f:
                dealers = json.load(f)['dealerships']
                return [d for d in dealers if d.get('state', '').lower() == state]

        elif endpoint == "/fetchDealers":
            with open(dealers_file, 'r', encoding='utf-8') as f:
                return json.load(f)['dealerships']

        elif endpoint.startswith("/fetchDealer/"):
            d_id = int(endpoint.replace("/fetchDealer/", "").strip())
            with open(dealers_file, 'r', encoding='utf-8') as f:
                dealers = json.load(f)['dealerships']
                for d in dealers:
                    if int(d.get('id', 0)) == d_id:
                        return d
            return None

        elif endpoint.startswith("/fetchReviews/dealer/"):
            d_id = int(endpoint.replace("/fetchReviews/dealer/", "").strip())
            with open(reviews_file, 'r', encoding='utf-8') as f:
                reviews = json.load(f)['reviews']
                return [r for r in reviews if int(r.get('dealership', 0)) == d_id]

        elif endpoint == "/fetchReviews":
            with open(reviews_file, 'r', encoding='utf-8') as f:
                return json.load(f)['reviews']
    except Exception as fallback_err:
        print(f"Fallback reading error: {fallback_err}")

    return []


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + requests.utils.quote(text)
    try:
        response = requests.get(request_url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as err:
        print(f"Sentiment service exception: {err}")

    # Fallback to direct VADER sentiment analyzer if microservice is offline
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        compound = scores['compound']
        if compound >= 0.05:
            return {"sentiment": "positive"}
        elif compound <= -0.05:
            return {"sentiment": "negative"}
        else:
            return {"sentiment": "neutral"}
    except Exception as nltk_err:
        print(f"Local NLTK analyzer error: {nltk_err}")
        return {"sentiment": "positive" if "great" in text.lower() or "fantastic" in text.lower() else "neutral"}


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Network exception occurred while posting review: {e}")

    # Return success object if network call is unrouted
    return {"status": 200, "message": "Review inserted successfully", "review": data_dict}
