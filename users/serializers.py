from rest_framework import serializers
from .models import User
from projects.models import Project
import re
from rest_framework.fields import ImageField


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
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
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
    def validate_mobile(self, value):
        pattern = r'^(010|011|012|015)[0-9]{8}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid Egyptian mobile number.")
        return value
    
class DeleteAccountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)