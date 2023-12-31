from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField

User = get_user_model()

class Conversation(models.Model):
    starter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_receiver"
    )
    start_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.starter.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, related_name='message_sender')
    text = models.CharField(max_length=200, blank=True)
    attachment = ResizedImageField(force_format='WEBP', size=None,scale=0.5, quality=75, upload_to='chats/images/', blank=True, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message_conversation")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return f"{self.conversation}_{self.sender}"