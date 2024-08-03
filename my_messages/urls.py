#!/usr/bin/env python
from django.urls import path
from .views import ChatHomeView, CreateRoomView, MessageListView, SendMessageView, ReadMessageView, mark_as_read, room, chat

app_name = 'my_messages'

urlpatterns = [
    path('chat_home/', ChatHomeView.as_view(), name='chat_home'),
    path('create_room/', CreateRoomView.as_view(), name='create_room'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('send_message/', SendMessageView.as_view(), name='send-message'),
    path('read_message/<int:pk>/', ReadMessageView.as_view(), name='read_message'),
    path('mark_as_read/<int:message_id>/', mark_as_read, name='mark_as_read'),
    path('room/<str:room_name>/', room, name='room'),
    path('chat/<int:chat_id>/', chat, name='chat'),
]


