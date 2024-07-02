#!/usr/bin/env python
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/messages/', ChatConsumer.as_asgi()),
]