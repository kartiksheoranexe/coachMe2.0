from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_one = models.CharField(max_length=254)
    address_line_two = models.CharField(max_length=254)
    long = models.DecimalField(max_digits=8, decimal_places=3)
    lat = models.DecimalField(max_digits=8, decimal_places=3)

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to ='certificates/')

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to ='achievement/')