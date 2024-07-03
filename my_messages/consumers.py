#!/usr/bin/env python
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    """
    ChatConsumer handles websocket connections and messages for the chat application.
    It is responsible for handling incoming websocket messages and sending them to the 
    appropriate recipients.
    """
    def connect(self):
        """
        Connects to the websocket and accepts the connection.
        """
        self.accept()
        self.group_name = 'chat'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        """
        Disconnects from the websocket and closes the connection.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        Receives incoming websocket messages and handles them accordingly.
        """
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'send':
            self.handle_send_message(data)
        elif action == 'read':
            self.handle_read_message(data)

    def handle_send_message(self, data):
        """
        Handles sending a message to a recipient.
        """
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']
        content = data['content']

        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            is_sent=True
        )
        self.send(text_data=json.dumps({
            'action': 'send',
            'message': MessageSerializer(message).data
        }))

    def handle_read_message(self, data):
        """
        Handles marking a message as read.
        """
        message_id = data['message_id']
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        self.send(text_data=json.dumps({
            'action': 'read',
            'message_id': message_id
        }))
    
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_receipt(self, event):
        send_receipt = event['send_receipt']
        self.send(text_data=json.dumps({
            'send_receipt': send_receipt
        }))

    def read_receipt(self, event):
        read_receipt = event['read_receipt']
        self.send(text_data=json.dumps({
            'read_receipt': read_receipt
        }))


"""class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name = 'chat'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        # Handle sending the message here (e.g., save to DB, send to group)
"""
