from django.contrib import admin
from coachMe.models import User, Address, Certificate, Achievement, Coach, Package, Client, Transaction, Mapping, ClientOnboard, Room, Message


# Register your models here.
admin.site.register(User),
admin.site.register(Address),
admin.site.register(Certificate),
admin.site.register(Achievement),
admin.site.register(Coach),
admin.site.register(Package),
admin.site.register(Client),
admin.site.register(Transaction),
admin.site.register(Mapping),
admin.site.register(ClientOnboard),
admin.site.register(Room),
admin.site.register(Message)
