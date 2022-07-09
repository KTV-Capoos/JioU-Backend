from django.db import models
from django.contrib.auth.models import User
from events.models import Event

# Create your models here.
class EventGroup(models.Model):
    """
    EventGroup is a group of events that are similar in some way.
    """
    group_no = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """String representation of the EventGroup"""
        return f"{self.event.event_name} - {self.user.username} in group {self.group_no}"