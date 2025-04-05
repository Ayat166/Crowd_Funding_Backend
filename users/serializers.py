#the Bridge between frontend and Backend
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
import re

User1 = get_user_model()

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