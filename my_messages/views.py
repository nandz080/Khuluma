from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from rest_framework import generics, permissions
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, Chat, FriendRequest, Friendship
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.conf import settings
from user.models import Profile
from django.contrib import messages
from django.views.decorators.http import require_POST


User = get_user_model()

class ChatHomeView(TemplateView):
    template_name = 'chat/chat_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve all chats involving the current user
        context['active_chats'] = Chat.objects.filter(participants=self.request.user)
        return context

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all messages between the current user and the selected chat participant
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id)
        return Message.objects.filter(sender=self.request.user, receiver__in=chat.participants.all()) | \
               Message.objects.filter(receiver=self.request.user, sender__in=chat.participants.all())

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
            }
        )
        return Response({'message': 'Message sent successfully'})

@login_required
def chat(request, chat_id):
    chat_instance = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(sender=request.user, receiver__in=chat_instance.participants.all()) | \
               Message.objects.filter(receiver=request.user, sender__in=chat_instance.participants.all())
    return render(request, 'chat/chat.html', {'chat': chat_instance, 'messages': messages})

#@method_decorator(login_required, name='dispatch')
#class CreateChatView(View):
 #   def post(self, request, *args, **kwargs):
  #      friend_id = request.POST.get('friend_id')
   #     friend = get_object_or_404(settings.AUTH_USER_MODEL, id=friend_id)
    #    chat = Chat.objects.filter(participants=request.user).filter(participants=friend).first()
     #   if not chat:
      #      chat = Chat.objects.create()
       #     chat.participants.add(request.user, friend)
        #return redirect('my_messages:chat', chat_id=chat.id)
#@method_decorator(login_required, name='dispatch')
#class CreateChatView(View):

#    def get(self, request, *args, **kwargs):
#        # Render the start_chat.html template with any necessary context
#       return render(request, 'chat/start_chat.html')

#    def post(self, request, *args, **kwargs):
 #       friend_id = request.POST.get('friend_id')
 #       friend = get_object_or_404(User, id=friend_id)
  #      chat = Chat.objects.filter(participants=request.user).filter(participants=friend).first()
   #     if not chat:
    #        chat = Chat.objects.create()
     #       chat.participants.add(request.user, friend)
      #  return redirect('my_messages:chat', chat_id=chat.id)


@method_decorator(login_required, name='dispatch')
class CreateChatView(View):
    def get(self, request, *args, **kwargs):
        # Render the start_chat.html template with any necessary context
        return render(request, 'chat/start_chat.html')

    def post(self, request, *args, **kwargs):
        friend_id = request.POST.get('friend_id')
        friend = get_object_or_404(User, id=friend_id)
        chat = Chat.objects.filter(participants=request.user).filter(participants=friend).first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(request.user, friend)
        return redirect('my_messages:chat', chat_id=chat.id)


# Friendship management

@login_required
def friend_suggestions(request):
    # Get the current user and their profile
    user = request.user
    profile = Profile.objects.get(user=user)
    
    # Get the friends of the current user's profile
    profile_friends = profile.friends.all()

    # Exclude current friends and the user themself from the suggestions
    suggested_friends = User.objects.exclude(id__in=profile_friends).exclude(id=user.id)
    
    # Get the friend requests that the current user has sent or received
    sent_requests = FriendRequest.objects.filter(from_user=user)
    received_requests = FriendRequest.objects.filter(to_user=user)
    
    # Prepare the context for rendering
    context = {
        's_friends': suggested_friends,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    
    # Render the suggestions in the template
    return render(request, 'friends/suggestions.html', context)

@login_required
@require_POST
def add_friend(request, user_id):
    try:
        user_to_add = get_object_or_404(User, id=user_id)
        
        # Check if a friend request already exists
        if FriendRequest.objects.filter(sender=request.user, receiver=user_to_add).exists():
            return JsonResponse({'success': False, 'message': 'Friend request already sent.'})
        
        # Check if they are already friends (assuming you have a Friendship model or similar)
        if request.user.friends.filter(id=user_to_add.id).exists():
            return JsonResponse({'success': False, 'message': 'You are already friends.'})
        
        # Create a new friend request
        FriendRequest.objects.create(sender=request.user, receiver=user_to_add)
        return JsonResponse({'success': True})
    
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'User not found.'})

@login_required
def send_friend_request(request, user_id):
    """Send a friend request to another user."""
    to_user = get_object_or_404(User, id=user_id)
    FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect('my_messages:friend_suggestions')

@login_required
def cancel_friend_request(request, user_id):
    """Cancel a sent friend request."""
    to_user = get_object_or_404(User, id=user_id)
    friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).first()
    if friend_request:
        friend_request.delete()
    return redirect('my_messages:friend_suggestions')

@login_required
def remove_friend(request, user_id):
    """Remove a friend from the current user's friend list."""
    friend = get_object_or_404(User, id=user_id)
    friendship = Friendship.objects.filter(user1=request.user, user2=friend) | \
                 Friendship.objects.filter(user1=friend, user2=request.user)
    if friendship.exists():
        friendship.delete()
    return redirect('my_messages:friends_list')

@login_required
def accept_friend_request(request, request_id):
    """Accept a friend request."""
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    Friendship.make_friend(friend_request.from_user, friend_request.to_user)
    
    # Delete the friend request after accepting
    friend_request.delete()
    
    # Notify the user
    messages.success(request, f"You and {friend_request.from_user.username} are now friends.")
    
    return redirect('my_messages:friend_requests')

@login_required
def delete_friend_request(request, request_id):
    """Delete a friend request."""
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    messages.info(request, "Friend request deleted.")
    return redirect('my_messages:friend_requests')

@login_required
def friend_requests(request):
    """List all pending friend requests."""
    received_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friends/requests.html', {'friend_requests': received_requests})

@login_required
def friends_list(request):
    """List all friends of the current user."""
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    friends = [friendship.user1 if friendship.user2 == request.user else friendship.user2 for friendship in friendships]
    return render(request, 'friends/list.html', {'friends': friends})


