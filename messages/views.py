#!/usr/bin/env python
""" 
Module for messages/views to handling message requests and responses
"""
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
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