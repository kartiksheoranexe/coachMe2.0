from django.contrib import admin
from coachMe.models import User, Address, Certificate, Achievement, Coach, Package, Client
                            

# Register your models here.
admin.site.register(User),
admin.site.register(Address),
admin.site.register(Certificate),
admin.site.register(Achievement),
admin.site.register(Coach),
admin.site.register(Package),
admin.site.register(Client)
