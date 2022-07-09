from django.core.validators import MinValueValidator
from django.db import models


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
    event_location = models.CharField(max_length=100, blank=True)
    event_price = models.PositiveBigIntegerField()
    event_organizer = models.CharField(max_length=1000)
    event_image = models.ImageField(upload_to="images/")
    event_limit = models.PositiveIntegerField()
    event_category = models.CharField(max_length=100)

    # Check updates
    event_created_at = models.DateTimeField(auto_now_add=True)
    event_updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self) -> str:
        """Representation of the event object"""
        return f"Event: {self.event_name} at {self.event_location} on {self.event_date} at {self.event_time} for {self.event_duration} hours"

    def __str__(self) -> str:
        """String version of the event object"""
        return f"Event: {self.event_name} at {self.event_location}"

    def toCardDict(self) -> dict:
        """Details for carousell card"""
        d = {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "event_duration": self.event_duration,
            "event_price": self.event_price,
        }
        if self.event_image:
            d["event_image"] = self.event_image.url
        return d

    def toDict(self) -> dict:
        """Convert the event into a dictionary"""
        d = {
            "event_id": self.event_id,
            "event_name": self.event_name,
            "event_description": self.event_description,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "event_duration": self.event_duration,
            "event_location": self.event_location,
            "event_price": self.event_price,
            "event_organizer": self.event_organizer,
            "event_created_at": self.event_created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_updated_at": self.event_updated_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "event_category": self.event_category,
        }
        if self.event_image:
            d["event_image"] = self.event_image.url
        return d
