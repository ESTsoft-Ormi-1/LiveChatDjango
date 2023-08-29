from rest_framework import serializers
from chat.models import Room, Chat


class RoomSerializer(serializers.ModelSerializer):
    chat_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'chat_url')

    def get_chat_url(self, obj):
        request = self.context.get('request')
        if request:
            # protocol = 'ws' if request.is_secure() else 'wss'
            return f"ws://{request.get_host()}/ws/chat/{obj.id}/chat/"
        return ''
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'