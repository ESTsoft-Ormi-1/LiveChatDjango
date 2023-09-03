from rest_framework import viewsets, generics
from .models import Room, Chat
from .serializers import RoomSerializer, ChatSerializer
from rest_framework.permissions import IsAuthenticated


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ChatCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        
        # Get the created chat
        chat = Chat.objects.get(pk=response.data['id'])

        # Get the associated post (you'll need to adjust this part based on how your models are related)
        post = chat.post

        # Check if a room exists for this post, create one if it doesn't
        room, created = Room.objects.get_or_create(post=post)

        # Return the room data along with the chat data in the response
        room_data = RoomSerializer(room, context={'request': request}).data
        response.data['room_data'] = room_data

        return response