from rest_framework import serializers
from .models import Donation
from projects.models import Project

class Donation_Serializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Keep the user field read-only
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())  # Ensure project accepts a project ID


    class Meta:
        model = Donation
        fields = ['id', 'user', 'project', 'amount', 'date_donated']  # Include user_name in the fields

    def get_user_name(self, obj):
        return obj.user.username  # Return the username of the user

class DonationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    date_donated = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'


