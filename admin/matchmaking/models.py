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

    def toDict(self) -> dict:
        """ Convert event into a dictionary"""
        d = {
            "event_id": self.event,
            "user_id" : self.user,
            "group_no": self.group_no,
        }

    def __str__(self) -> str:
        """String representation of the EventGroup"""
        return f"{self.event.event_name} - {self.user.username} in group {self.group_no}"