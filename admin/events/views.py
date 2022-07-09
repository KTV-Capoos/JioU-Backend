import datetime

from django.http import JsonResponse
from utils import allow_methods, login_required

from .models import Event


# Create your views here.
@login_required
@allow_methods(["GET"])
def all_event(_) -> JsonResponse:
    """Get all events"""
    future_events = Event.objects.filter(
        event_date__gte=datetime.date.today() - datetime.timedelta(days=3)
    ).all()
    event_list = (list(map(lambda event: event.toCardDict(), future_events)),)
    return JsonResponse({"events": event_list[0]}, safe=False)


@login_required
@allow_methods(["GET"])
def event_detail(_, event_id) -> JsonResponse:
    """Get event detail"""
    try:
        event = Event.objects.get(event_id=event_id)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)
    else:
        return JsonResponse(
            event.toDict(),
            safe=False,
        )
