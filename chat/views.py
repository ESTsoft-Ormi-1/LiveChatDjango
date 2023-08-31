from rest_framework import viewsets, generics
from .models import Room, Chat
from .serializers import RoomSerializer, ChatSerializer
from rest_framework.permissions import IsAuthenticated


class RoomViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated] 
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ChatCreateView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated] 
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer