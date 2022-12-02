from django.db import models
import uuid
from phone_field import PhoneField
from django.contrib.auth.models import AbstractUser
from datetime import datetime


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_TYPE = (
    ('U', 'User'),
    ('C', 'Coach'),
    ('L', 'Client')
)

DURATION_TYPE = (
    ('Y', 'Years'),
    ('M',  'Months'),
    ('D',  'Days')
)

STATUS = (
    ('P', 'Pending'),
    ('S',  'Success'),
    ('C',  'Cancelled')
)

MODE = (
    ('CC', 'Credit Card'),
    ('DC',  'Debit Card'),
    ('UPI',  'UPI'),
    ('ND', 'Not Defined')
)

TYPE = (
    ('P', 'Purchase'),
    ('R', 'Reverse'),
)

YES_NO = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

V_NV = (
    ('V', 'Veg'),
    ('N', 'Non Veg'),
)


class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_no = PhoneField(blank=True, help_text='Contact phone number')
    user_type = models.CharField(max_length=1, choices=USER_TYPE, null=True)


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
    thumbnail = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    thumbnail = models.ImageField(upload_to='achievements/')

    def __str__(self):
        return self.title


class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=254)
    years_of_experience = models.FloatField(null=True, blank=True)
    certifications = models.ManyToManyField(Certificate)
    achievements = models.ManyToManyField(Achievement)
    is_active = models.BooleanField(('active'), default=True)
    coach_avatar = models.ImageField(
        upload_to='coachavatars/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Package(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    package_name = models.CharField(max_length=100)
    package_desc = models.CharField(max_length=254)
    duration_type = models.CharField(max_length=1, choices=DURATION_TYPE)
    duration = models.IntegerField()
    base_price = models.IntegerField()

    def __str__(self):
        return self.package_name


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    client_avatar = models.ImageField(
        upload_to='clientavatars/', null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Mapping(models.Model):
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    coach_id = models.ForeignKey(Coach, on_delete=models.CASCADE)
    price = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    unique_id = models.UUIDField(primary_key=True, unique=True, editable=False)
    amount_paid = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS)
    mode = models.CharField(max_length=3, choices=MODE)
    date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=TYPE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.unique_id)


class ClientOnboard(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    goal = models.CharField(max_length=254)
    height = models.FloatField()
    weight = models.FloatField()
    neck_inches = models.FloatField()
    chest_inches = models.FloatField(null=True)
    shoulder_inches = models.FloatField()
    waist_inches = models.FloatField()
    quads_inches = models.FloatField()
    calf_inches = models.FloatField()
    daily_act_level = models.IntegerField()
    gym_join = models.CharField(max_length=1, choices=YES_NO)
    curr_workout_patt = models.TextField()
    pref_workout_time = models.CharField(max_length=100)
    avg_sleeping_hours = models.FloatField()
    sleep_quality = models.IntegerField()
    stress_levels = models.IntegerField()
    any_diff_mov = models.TextField()
    health_related_issues = models.TextField()
    supps = models.TextField()
    anabolics = models.CharField(max_length=1, choices=YES_NO)
    anabolics_desc = models.TextField()
    past_curr_injuries = models.TextField()
    veg_non_veg = models.CharField(max_length=1, choices=V_NV)
    no_of_meals = models.TextField()
    curr_eating_pattern = models.TextField()
    cheat_meals = models.TextField()
    easily_reach_food = models.TextField()
    curr_physique_pic = models.ImageField(
        upload_to='current physique/', null=True, blank=True)
    expectations_from_caoch = models.TextField()

    def __str__(self):
        return self.coach.user.first_name + ' ' + self.client.user.first_name
    

class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=1000000)
    file_upload = models.FileField(
        upload_to='messages/%Y/%m/%d', null=True, blank=True)
