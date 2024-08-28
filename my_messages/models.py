from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Model to represent a 1:1 chat between two users
class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join([user.username for user in self.participants.all()])

# Model to represent an individual message in a 1:1 chat
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'

    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Friend request from {self.from_user.username} to {self.to_user.username}'

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendship_set', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1.username} is friends with {self.user2.username}'

    class Meta:
        unique_together = ('user1', 'user2')

    @classmethod
    def make_friend(cls, user1, user2):
        if user1 != user2:
            friendship, created = cls.objects.get_or_create(
                user1=min(user1, user2),
                user2=max(user1, user2),
            )
            return friendship


