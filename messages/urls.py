#!/usr/bin/env python

from django.urls import path
from .views import MessageListView, SendMessageView, ReadMessageView

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('read/<int:pk>/', ReadMessageView.as_view(), name='read_message'),
]