from django.http import JsonResponse

# Create your views here.


def all_event(request):
    """Get all events"""
    return JsonResponse(
        {
            "events": []
        }
    )


def event_detail(request, event_id):
    """Get event detail"""
    return JsonResponse(
        {
            "id": event_id,
        }
    )
