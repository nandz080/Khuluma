#!/usr/bin/env python
from django.urls import path, re_path
from .consumers import ChatConsumer
from . import consumers

websocket_urlpatterns = [
    path('ws/my_messages/', ChatConsumer.as_asgi()),
   #re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]

