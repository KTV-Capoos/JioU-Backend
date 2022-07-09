from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from utils import allow_methods

from .models import UserInfo


# Create your views here.
@allow_methods(["POST"])
def login_request(request) -> JsonResponse:
    """Login user"""
    post_dict = request.POST
    username = post_dict.get("username")
    password = post_dict.get("password")

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)
    login(request, user)
    return JsonResponse({"success": True})


@allow_methods(["POST"])
def logout_request(request) -> JsonResponse:
    logout(request)
    return JsonResponse({"success": True})


def _add_user(
    username,
    password,
    gender,
    dob,
    mobile_number,
    nok,
    religion,
    nationality,
    ethnicity,
    medical_conditions="",
    allergies="",
    dietary_restrictions="",
    email="",
    **_
) -> JsonResponse:
    """Add a user to login"""
    try:
        user = User.objects.create(username=username, email=email, password=password)
    except IntegrityError:
        return None

    UserInfo.objects.create(
        user=user,
        gender=gender,
        dob=dob,
        mobile_number=mobile_number,
        nok=nok,
        religion=religion,
        nationality=nationality,
        ethnicity=ethnicity,
        medical_conditions=medical_conditions,
        allergies=allergies,
        dietary_restrictions=dietary_restrictions,
    )
    return user


@allow_methods(["POST"])
def signup(request) -> JsonResponse:
    """User Signup for django"""
    user = _add_user(**dict(request.POST.items()))
    if user is None:
        return JsonResponse({"error": "Username already exists"}, status=409)
    return JsonResponse({"success": True})
