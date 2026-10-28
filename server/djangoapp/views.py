import json
import logging
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('userName') or data.get('username') or ''
    password = data.get('password') or ''

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Authentication Failed"}, status=401)


@csrf_exempt
def logout_request(request):
    username = request.user.username if request.user.is_authenticated else ""
    if not username and request.session.get('username'):
        username = request.session.get('username')
    logout(request)
    return JsonResponse({
        "userName": username,
        "status": "Logged out",
        "success": True,
        "message": "Logged out successfully"
    })


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = data.get('userName') or data.get('username')
    password = data.get('password')
    first_name = data.get('firstName') or data.get('first_name', '')
    last_name = data.get('lastName') or data.get('last_name', '')
    email = data.get('email', '')

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    try:
        User.objects.get(username=username)
        return JsonResponse({"userName": username, "error": "Already Registered"})
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})


def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make').all()
    cars = []
    for model in car_models:
        cars.append({
            "CarModel": model.name,
            "CarMake": model.car_make.name,
            "Type": model.type,
            "Year": model.year,
        })
    return JsonResponse({"status": 200, "CarModels": cars})


def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        dealer_list = [dealership] if isinstance(dealership, dict) else dealership
        return JsonResponse({"status": 200, "dealer": dealer_list})
    return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        if reviews is None:
            reviews = []

        for review_detail in reviews:
            rev_text = review_detail.get('review', '')
            sentiment_resp = analyze_review_sentiments(rev_text)
            if sentiment_resp and 'sentiment' in sentiment_resp:
                review_detail['sentiment'] = sentiment_resp['sentiment']
            else:
                review_detail['sentiment'] = 'neutral'

        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST.dict()

    try:
        post_response = post_review(data)
        return JsonResponse({
            "status": 200,
            "message": "Review posted successfully",
            "result": post_response,
            "review": data
        })
    except Exception as e:
        logger.error(f"Error in posting review: {e}")
        return JsonResponse({"status": 500, "message": "Error posting review"}, status=500)
