#!/usr/bin/env python
from django.urls import path
from . import views
from .views import MessageListView, SendMessageView, ReadMessageView


urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/send/', views.SendMessageView.as_view(), name='send-message'),
    path('messages/read/<int:pk>/', views.ReadMessageView.as_view(), name='read-message'),
    path('messages/send-message/', views.send_message, name='send-message-view'),
    path('messages/mark-as-read/<int:message_id>/', views.mark_as_read, name='mark-as-read'),
    path('chat/<str:room_name>/', views.room, name='room'),
]

#urlpatterns = [
 #   path('', MessageListView.as_view(), name='message_list'),
  #  path('send/', SendMessageView.as_view(), name='send_message'),
   # path('read/<int:pk>/', ReadMessageView.as_view(), name='read_message'),
    #path('chat/<str:room_name>/', views.room, name='room'),
#]