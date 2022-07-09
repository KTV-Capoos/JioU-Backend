from django.http import JsonResponse


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Login required'}, status=401)
    return wrapper