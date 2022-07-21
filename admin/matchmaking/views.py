from utils import login_required, allow_methods
from events.models import Event
from .models import EventGroup
from .kmeansExecution import knn_endpoint

from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse


# Views here
@login_required
@allow_methods(["POST"])
@user_passes_test(lambda user: user.is_superuser)
def run_grouping(request):
    """Run the grouping algorithm"""
    event_groups = knn_endpoint()
    for event_id, groupings in event_groups.items():
        for index, user in enumerate(groupings):
            EventGroup.objects.create(
                group_no=index,
                event=Event.objects.filter(event_id=event_id).get(),
                user=user,
            )
    return JsonResponse({"success": "Grouping complete"}, status=200)
