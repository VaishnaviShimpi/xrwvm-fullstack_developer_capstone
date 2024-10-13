from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CarMake, CarModel
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate  # Uncomment and ensure initiate function is imported correctly

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
def logout_request(request):
    logout(request)
    data = {"userName": "", "status": "Logged out"}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is a new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

@csrf_exempt
def get_cars(request):
    # Check if there are any car makes or models in the database
    count = CarMake.objects.filter().count()
    if count == 0:
        print("Database is empty, initiating population...")
        initiate()  # Populate the database if empty

    # Fetch all car models and their makes
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        car_data = {
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
            "Year": car_model.year
        }
        # Add debugging print statement
        print(f"Fetched CarModel: {car_data}")
        cars.append(car_data)

    # If the list is empty, print a message
    if not cars:
        print("No car data found in the database.")

    return JsonResponse({"CarModels": cars})