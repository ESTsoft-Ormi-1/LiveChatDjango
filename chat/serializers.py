from rest_framework import serializers
from chat.models import Room, Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'sender', 'room', 'message', 'created_at', 'parent_chat')


class RoomSerializer(serializers.ModelSerializer):
    chat_url = serializers.SerializerMethodField()
    chat_messages = ChatSerializer(source='chat_set', many=True, read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'chat_url', 'chat_messages', 'owner')

    def get_chat_url(self, obj):
        request = self.context.get('request')
        if request:
            # protocol = 'ws' if request.is_secure() else 'wss'
            return f"ws://{request.get_host()}/ws/chat/{obj.id}/chat/"
        return ''