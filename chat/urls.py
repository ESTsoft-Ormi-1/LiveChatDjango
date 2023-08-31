from django.urls import re_path, include, path
from rest_framework import routers
from chat.views import RoomViewSet, ChatCreateView

router = routers.DefaultRouter()
router.register('room', RoomViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('message/', ChatCreateView.as_view(), name='chat-create'),
]
