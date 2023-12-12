from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utilss.user_message import io
from django.db.models import Q
from .models import *
from rest_framework.permissions import IsAuthenticated
from .api.serializer import *

User = get_user_model()

class ConverstationView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        conversation = Conversation.objects.filter( Q(starter=request.user) |
                                                    Q(receiver=request.user))
        if conversation.exists():
            print('+++++++++++++++++++++++', conversation[0].starter)
            serializer = ConversationSerializer(conversation, many=True)
            return Response(io._success(serializer.data))
        else:
            io._error('You have not any conversations.')
