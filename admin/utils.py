from django.http import JsonResponse


def login_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return JsonResponse({'error': 'Login required'}, status=401)
    return wrapper


def allow_methods(methods):
    def func_wrapper(func):
        def wrapper(request, *args, **kwargs):
            if request.method in methods:
                return func(request, *args, **kwargs)
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return wrapper
    return func_wrapper
