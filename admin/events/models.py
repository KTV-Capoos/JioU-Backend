from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)

    # Event details.
    event_name = models.CharField(max_length=100)
    event_description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    event_duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    event_location = models.CharField(max_length=100)
    event_image = models.ImageField(upload_to='images/')

    # Check updates
    event_created_at = models.DateTimeField(auto_now_add=True)
    event_updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        """Representation of the event object"""
        return f"Event: {self.event_name} at {self.event_location} on {self.event_date} at {self.event_time} for {self.event_duration} hours"

    def __str__(self) -> str:
        """String version of the event object"""
        return f"Event: {self.event_name} at {self.event_location}"
