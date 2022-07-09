from django.db import models


# Create your models here.
class Attendance(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)

    def __str__(self: "Attendance") -> str:
        """String representation of the participation object"""
        return f"{self.user} is participating in {self.event}"
