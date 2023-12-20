from django.urls import  path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('conversations/', ConverstationsView.as_view(), name='conversations'  ),
    path('conversations/<str:username>/', ConversationMessageView.as_view(), name='conversation_messages'  ),
]