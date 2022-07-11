from typing import Type
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse

from .models import UserInfo
from utils import allow_methods, login_required


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
    full_name,
    password,
    gender,
    email,
    dob,
    mobile_number,
    religion,
    nationality,
    ethnicity,
    nok="",
    medical_conditions="",
    allergies="",
    dietary_restrictions="",
    **_
) -> JsonResponse:
    """Add a user to login"""
    try:
        user: User = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
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
        full_name=full_name,
    )
    return user


@allow_methods(["POST"])
def signup(request) -> JsonResponse:
    """User Signup for django"""
    try:
        user = _add_user(**dict(request.POST.items()))
    except TypeError:
        return JsonResponse({"error": "Missing form values"}, status=400)
    if user is None:
        return JsonResponse({"error": "Username already exists"}, status=409)
    return JsonResponse({"success": True})


@login_required
@allow_methods(["GET"])
def get_info(request) -> JsonResponse:
    """Get user info"""
    user = request.user
    user_info = UserInfo.objects.get(user=user)
    return JsonResponse(user_info.to_dict())
