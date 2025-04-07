from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User1 = get_user_model()

class RegisterViewset(viewsets.ViewSet):
    permission_classes= [permissions.AllowAny]
    queryset = User1.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, requests):
        serializer = self.serializer_class(data = requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        