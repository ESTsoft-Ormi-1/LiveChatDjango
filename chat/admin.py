from django.contrib import admin
from chat.models import Room, Chat, RoomMember

# Register your models here.
admin.site.register(Room)
admin.site.register(Chat)
admin.site.register(RoomMember)