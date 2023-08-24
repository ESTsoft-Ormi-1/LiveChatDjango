from django.urls import re_path, include
from rest_framework import routers
from chat.views import RoomViewSet

router = routers.DefaultRouter()
router.register('room', RoomViewSet)


urlpatterns = [
    re_path(r'^', include(router.urls)),
]
