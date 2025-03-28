from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from .serializers import DeleteAccountSerializer
from .serializers import UserUpdateSerializer
from donations.models import Donation
from donations.serializers import DonationSerializer
from projects.models import Project
from projects.serializers import ProjectSerializer



class ProfileView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_data = UserSerializer(user).data
        projects = Project.objects.filter(creator_id=pk)
        donations = Donation.objects.filter(user_id=pk)

        projects_data = ProjectSerializer(projects, many=True).data
        donations_data = DonationSerializer(donations, many=True).data

        return Response({
            "user": user_data,
            "projects_count": projects.count(),
            "donations_count": donations.count(),
            "projects": projects_data,
            "donations": donations_data,
        }, status=status.HTTP_200_OK)
    
        
class UserUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
            
class DeleteAccountAPIView(APIView):
    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if check_password(password, user.password):
                user.delete()
                return Response({"message": "Account deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Incorrect password"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)