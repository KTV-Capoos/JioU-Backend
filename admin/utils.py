from typing import Callable
from django.http import JsonResponse, HttpRequest


def login_required(func: Callable[..., JsonResponse]):
    def wrapper(request: HttpRequest, *args, **kwargs) -> JsonResponse:
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return JsonResponse({"error": "Login required"}, status=401)

    return wrapper


def allow_methods(methods):
    def func_wrapper(func: Callable[..., JsonResponse]):
        def wrapper(request: HttpRequest, *args, **kwargs) -> JsonResponse:
            if request.method in methods:
                return func(request, *args, **kwargs)
            return JsonResponse({"error": "Method not allowed"}, status=405)

        return wrapper

    return func_wrapper
