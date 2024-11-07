from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True,unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.username
