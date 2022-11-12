from django.db import models
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

DURATION_TYPE = (
        ('Y', 'Years'),
        ('M',  'Months'),
        ('D',  'Days')
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

    def __str__(self):
        return self.user.first_name

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to ='certificates/')

    def __str__(self):
        return self.title

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to ='achievements/')

    def __str__(self):
        return self.title

class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=254)
    years_of_experience = models.FloatField(null=True, blank=True)
    certifications = models.ManyToManyField(Certificate)
    achievements = models.ManyToManyField(Achievement)
    is_active = models.BooleanField(('active'), default=True)
    coach_avatar = models.ImageField(upload_to='coachavatars/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Package(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    package_desc = models.CharField(max_length=254)
    duration_type = models.CharField(max_length=1, choices=DURATION_TYPE)
    duration = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.coach.first_name

