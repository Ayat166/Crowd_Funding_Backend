from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields ): 
        if not email: 
            raise ValueError('Email is a required field')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and returns a superuser with the necessary fields set.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        user.set_password(password)
        user.is_active = True  # Set is_active to True for superuser
        user.is_staff = True  # Ensure is_staff is True for superuser
        user.is_superuser = True  # Ensure is_superuser is True for superuser
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Activated via email
    
    
    objects = CustomUserManager() 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    