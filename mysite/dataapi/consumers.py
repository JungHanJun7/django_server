from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChangeConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "changes",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "changes",
            self.channel_name
        )

    def receive(self, text_data):
        pass  # 여기서는 클라이언트로부터의 메시지를 받지 않습니다.

    def send_change(self, event):
        self.send(json.dumps(event["text"]))