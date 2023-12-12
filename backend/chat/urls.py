from django.urls import  path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('conversations/', ConverstationView.as_view(), name='conversations'  )
]