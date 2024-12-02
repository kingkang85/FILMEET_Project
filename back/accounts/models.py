from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    phone_num = models.CharField(max_length=20, null=True, blank=True, unique=True, default=None) 
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(blank=True, upload_to='images/', default='static/images/default_profile.jpg')
    points = models.IntegerField(null=True, default=500)