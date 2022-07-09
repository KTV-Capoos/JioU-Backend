import datetime
from django.http import JsonResponse

from .models import Event


# Create your views here.
def all_event(request):
    """Get all events"""
    future_events = Event.objects.filter(
        event_date__gte=datetime.date.today() - datetime.timedelta(days=3)
    ).all()
    event_list = list(
        map(
            lambda event: event.toCardDict(),
            future_events
        )
    ),
    return JsonResponse(
        {'events': event_list[0]},
        safe=False
    )


def event_detail(request, event_id):
    """Get event detail"""
    try:
        event = Event.objects.get(event_id=event_id)
        return JsonResponse(
            event.toDict(),
            safe=False,
        )
    except Event.DoesNotExist:
        return JsonResponse(
            {'error': 'Event not found'},
            status=404
        )
