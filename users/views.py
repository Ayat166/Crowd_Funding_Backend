from django.shortcuts import render, redirect
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
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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