from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utilss.user_message import io
from django.db.models import Q
from django.shortcuts import redirect, reverse
from .models import *
from rest_framework.permissions import IsAuthenticated
from .api.serializer import *

User = get_user_model()

class ConverstationsView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        conversation = Conversation.objects.filter( Q(starter=request.user) |
                                                    Q(receiver=request.user)
                                                )
        if conversation.exists():
            serializer = ConversationSerializer(conversation, many=True)
            return Response(io._success(serializer.data))
        else:
            io._error('You have not any conversations.')


class ConversationMessageView(APIView):
    permission_classes = [IsAuthenticated,]

    # change it to post methods
    def post(self, request, username):
        print('__________________', request.user, username)
        try:
            conversation = Conversation.objects.get(
                Q(starter__username=username, receiver__username=request.user) | 
                Q(receiver__username=username, starter__username=request.user)
            )
            serializer = MessageSerializer(conversation.message_conversation.all(), many=True)
            return Response(serializer.data)
        except:
            receiver = User.objects.filter(username=username)
            if receiver.exists():
                conversation = Conversation.objects.create(starter=request.user, receiver=receiver[0])
                return Response(io._success(f"conversation with {username} was created successfully."))
            else:
                io._error("No user was found with this username.")





