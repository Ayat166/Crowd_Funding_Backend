from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
import uuid
from datetime import timedelta
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields ): 
        if not email: 
            raise ValueError('Email is a required field')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with the necessary fields set.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = None
        user.set_password(password)
        user.is_active = True  
        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)
        return user


def default_expiration():
    return timezone.now() + timedelta(days=1)

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Activated via email
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    token_expiration = models.DateTimeField(default=default_expiration)

    def generate_activation_token(self):
        self.activation_token = uuid.uuid4()
        self.token_expiration = timezone.now() + timedelta(hours=24)
        self.save()
    
    objects = CustomUserManager() 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    