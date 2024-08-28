#!/usr/bin/env python
from django.urls import path
from . import  views
from .views import ChatHomeView, MessageListView, SendMessageView, chat, CreateChatView 

app_name = 'my_messages'

urlpatterns = [
    path('chat_home/', ChatHomeView.as_view(), name='chat_home'),
    #path('create_room/', CreateRoomView.as_view(), name='create_room'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('send_message/', SendMessageView.as_view(), name='send-message'),
    #path('read_message/<int:pk>/', ReadMessageView.as_view(), name='read_message'), (import ReadMessageView,
    #path('mark_as_read/<int:message_id>/', mark_as_read, name='mark_as_read'), (import mark_as_read
    #path('room/<str:room_name>/', room, name='room'),
    path('chat/<int:chat_id>/', chat, name='chat'),
    path('start_chat/', CreateChatView.as_view(), name='start_chat'),

    # Friend suggestion and request management
    path('suggestions/', views.friend_suggestions, name='suggestions'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('friends/', views.friends_list, name='friends_list'),
]
#urlpatterns = [
#    path('', views.ChatHomeView.as_view(), name='chat_home'),
#    path('chat/<int:chat_id>/', views.chat, name='chat'),
#    path('send_message/', views.SendMessageView.as_view(), name='send_message'),
#    path('create_chat/', views.CreateChatView.as_view(), name='create_chat'),
#]


