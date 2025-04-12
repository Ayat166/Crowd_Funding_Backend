from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model,logout
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
from projects.serializers import ProjectSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser



from projects.serializers import ProjectUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "'refresh_token' is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class RequestPasswordReset(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"  # Frontend route

            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "noreply@example.com",
                [user.email],
            )
        return Response({"message": "a reset link has been sent."}, status=status.HTTP_200_OK)
    
class ConfirmPasswordReset(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=400)

        if PasswordResetTokenGenerator().check_token(user, token):
            password = request.data.get("password")
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successful"})
        return Response({"error": "Invalid or expired token"}, status=400)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        if request.user.id != user.id:
            return Response({"error": "You are not authorized to view this profile."}, status=status.HTTP_403_FORBIDDEN)

        user_data = UserSerializer(user).data
        projects = Project.objects.filter(creator_id=id)
        donations = Donation.objects.filter(user_id=id)

        projects_data = ProjectSerializer(projects, many=True).data
        donations_data = DonationSerializer(donations, many=True).data

        return Response({
            "user": user_data,
            "projects_count": projects.count(),
            "donations_count": donations.count(),
            "projects": projects_data,
            "donations": donations_data,
        }, status=status.HTTP_200_OK)


class User_Update_Delete(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def put(self, request, id):
        user = get_object_or_404(User, id=id)

        serializer = UserUpdateSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(data={
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)

        if request.user.id != user.id:
            return Response(
                {"error": "You are not authorized to delete this account."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user.delete()
            return Response(
                {"message": "Account deleted successfully."},
                status=status.HTTP_200_OK
            )
    
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
    )

