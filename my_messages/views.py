from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, Room, Chat
from .serializers import MessageSerializer

class ChatHomeView(TemplateView):
    template_name = 'chat/chat_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(receiver=self.request.user)
        context['active_chats'] = Chat.objects.filter(participants=self.request.user)
        return context

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user, is_sent=True)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{message.receiver.id}',
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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
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

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{message.receiver.id}',
        {
            'type': 'read_receipt',
            'read_receipt': {
                'message_id': message.id,
                'status': 'read'
            }
        }
    )
    return JsonResponse({'status': 'Message marked as read'}, status=200)

@method_decorator(login_required, name='dispatch')
class CreateRoomView(View):
    def post(self, request, *args, **kwargs):
        room_name = request.POST.get('room_name')
        if Room.objects.filter(name=room_name).exists():
            return JsonResponse({'error': 'Room name already exists'}, status=400)
        
        room = Room.objects.create(name=room_name)
        return redirect('my_messages:room', room_name=room.name)

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room)
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})

@login_required
def chat(request, chat_id):
    chat_instance = get_object_or_404(Chat, id=chat_id)
    return render(request, 'chat/chat.html', {'chat': chat_instance})


