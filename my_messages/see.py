from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message
from .serializers import MessageSerializer

# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message, ChatRoom

@login_required
def chat_home(request):
    # Assuming you have a ChatRoom model to handle conversations
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chats/chat_home.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room(request, room_name):
    chat_room = get_object_or_404(ChatRoom, name=room_name)
    messages = Message.objects.filter(room=chat_room)
    return render(request, 'chats/chat_room.html', {'chat_room': chat_room, 'messages': messages})






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
        Automates the assignment of message sender and sends WebSocket message
        """
        message = serializer.save(sender=self.request.user, is_sent=True)

        # Send WebSocket message
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.receiver.id}',  # Group name
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': message.sender.username,
                    'content': message.content,
                },
                'send_receipt': {
                    'message_id': message.id,
                    'status': 'sent'
                }
            }
        )

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

def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.receiver != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    message.is_read = True
    message.save()

    # Send WebSocket message
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{message.receiver.id}',  # Group name
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
