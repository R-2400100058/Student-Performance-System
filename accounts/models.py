from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"