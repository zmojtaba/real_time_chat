from account.api.serializer import UserSerializer
from ..models import Conversation, Message
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        exclude = ('conversation',)
        extra_fields = ('sender',)


class ConversationListSerializer(serializers.ModelSerializer):
    starter = UserSerializer()
    receiver = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['starter', 'receiver', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)


class ConversationSerializer(serializers.ModelSerializer):
    starter = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Conversation
        fields = ['starter', 'receiver', 'start_time']

