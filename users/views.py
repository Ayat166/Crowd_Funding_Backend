from rest_framework import viewsets, permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from donations.models import Donation
from donations.serializers import DonationSerializer
from projects.models import Project
from projects.serializers import ProjectUserSerializer





User1 = get_user_model()

class RegisterViewset(viewsets.ViewSet):
    permission_classes= [permissions.AllowAny]
    queryset = User1.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, requests):
        serializer = self.serializer_class(data = requests.data)
        if serializer.is_valid():
            user = serializer.save()
            send_activation_email(user, requests)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
def send_activation_email(user, request):

    token = user.activation_token  
    uid = str(user.pk)
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    url = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': user.activation_token})
    activation_link = f"http://{domain}/api/users/activate/{uidb64}/{token}/"
    
    subject = "Activate Your Account"

    # simple text message body
    message = f"Hello {user.first_name},\n\n"
    message += "Thank you for registering on our Crowd_funding platform! Please click the link below to activate your account:\n\n"
    message += f"{activation_link}\n\n"
    message += "If you did not request this email, please ignore it.\n\n"
    message += "Thank you,\n Website Team"

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    print(f"Email sent to {user.email}")
        
def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User1, pk=uid)  
        
        if str(user.activation_token) != token:
            return HttpResponse("Invalid activation token.", status=400)

        if user.token_expiration < timezone.now():
            return HttpResponse("This activation token has expired.", status=400)

        user.is_active = True
        user.activation_token = None
        user.save()

        return HttpResponse("Your account has been successfully activated!", status=200)

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=400)



class ProfileView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user_data = UserSerializer(user).data
        projects = Project.objects.filter(creator_id=pk)
        donations = Donation.objects.filter(user_id=pk)

        projects_data = ProjectUserSerializer(projects, many=True).data
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
