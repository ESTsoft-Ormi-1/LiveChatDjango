from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import Room
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import exceptions


class ChatConsumer(JsonWebsocketConsumer):
    # room_name에 기반하여 그룹명을 생성

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수는 생성자 내에서 정의.
        # 인스턴스 변수 group_name 추가
        self.group_name = ""
        self.room = None
    
    # 웹소켓 클라이언트가 접속을 요청할 때, 호출됩니다.
    def connect(self):

        user = self.scope["user"]
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        try:
            self.room = Room.objects.get(pk=room_pk)
        except Room.DoesNotExist:
            self.close()
        else:
            self.group_name = self.room.chat_group_name
            is_new_join = self.room.user_join(self.channel_name, user)
            if is_new_join:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chat.user.join",
                        "username": user.userprofile.nickname,
                    }
                )

            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name,
            )
            # 본 웹소켓 접속을 허용.
            self.accept()

    # 웹소켓 클라이언트와의 접속이 끊겼을 때, 호출 됩니다.
    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )

        user = self.scope["user"]

        if self.room is not None:
            is_last_leave = self.room.user_leave(self.channel_name, user)
            if is_last_leave:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chat.user.leave",
                        "username": user.userprofile.nickname,
                    }
                )
    
    # 단일 클라이언트로 메세지를 받으면 호출
    def receive_json(self, content, **kwargs):
        user = self.scope["user"]

        _type = content["type"]

        if _type == "chat.message":
            sender = user.email
            nickname = user.userprofile.nickname
            profile_picture_url =  "/media/" + user.userprofile.profile_picture.name
            message = content["message"]
            # Publish 과정: "square" 그룹 내 다른 consumer들에게 메세지를 전달합니다.
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                    "nickname": nickname,
                    "profile_picture_url": profile_picture_url
                }
            )
        else:
            print(f"Invalid message type : {_type}")
        
    def chat_user_join(self, message_dict):
        self.send_json({
            "type": "chat.user.join",
            "username": message_dict["username"]
        })

    def chat_user_leave(self, message_dict):
        self.send_json({
            "type": "chat.user.leave",
            "username": message_dict["username"]
        })

        # 그룹을 통해 type="chat.message" 메세지 받으면 호출됩니다.
    def chat_message(self, message_dict):
        # 접속되어있는 클라이언트에게 메세지를 전달합니다.
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"],
            "sender": message_dict["sender"],
            "nickname": message_dict["nickname"],
            "profile_picture_url": message_dict["profile_picture_url"],
        })