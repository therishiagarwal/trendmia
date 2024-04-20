# myapp/consumers.py

from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Add user to chat group
        self.group_name = 'chat_room'
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Remove user from chat group
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        # Broadcast message to chat group
        self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=event['message'])
