#!/usr/bin/env python
"""
Module for messages/views to handle message requests and responses
"""
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message
from .serializers import MessageSerializer

# Create your views here.

class MessageListView(generics.ListAPIView):
    """
    List all messages for a user
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return all messages for a user
        """
        return Message.objects.filter(receiver=self.request.user)

class SendMessageView(generics.CreateAPIView):
    """
    Send a message to a user
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automates the assignment of message sender 
        """
        serializer.save(sender=self.request.user, is_sent=True)

class ReadMessageView(generics.UpdateAPIView):
    """
    Mark a message as read
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Mark a message as read
        """
        instance = self.get_object()
        instance.is_read = True
        instance.save()
        return Response({'status': 'Message read'})

def send_message(request):
    message = request.POST['message']
    sender = request.user
    # Save the message to the database
    new_message = Message.objects.create(content=message, sender=sender)
    # Send WebSocket message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat',  # Group name
        {
            'type': 'chat_message',
            'message': {
                'id': new_message.id,
                'sender': sender.username,
                'content': new_message.content,
            },
            'send_receipt': {
                'message_id': new_message.id,
                'status': 'sent'
            }
        }
    )
    return HttpResponse('Message sent')

def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    message.is_read = True
    message.save()

    # Send WebSocket message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat',  # Group name
        {
            'type': 'read_receipt',
            'read_receipt': {
                'message_id': message.id,
                'status': 'read'
            }
        }
    )
    return JsonResponse({'status': 'Message marked as read'}, status=200)

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })
