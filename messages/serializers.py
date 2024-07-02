#!/usr/bin/env python
"""
Module  for messages serializers
"""
from rest_framework import serializers
from .models import Message

""" 
Class for message serializer 
Serializes fields from the Message model defined in `fields`.
"""
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'is_sent', 'is_read']
