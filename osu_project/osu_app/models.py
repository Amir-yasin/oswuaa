from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

import random

class CustomUser(AbstractUser):
    SERVICE_PROVIDER = 'Service Provider'
    SERVICE_TAKER = 'Service Taker'
    USER_TYPE_CHOICES = [
        (SERVICE_PROVIDER, 'Service Provider'),
        (SERVICE_TAKER, 'Service Taker'),
    ]
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    user_type = models.CharField(max_length=25, choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='profile_images/', default='default.jpeg')
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def generate_otp(self):
        otp = str(random.randint(100000, 999999))
        self.otp = otp
        self.save()
        return otp
        
    def formatted_user_id(self):
        return f"{self.pk:04}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SP_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='sp_profile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    experience = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    image = models.ImageField(default='default.jpeg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} SP_Profile'

class ST_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='st_profile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    image = models.ImageField(default='default.jpeg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} ST_Profile'
