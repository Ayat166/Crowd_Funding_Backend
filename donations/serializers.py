from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    date_donated = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'


