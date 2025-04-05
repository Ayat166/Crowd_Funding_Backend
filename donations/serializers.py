from rest_framework import serializers
from .models import Donation
from projects.models import Project

class DonationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Keep the user field read-only
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Ensure project accepts a project ID
    user_name = serializers.SerializerMethodField()  # Add a field to include the user's name

    class Meta:
        model = Donation
        fields = ['id', 'user', 'user_name', 'project', 'amount', 'date_donated']  # Include user_name in the fields

    def get_user_name(self, obj):
        return obj.user.username  # Return the username of the user