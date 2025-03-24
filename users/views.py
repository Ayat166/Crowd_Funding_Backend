from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class ProfileView(APIView):
    def get(self, request):
        try:
            user_object = User.objects.get(id=1)

            data = {
                'user': UserSerializer(user_object).data,
            }

            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)