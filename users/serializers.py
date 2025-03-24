from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
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
            'is_active',
            'date_joined',
            'last_login',
        ]
