from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import Room

class ChatConsumer(JsonWebsocketConsumer):
    # room_name에 기반하여 그룹명을 생성

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수는 생성자 내에서 정의.
        # 인스턴스 변수 group_name 추가
        self.group_name = ""
    
    # 웹소켓 클라이언트가 접속을 요청할 때, 호출됩니다.
    def connect(self):
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]

        self.group_name = Room.make_chat_group_name(room_pk=room_pk)

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
    
    # 단일 클라이언트로 메세지를 받으면 호출
    def receive_json(self, content, **kwargs):
        _type = content["type"]

        if _type == "chat.message":
            message = content["message"]
            # Publish 과정: "square" 그룹 내 다른 consumer들에게 메세지를 전달합니다.
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message,
                }
            )
        else:
            print(f"Invalid message type : {_type}")
        
        # 그룹을 통해 type="chat.message" 메세지 받으면 호출됩니다.
    def chat_message(self, message_dict):
        # 접속되어있는 클라이언트에게 메세지를 전달합니다.
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"],
        })