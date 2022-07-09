from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    mobile_number = models.CharField(max_length=10)
    nok = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    ethnicity = models.CharField(max_length=50)
    medical_conditions = models.TextField()
    allergies = models.TextField()
    dietary_restrictions = models.TextField()

    def __str__(self):
        """String representation of the user"""
        return f"{self.user.username} details"
