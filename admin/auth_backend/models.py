from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.TextField()
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

    def to_dict(self):
        """Return a dictionary representation of the user"""
        return {
            "full_name": self.full_name,
            "username": self.user.username,
            "email": self.user.email,
            "gender": self.gender,
            "dob": self.dob,
            "mobile_number": self.mobile_number,
            "nok": self.nok,
            "religion": self.religion,
            "nationality": self.nationality,
            "ethnicity": self.ethnicity,
            "medical_conditions": self.medical_conditions,
            "allergies": self.allergies,
            "dietary_restrictions": self.dietary_restrictions
        }
