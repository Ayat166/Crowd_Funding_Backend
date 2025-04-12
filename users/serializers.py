#the Bridge between frontend and Backend
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
import re
from rest_framework import serializers
from .models import User
from projects.models import Project
import re
from rest_framework.fields import ImageField


User1 = get_user_model()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to the response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_superuser': self.user.is_superuser,

        }

        return data

class RegisterSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User1
        fields = ('id', 'email', 'password', 'mobile', 'first_name','last_name','profile_picture')
        # hiding the password from the response to be more secured
        extra_kwargs =  { 'password': {'write_only':True}}

    def validate_mobile(self, value):
        if not re.match(r'^01[0-2,5][0-9]{8}$', value):
            raise serializers.ValidationError('Invalid Egyptian mobile number')
        return value

    def create(self, validated_data):
        user = User1.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'profile_picture',
            'birthdate',
            'facebook_profile',
            'country',
            'is_superuser',
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'mobile',
            'profile_picture',
            'birthdate',
            'facebook_profile',
            'country'
        ]
        extra_kwargs = {
            'profile_picture': {'required': False, 'allow_null': True},
        }

    def validate_mobile(self, value):
        if value in [None, '']:
                raise serializers.ValidationError("Mobile field is required.")
        pattern = r'^(010|011|012|015)[0-9]{8}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid Egyptian mobile number.")
        return value
    
    def validate_first_name(self, value):
        if value in [None, '']:
            raise serializers.ValidationError("First name is required.")
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("First name must contain letters, not only numbers.")
        return value
    
    def validate_last_name(self, value):
        if value in [None, '']:
            raise serializers.ValidationError("Last name is required.")
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Last name must contain letters, not only numbers.")
        return value
    
    def validate_profile_picture(self, value):
        if value is None:
            return value 
        return value
    
    def update(self, instance, validated_data):
        for attr in self.Meta.fields:
            if attr == 'id':
                continue  
            if attr == 'profile_picture':
                if 'profile_picture' not in validated_data:
                    continue
                if validated_data.get('profile_picture') in [None, '', []]:
                    continue

            if attr in validated_data:
                value = validated_data.get(attr)
                setattr(instance, attr, value)
            
        instance.save()
        return instance

    
class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        password = attrs.get('password')
        request = self.context.get('request')

        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect password."})

        return attrs