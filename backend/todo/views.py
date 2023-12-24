from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from .task import get, remove, add, update
from .cache_function import getAllKey, getKey
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, status


class TodoViewSet(viewsets.ViewSet):
    def get(self, request):
        data = get()
        return Response(data)

    def add(self, request):
        data = add(request)
        return Response(data)

    def update(self, request, pk=None):
        data = update(request, pk)
        return Response(data)

    def remove(self, request, pk=None):
        data = remove(request, pk)
        return Response(data)

    def getCache(self, request, key="*"):
        return Response(getAllKey(key))

    def getKey(self, request, key="*"):
        return Response(getKey(key))