# user/admin.py

from django.contrib import admin
from .models import UserProfile, User

admin.site.register(UserProfile)
admin.site.register(User)

