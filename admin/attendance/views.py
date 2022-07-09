import datetime
from django.http import JsonResponse

from utils import login_required, allow_methods
from events.models import Event
from .models import Attendance


# Create your views here.
@login_required
@allow_methods(['GET'])
def get_user_attendance(request) -> JsonResponse:
    """Get the events that the user is participating in."""
    participation_events = Attendance.objects.filter(
        user=request.user
    ).order_by('event__event_date').all()
    return JsonResponse({'events': [event.toDict() for event in map(lambda x: x.event, participation_events)]})


@login_required
@allow_methods(['GET'])
def get_event_attendance(_, event_id) -> JsonResponse:
    """Get the users that are participating in the event."""
    count = Attendance.objects.filter(
        event=event_id
    ).order_by('user__username').count()
    return JsonResponse({'event_id': event_id, 'count': count})


@login_required
@allow_methods(['POST'])
def add_user_attendance(request, event_id) -> JsonResponse:
    """Add a user to participate in an event."""
    try:
        event = Event.objects.filter(event_id=event_id).get()
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)
    
    if Attendance.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'error': 'User already participating'}, status=400)

    if event.event_date < datetime.datetime.now().date() + datetime.timedelta(days=3):
        return JsonResponse({'error': 'Event already happened'}, status=400)

    event_count = Attendance.objects.filter(event=event).count()
    if event_count >= event.event_limit:
        return JsonResponse({'error': 'Event is full'}, status=400)

    Attendance.objects.create(
        user=request.user,
        event=event
    )
    return JsonResponse({'success': True})
