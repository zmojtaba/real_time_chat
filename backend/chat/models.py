from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

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
    attachment = models.FileField(blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message_conversation")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)