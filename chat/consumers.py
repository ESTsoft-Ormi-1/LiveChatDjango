from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

class ChatConsumer(JsonWebsocketConsumer):
    # room_name 에 상관없이 모든 유저들을 square를 통해 채팅 해도록 구현.
    SQAUARE_GROUP_NAME = "square"
    groups = [SQAUARE_GROUP_NAME]
    
    # 단일 클라이언트로 메세지를 받으면 호출
    def receive_json(self, content, **kwargs):
        _type = content["type"]

        if _type == "chat.message":
            message = content["message"]
            # Publish 과정: "square" 그룹 내 다른 consumer들에게 메세지를 전달합니다.
            async_to_sync(self.channel_layer.group_send)(
                self.SQAUARE_GROUP_NAME,
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